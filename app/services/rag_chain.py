"""LangChain Expression Language (LCEL) RAG Pipeline with Human-Friendly Agronomy Guidance."""

import time
import asyncio
from typing import List, Dict, Any, Optional, Tuple
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import get_settings
from app.services.vector_store import get_vector_store
from app.schemas import SourceReference
from app.utils.logger import logger

# Simple, Conversational, Human-Friendly Agronomy System Prompt
AGRONOMY_SYSTEM_PROMPT = """You are a friendly, expert Organic Terrace Gardening Advisor and Rooftop Safety Guide.
Your goal is to explain organic rooftop farming in simple, clear, and easy-to-understand language so that ANY beginner or home gardener can follow your advice with confidence.

COMMUNICATION STYLE & FORMATTING RULES:
1. SPEAK IN SIMPLE, PLAIN ENGLISH:
   - Avoid overly dense academic or chemical jargon.
   - Use clear everyday measurements (e.g., "1 teaspoon", "1 handful", "5 ml per liter of water").
   - Write warmly, encouragingly, and clearly.

2. STRUCTURE EVERY ANSWER BEAUTIFULLY:
   - 🎯 **Quick Answer / Summary**: Give the bottom-line answer in 1–2 simple sentences.
   - 📋 **Step-by-Step Guide or Recipe**: Use clear numbered steps or bullet points with exact quantities.
   - ⚠️ **Rooftop Safety Note** (if applicable): Explain roof weight/waterproofing in simple terms (e.g., "Why regular garden mud gets too heavy when wet and can strain your terrace slab").
   - 💡 **Helpful Gardener Tip**: A practical bonus tip to get the best results.

3. STRICT ORGANIC & ROOFTOP RULES:
   - Always recommend natural organic remedies (Neem oil, sour buttermilk spray, Jeevamrut, vermicompost, marigold companion planting).
   - NEVER suggest toxic chemical pesticides or synthetic chemical fertilizers.
   - For potting mix, always recommend the lightweight 3:1:1 mix (3 parts cocopeat, 1 part vermicompost, 1 part perlite) to protect the roof from heavy weight.

4. GROUNDED IN KNOWLEDGE:
   - Use the provided Context below to answer accurately.
   - If something isn't mentioned in the context, give safe general organic advice and encourage consulting a local gardening expert.

Context:
{context}

Question:
{question}

Provide your friendly, clear, and step-by-step response below:"""


def get_llm() -> ChatGoogleGenerativeAI:
    """Initialize and return the Google Gemini Chat Model."""
    settings = get_settings()
    model_name = settings.gemini_model
    if not model_name.startswith("models/"):
        model_name = f"models/{model_name}"
    logger.info(f"Initializing ChatGoogleGenerativeAI with model: {model_name}")
    return ChatGoogleGenerativeAI(
        model=model_name,
        google_api_key=settings.google_api_key,
        temperature=0.3,
        max_output_tokens=2048,
        transport="rest",
    )


def format_docs(docs: List[Document]) -> str:
    """Format retrieved documents into a context block with source headers."""
    formatted_chunks = []
    for i, doc in enumerate(docs, start=1):
        source_title = doc.metadata.get("title", "Rooftop Farming Knowledge Base")
        source_file = doc.metadata.get("source", "Unknown Document")
        section = doc.metadata.get("section", "")
        header = f"[Source {i}: {source_title}{f' - {section}' if section else ''}]"
        formatted_chunks.append(f"{header}\n{doc.page_content}")
    return "\n\n---\n\n".join(formatted_chunks)


def extract_source_references(docs: List[Document]) -> List[SourceReference]:
    """Convert LangChain Document objects into structured SourceReference schemas."""
    references = []
    for doc in docs:
        title = doc.metadata.get("title", "Urban Rooftop Knowledge Document")
        source = doc.metadata.get("source", "kb")
        content_snippet = doc.page_content.strip()
        if len(content_snippet) > 280:
            content_snippet = content_snippet[:277] + "..."
        references.append(
            SourceReference(
                title=title,
                source=source,
                content_snippet=content_snippet,
                metadata=doc.metadata,
            )
        )
    return references


def build_rag_chain():
    """Build the LCEL RAG chain pipeline."""
    llm = get_llm()
    prompt = ChatPromptTemplate.from_template(AGRONOMY_SYSTEM_PROMPT)
    output_parser = StrOutputParser()
    return prompt | llm | output_parser


_cached_gemini_model = None

def get_direct_gemini_model():
    """Return cached GenerativeModel instance."""
    global _cached_gemini_model
    if _cached_gemini_model is not None:
        return _cached_gemini_model
    
    settings = get_settings()
    import google.generativeai as genai
    genai.configure(api_key=settings.google_api_key)
    _cached_gemini_model = genai.GenerativeModel(settings.gemini_model)
    return _cached_gemini_model


async def run_rag_pipeline(
    question: str,
    top_k: Optional[int] = None,
    include_sources: bool = True,
) -> Tuple[str, List[SourceReference], int, str, float]:
    """Execute the fast RAG pipeline and return friendly answer, sources, chunk count, model name, and latency in ms."""
    start_time = time.perf_counter()
    settings = get_settings()
    k = top_k if top_k is not None else settings.top_k_retrieval

    logger.info(f"Executing RAG retrieval for question: '{question[:60]}...' with k={k}")

    # 1. Retrieve relevant documents from Vector Store
    vector_store = get_vector_store()
    retrieved_docs = await asyncio.to_thread(vector_store.similarity_search, question, k)
    logger.info(f"Retrieved {len(retrieved_docs)} context chunks")

    # 2. Format Context
    formatted_context = format_docs(retrieved_docs) if retrieved_docs else "No matching knowledge base documents found."

    # 3. Fast Prompt & LLM Generation
    prompt_text = AGRONOMY_SYSTEM_PROMPT.format(context=formatted_context, question=question)
    model = get_direct_gemini_model()
    
    response = await asyncio.to_thread(model.generate_content, prompt_text)
    answer = response.text

    # 4. Extract Sources
    sources = extract_source_references(retrieved_docs) if include_sources else []

    latency_ms = (time.perf_counter() - start_time) * 1000.0
    logger.info(f"RAG generation completed in {latency_ms:.2f} ms")

    return answer, sources, len(retrieved_docs), settings.gemini_model, latency_ms
