"""CLI script to ingest curated rooftop farming knowledge base into Pinecone."""

import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from app.services.ingestion import ingest_knowledge_base
from app.config import get_settings
from app.utils.logger import logger


def main():
    """Main CLI execution entry point."""
    print("=" * 70)
    print("🌱 Urban Rooftop Organic Farming Assistant - Knowledge Base Ingestion")
    print("=" * 70)

    settings = get_settings()
    print(f"Embedding Model: {settings.embedding_model}")
    print(f"Target Pinecone Index: {settings.pinecone_index_name} (dim: {settings.pinecone_dimension})")
    print(f"Cloud/Region: {settings.pinecone_cloud}/{settings.pinecone_region}")
    print(f"Chunk Size / Overlap: {settings.chunk_size} / {settings.chunk_overlap}")
    print("-" * 70)

    if not settings.google_api_key or settings.google_api_key.startswith("your_"):
        print("❌ Error: GOOGLE_API_KEY is not set. Please update your .env file.")
        sys.exit(1)

    if not settings.pinecone_api_key or settings.pinecone_api_key.startswith("your_"):
        print("❌ Error: PINECONE_API_KEY is not set. Please update your .env file.")
        sys.exit(1)

    try:
        result = ingest_knowledge_base()
        print("\n✅ Ingestion Completed Successfully!")
        print(f" - Documents Processed : {result['documents_processed']}")
        print(f" - Chunks Generated    : {result['chunks_created']}")
        print(f" - Vectors Upserted    : {result['vectors_upserted']}")
        print(f" - Pinecone Index      : {result['index_name']}")
        print(f" - Elapsed Time        : {result['duration_seconds']}s")
        print("=" * 70)
    except Exception as e:
        logger.error(f"Ingestion failed: {e}", exc_info=True)
        print(f"\n❌ Ingestion Failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
