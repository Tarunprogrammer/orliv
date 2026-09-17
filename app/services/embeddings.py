"""Google Gemini Embeddings Service using text-embedding-004."""

from typing import Optional
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.config import get_settings
from app.utils.logger import logger

_embeddings_instance: Optional[GoogleGenerativeAIEmbeddings] = None


def get_embeddings() -> GoogleGenerativeAIEmbeddings:
    """Initialize or return the cached GoogleGenerativeAIEmbeddings singleton."""
    global _embeddings_instance
    if _embeddings_instance is not None:
        return _embeddings_instance

    settings = get_settings()

    if not settings.google_api_key or settings.google_api_key.startswith("your_"):
        logger.warning(
            "GOOGLE_API_KEY is not configured or contains placeholder value. "
            "Embeddings initialization will fail if invoked against the live API."
        )

    # Ensure model name is properly formatted
    model_name = settings.embedding_model
    if not model_name.startswith("models/"):
        model_name = f"models/{model_name}"

    logger.info(f"Initializing GoogleGenerativeAIEmbeddings with model: {model_name}")

    _embeddings_instance = GoogleGenerativeAIEmbeddings(
        model=model_name,
        google_api_key=settings.google_api_key,
        transport="rest",
    )
    return _embeddings_instance
