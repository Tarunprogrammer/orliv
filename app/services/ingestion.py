"""Unified Ingestion & Training Pipeline for Markdown, PDFs, Spreadsheets, and Web URLs."""

import os
import time
import asyncio
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional, Union
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config import get_settings
from app.services.vector_store import get_vector_store
from app.services.multi_loader import (
    load_pdf_file,
    load_excel_file,
    load_url_page,
)
from app.utils.logger import logger


def load_markdown_documents(data_dir: Path) -> List[Tuple[str, str, Dict[str, Any]]]:
    """Load all markdown files from the data directory and extract titles and metadata."""
    if not data_dir.exists():
        raise FileNotFoundError(f"Knowledge base data directory '{data_dir}' does not exist.")

    markdown_files = sorted(list(data_dir.glob("*.md")))
    if not markdown_files:
        raise FileNotFoundError(f"No .md files found in knowledge base directory '{data_dir}'.")

    documents_data = []
    for filepath in markdown_files:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read().strip()

            title = filepath.stem.replace("_", " ").title()
            for line in content.splitlines():
                if line.startswith("# "):
                    title = line.replace("# ", "").strip()
                    break

            metadata = {
                "source": filepath.name,
                "title": title,
                "file_path": str(filepath.resolve()),
                "file_type": "markdown",
            }
            documents_data.append((filepath.name, content, metadata))
            logger.info(f"Loaded document: '{filepath.name}' ({len(content)} chars) - '{title}'")
        except Exception as e:
            logger.error(f"Error reading {filepath}: {e}")
            raise

    return documents_data


def chunk_documents(
    documents_data: List[Tuple[str, str, Dict[str, Any]]],
    chunk_size: int,
    chunk_overlap: int,
) -> List[Document]:
    """Split raw document contents into smaller semantic chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n## ", "\n### ", "\n\n", "\n", ". ", " ", ""],
        is_separator_regex=False,
    )

    all_chunks: List[Document] = []
    for filename, text, base_metadata in documents_data:
        raw_chunks = text_splitter.split_text(text)
        for idx, chunk_text in enumerate(raw_chunks):
            section_title = ""
            for line in chunk_text.splitlines():
                if line.startswith("## ") or line.startswith("### "):
                    section_title = line.lstrip("#").strip()
                    break

            chunk_metadata = {
                **base_metadata,
                "chunk_index": idx,
                "total_chunks_in_doc": len(raw_chunks),
                "section": section_title,
            }
            all_chunks.append(Document(page_content=chunk_text, metadata=chunk_metadata))

    return all_chunks


def ingest_raw_documents(raw_docs: List[Document], source_name: str = "Raw Data Ingestion") -> Dict[str, Any]:
    """Unified ingestion: Chunks, embeds, and batch upserts any list of LangChain documents."""
    start_time = time.perf_counter()
    settings = get_settings()

    if not raw_docs:
        raise ValueError("No valid document content provided to ingest.")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        separators=["\n## ", "\n### ", "\n\n", "\n", ". ", " ", ""],
        is_separator_regex=False,
    )

    chunk_docs: List[Document] = []
    for doc in raw_docs:
        sub_chunks = text_splitter.split_text(doc.page_content)
        for idx, chunk_text in enumerate(sub_chunks):
            chunk_meta = {
                **doc.metadata,
                "chunk_index": idx,
                "total_sub_chunks": len(sub_chunks),
            }
            chunk_docs.append(Document(page_content=chunk_text, metadata=chunk_meta))

    logger.info(f"Split {len(raw_docs)} documents into {len(chunk_docs)} semantic chunks.")

    backend = settings.vector_store_backend.lower()
    vector_store = get_vector_store()
    target_name = "RAM (In-Memory)" if backend in ("ram", "memory", "in_memory") else settings.pinecone_index_name

    logger.info(f"Upserting {len(chunk_docs)} chunks into vector store target '{target_name}' (backend: {backend})...")

    # Batch upsert with rate limit protection
    batch_size = 20
    total_batches = (len(chunk_docs) + batch_size - 1) // batch_size
    for i in range(0, len(chunk_docs), batch_size):
        batch = chunk_docs[i : i + batch_size]
        batch_num = i // batch_size + 1
        logger.info(f"Upserting batch {batch_num}/{total_batches} ({len(batch)} chunks)...")

        max_retries = 5
        for attempt in range(max_retries):
            try:
                vector_store.add_documents(batch)
                break
            except Exception as e:
                err_str = str(e)
                if ("429" in err_str or "RESOURCE_EXHAUSTED" in err_str) and attempt < max_retries - 1:
                    wait_sec = 25 * (attempt + 1)
                    logger.warning(f"Rate limit reached on batch {batch_num}. Waiting {wait_sec}s before retry...")
                    time.sleep(wait_sec)
                else:
                    raise e

        if i + batch_size < len(chunk_docs):
            time.sleep(2)

    duration = time.perf_counter() - start_time
    logger.info(f"Successfully ingested {len(chunk_docs)} vectors in {duration:.2f} seconds.")

    return {
        "status": "success",
        "source": source_name,
        "documents_processed": len(raw_docs),
        "chunks_created": len(chunk_docs),
        "vectors_upserted": len(chunk_docs),
        "index_name": target_name,
        "backend": backend,
        "dimension": settings.pinecone_dimension,
        "duration_seconds": round(duration, 2),
    }


def ingest_knowledge_base(data_path: Optional[str] = None) -> Dict[str, Any]:
    """Ingest markdown files from data directory."""
    if data_path:
        base_dir = Path(data_path)
    else:
        base_dir = Path(__file__).resolve().parent.parent.parent / "data"

    raw_data = load_markdown_documents(base_dir)
    docs = [
        Document(page_content=content, metadata=meta)
        for _, content, meta in raw_data
    ]
    return ingest_raw_documents(docs, source_name=str(base_dir.resolve()))
