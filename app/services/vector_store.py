"""Vector Database Service supporting Pinecone Serverless and In-Memory RAM Vector Store."""

import time
from typing import Optional, Dict, Any, Union
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_core.vectorstores import InMemoryVectorStore, VectorStore
from app.config import get_settings
from app.services.embeddings import get_embeddings
from app.utils.logger import logger

_vector_store_instance: Optional[VectorStore] = None
_in_memory_ram_store: Optional[InMemoryVectorStore] = None
_pinecone_client: Optional[Pinecone] = None


def get_pinecone_client() -> Pinecone:
    """Return or initialize the singleton Pinecone client instance."""
    global _pinecone_client
    if _pinecone_client is not None:
        return _pinecone_client

    settings = get_settings()
    if not settings.pinecone_api_key or settings.pinecone_api_key.startswith("your_"):
        logger.warning(
            "PINECONE_API_KEY is not configured or contains placeholder value."
        )

    _pinecone_client = Pinecone(api_key=settings.pinecone_api_key)
    return _pinecone_client


def ensure_pinecone_index() -> None:
    """Check if the configured Pinecone index exists; create a serverless index if it doesn't."""
    settings = get_settings()
    client = get_pinecone_client()

    index_name = settings.pinecone_index_name
    logger.info(f"Checking existence of Pinecone index: '{index_name}'")

    existing_indexes = [idx.name for idx in client.list_indexes()]

    if index_name in existing_indexes:
        try:
            desc = client.describe_index(index_name)
            if desc.dimension != settings.pinecone_dimension:
                logger.warning(
                    f"Index '{index_name}' dimension ({desc.dimension}) differs from configured "
                    f"({settings.pinecone_dimension}). Re-creating index..."
                )
                client.delete_index(index_name)
                time.sleep(3)
                existing_indexes = [idx.name for idx in client.list_indexes()]
        except Exception as e:
            logger.warning(f"Could not verify existing index dimension: {e}")

    if index_name not in existing_indexes:
        logger.info(
            f"Index '{index_name}' not found. Creating Serverless Index "
            f"(dim={settings.pinecone_dimension}, metric={settings.pinecone_metric}, "
            f"cloud={settings.pinecone_cloud}, region={settings.pinecone_region})..."
        )
        client.create_index(
            name=index_name,
            dimension=settings.pinecone_dimension,
            metric=settings.pinecone_metric,
            spec=ServerlessSpec(
                cloud=settings.pinecone_cloud,
                region=settings.pinecone_region,
            ),
        )

        # Wait until the index is fully ready
        max_wait_seconds = 60
        waited = 0
        while not client.describe_index(index_name).status["ready"]:
            time.sleep(2)
            waited += 2
            if waited >= max_wait_seconds:
                raise TimeoutError(
                    f"Timed out after {max_wait_seconds}s waiting for Pinecone index '{index_name}' to become ready."
                )
        logger.info(f"Pinecone serverless index '{index_name}' created and ready.")
    else:
        logger.info(f"Pinecone index '{index_name}' already exists and is active.")


def get_ram_vector_store() -> InMemoryVectorStore:
    """Initialize or return the In-Memory RAM Vector Store."""
    global _in_memory_ram_store
    if _in_memory_ram_store is not None:
        return _in_memory_ram_store

    logger.info("Initializing In-Memory RAM VectorStore...")
    embeddings = get_embeddings()
    _in_memory_ram_store = InMemoryVectorStore(embedding=embeddings)
    return _in_memory_ram_store


def get_vector_store() -> VectorStore:
    """Return the active VectorStore based on configuration (Pinecone or RAM)."""
    global _vector_store_instance
    if _vector_store_instance is not None:
        return _vector_store_instance

    settings = get_settings()
    backend = settings.vector_store_backend.lower()

    if backend in ("ram", "memory", "in_memory"):
        logger.info("Operating in In-Memory (RAM) Vector Store mode.")
        _vector_store_instance = get_ram_vector_store()
        return _vector_store_instance

    # Default to Pinecone with auto-fallback support
    try:
        embeddings = get_embeddings()
        ensure_pinecone_index()
        logger.info(f"Initializing PineconeVectorStore for index: {settings.pinecone_index_name}")
        _vector_store_instance = PineconeVectorStore(
            index_name=settings.pinecone_index_name,
            embedding=embeddings,
            pinecone_api_key=settings.pinecone_api_key,
        )
        return _vector_store_instance
    except Exception as e:
        if backend == "auto":
            logger.warning(
                f"Pinecone connection failed ({e}). Falling back to In-Memory RAM Vector Store."
            )
            _vector_store_instance = get_ram_vector_store()
            return _vector_store_instance
        logger.error(f"Failed to initialize Pinecone Vector Store: {e}")
        raise e


def get_index_stats() -> Dict[str, Any]:
    """Retrieve runtime statistics for the configured Pinecone or RAM vector store."""
    settings = get_settings()
    backend = settings.vector_store_backend.lower()

    if backend in ("ram", "memory", "in_memory"):
        ram_store = get_ram_vector_store()
        store_dict = getattr(ram_store, "store", {})
        return {
            "backend": "RAM (In-Memory)",
            "total_vector_count": len(store_dict),
            "dimension": settings.pinecone_dimension,
        }

    client = get_pinecone_client()
    try:
        index = client.Index(settings.pinecone_index_name)
        stats = index.describe_index_stats()
        
        # Convert Pinecone stats object to native Python types
        total_vectors = getattr(stats, "total_vector_count", None)
        if total_vectors is None and isinstance(stats, dict):
            total_vectors = stats.get("total_vector_count", 0)
            
        dim = getattr(stats, "dimension", None)
        if dim is None and isinstance(stats, dict):
            dim = stats.get("dimension", settings.pinecone_dimension)
            
        namespaces = getattr(stats, "namespaces", None)
        if namespaces is None and isinstance(stats, dict):
            namespaces = stats.get("namespaces", {})

        return {
            "backend": "Pinecone Serverless",
            "total_vector_count": int(total_vectors) if total_vectors is not None else 0,
            "dimension": int(dim) if dim is not None else settings.pinecone_dimension,
            "namespaces": str(namespaces) if namespaces else {},
        }
    except Exception as e:
        logger.error(f"Failed to fetch Pinecone index stats: {e}")
        return {"error": str(e)}
