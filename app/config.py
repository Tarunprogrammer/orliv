"""Application Configuration Module using Pydantic Settings."""

from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables and .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # Application Information
    app_name: str = Field(
        default="Urban Rooftop Organic Farming RAG Assistant",
        description="Application Display Name",
    )
    app_env: str = Field(default="development", description="Application Environment")
    debug: bool = Field(default=False, description="Debug mode")
    host: str = Field(default="0.0.0.0", description="Server Host")
    port: int = Field(default=8000, description="Server Port")

    # Google Gemini API
    google_api_key: Optional[str] = Field(
        default=None,
        description="API Key for Google Gemini LLM & Embeddings",
    )
    gemini_model: str = Field(
        default="gemini-2.0-flash",
        description="Google Gemini Chat Model Name",
    )
    embedding_model: str = Field(
        default="models/text-embedding-004",
        description="Google Gemini Text Embedding Model Name",
    )

    # Pinecone Vector Database
    pinecone_api_key: Optional[str] = Field(
        default=None,
        description="Pinecone API Key",
    )
    pinecone_index_name: str = Field(
        default="urban-rooftop-farming",
        description="Pinecone Index Name",
    )
    pinecone_cloud: str = Field(
        default="aws",
        description="Pinecone Serverless Cloud Provider",
    )
    pinecone_region: str = Field(
        default="us-east-1",
        description="Pinecone Serverless Cloud Region",
    )
    pinecone_dimension: int = Field(
        default=768,
        description="Embedding Vector Dimension (768 for text-embedding-004)",
    )
    pinecone_metric: str = Field(
        default="cosine",
        description="Vector Similarity Metric",
    )
    vector_store_backend: str = Field(
        default="pinecone",
        description="Vector store backend to use: 'pinecone', 'ram' (in-memory), or 'auto'",
    )

    # Database Settings (Local MySQL with SQLite fallback)
    db_dialect: str = Field(
        default="mysql",
        description="Database dialect: 'mysql' for local MySQL or 'sqlite' for local SQLite file",
    )
    mysql_host: str = Field(default="localhost", description="MySQL host")
    mysql_port: int = Field(default=3306, description="MySQL port")
    mysql_user: str = Field(default="root", description="MySQL user")
    mysql_password: str = Field(default="", description="MySQL password")
    mysql_database: str = Field(default="rooftop_farming", description="MySQL database name")

    # RAG Retrieval & Ingestion Hyperparameters
    top_k_retrieval: int = Field(
        default=3,
        description="Number of top documents to retrieve for RAG context",
        ge=1,
        le=10,
    )
    chunk_size: int = Field(
        default=600,
        description="Character count per document chunk during ingestion",
    )
    chunk_overlap: int = Field(
        default=100,
        description="Character overlap between consecutive chunks",
    )


@lru_cache()
def get_settings() -> Settings:
    """Return cached application settings instance."""
    return Settings()
