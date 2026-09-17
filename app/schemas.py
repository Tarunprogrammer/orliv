"""Pydantic V2 schemas for API request validation, response serialization, and project management."""

from typing import List, Dict, Any, Optional
from datetime import datetime, date
from pydantic import BaseModel, Field, ConfigDict


# ==============================================================================
# RAG Q&A Schemas
# ==============================================================================

class AskRequest(BaseModel):
    """Payload schema for submitting an agronomy / rooftop question."""

    question: str = Field(
        ...,
        min_length=3,
        max_length=1000,
        description="The user query regarding urban rooftop organic farming.",
        examples=["What is the recommended potting mix recipe to keep roof load safe?"],
    )
    top_k: Optional[int] = Field(
        default=3,
        ge=1,
        le=10,
        description="Number of relevant knowledge chunks to retrieve for grounding.",
    )
    include_sources: Optional[bool] = Field(
        default=True,
        description="Flag to include source document citations in the response payload.",
    )


class SourceReference(BaseModel):
    """Schema representing an individual retrieved document citation."""

    title: str = Field(..., description="Document title")
    source: str = Field(..., description="Source filename or origin")
    content_snippet: str = Field(..., description="Snippet of retrieved context")
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional chunk metadata"
    )


class AskResponse(BaseModel):
    """Response schema containing the generated agronomy advice with source grounding."""

    question: str = Field(..., description="Original user question")
    answer: str = Field(..., description="Generated agronomic guidance")
    sources: List[SourceReference] = Field(
        default_factory=list, description="Referenced grounding documents"
    )
    retrieved_chunks_count: int = Field(
        ..., description="Number of context chunks passed to the LLM"
    )
    model_used: str = Field(..., description="Google Gemini model identifier")
    latency_ms: float = Field(..., description="End-to-end request processing latency in ms")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ==============================================================================
# Health & Ingestion Schemas
# ==============================================================================

class HealthResponse(BaseModel):
    """Response schema for service health and connectivity status."""

    status: str = Field(..., description="Overall service status (healthy/degraded)")
    app_name: str = Field(..., description="Application name")
    version: str = Field(..., description="Application version")
    environment: str = Field(..., description="Deployment environment")
    database_dialect: str = Field(default="sqlite", description="Active database engine: 'mysql' or 'sqlite'")
    gemini_api_configured: bool = Field(..., description="Gemini API connectivity status")
    pinecone_configured: bool = Field(..., description="Pinecone Vector DB connectivity status")
    vector_store_stats: Dict[str, Any] = Field(
        default_factory=dict, description="Vector store statistics"
    )
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class IngestResponse(BaseModel):
    """Response schema for the knowledge base ingestion endpoint."""

    status: str = Field(..., description="Ingestion execution status")
    documents_processed: int = Field(
        ..., description="Total raw documents parsed from disk"
    )
    chunks_created: int = Field(
        ..., description="Total text chunks generated via text splitter"
    )
    vectors_upserted: int = Field(
        ..., description="Total vector embeddings upserted into Pinecone"
    )
    index_name: str = Field(..., description="Pinecone index name")
    backend: Optional[str] = Field(default=None, description="Vector store backend type")
    dimension: int = Field(..., description="Vector embedding dimension")
    duration_seconds: float = Field(..., description="Total time taken for ingestion")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ErrorResponse(BaseModel):
    """Standardized error response schema."""

    error: str = Field(..., description="Error category or type")
    message: str = Field(..., description="Human-readable error description")
    status_code: int = Field(..., description="HTTP status code")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ==============================================================================
# Crop Project & Real-Time Tracking Schemas
# ==============================================================================

class ProjectCreateRequest(BaseModel):
    """Payload to start a new rooftop crop project."""

    crop_type: str = Field(..., description="Crop template identifier: 'tomato', 'chilli', 'eggplant', 'spinach', 'cucumber', 'coriander'")
    crop_name: Optional[str] = Field(default=None, description="Custom name for your crop project")
    variety: Optional[str] = Field(default="Standard", description="Variety / cultivar name")
    planted_date: date = Field(default_factory=date.today, description="Date seeds were sown or transplanted")
    container_type: Optional[str] = Field(default="12x12 HDPE Grow Bag", description="Container or pot type")
    container_count: Optional[int] = Field(default=2, ge=1, le=50, description="Number of containers")
    soil_mix: Optional[str] = Field(default="3:1:1 Cocopeat + Vermicompost + Perlite", description="Potting soil recipe")
    rooftop_location: Optional[str] = Field(default="East Wall / Structural Beam", description="Placement area on terrace")
    notes: Optional[str] = Field(default=None, description="Initial project notes")


class CropTaskResponse(BaseModel):
    """Task item in project care timeline."""

    id: int
    project_id: int
    day_number: int
    stage: str
    title: str
    description: str
    category: str
    is_completed: bool
    completed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class ProjectLogCreateRequest(BaseModel):
    """Log an activity or observation."""

    log_type: str = Field(default="observation", description="watering, fertilizer, observation, pest, harvest")
    note: str = Field(..., min_length=2, description="Log message or care details")


class ProjectLogResponse(BaseModel):
    """Activity log entry response."""

    id: int
    project_id: int
    log_date: date
    log_type: str
    note: str
    photo_path: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DiagnosisResponse(BaseModel):
    """AI Vision disease diagnosis response."""

    id: Optional[int] = None
    project_id: Optional[int] = None
    crop_name: str
    image_url: str
    disease_name: str
    confidence: float
    severity: str
    symptoms: str
    organic_remedy: str
    preventive_measures: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(from_attributes=True)


class ProjectSummaryResponse(BaseModel):
    """Summary of a crop project for dashboard card listing."""

    id: int
    crop_type: str
    crop_name: str
    variety: str
    icon: str
    planted_date: date
    crop_age_days: int
    total_days: int
    days_to_harvest: int
    progress_percentage: int
    current_stage: str
    stage_summary: str
    today_water_ml: int
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProjectDetailResponse(BaseModel):
    """Comprehensive details of a crop project including real-time advice, tasks, logs, and diagnoses."""

    project: ProjectSummaryResponse
    container_type: str
    container_count: int
    soil_mix: str
    rooftop_location: str
    notes: Optional[str] = None
    realtime_care: Dict[str, Any]
    tasks: List[CropTaskResponse]
    logs: List[ProjectLogResponse]
    diagnoses: List[DiagnosisResponse]


# ==============================================================================
# Organic Knowledge & Calculator Schemas
# ==============================================================================

class RoofLoadRequest(BaseModel):
    """Payload to calculate rooftop structural load and potting mix volumes."""

    container_count: int = Field(default=10, ge=1, le=500, description="Total number of pots/grow bags")
    container_size_liters: float = Field(default=20.0, ge=1.0, le=500.0, description="Volume per container in liters (e.g. 20L for a 12x12 bag)")
    terrace_area_sqm: float = Field(default=10.0, ge=1.0, le=10000.0, description="Terrace/balcony area in square meters over which bags are distributed")
    soil_type: Optional[str] = Field(default="3:1:1_cocopeat_mix", description="3:1:1_cocopeat_mix, cocopeat_vermicompost, or traditional_topsoil")


class WeatherAdviceRequest(BaseModel):
    """Payload to evaluate rooftop microclimate and heatwave stress."""

    temp_celsius: float = Field(..., description="Current or forecast rooftop temperature in °C")
    humidity_pct: Optional[float] = Field(default=60.0, ge=0.0, le=100.0, description="Relative humidity %")
    wind_kmh: Optional[float] = Field(default=12.0, ge=0.0, le=150.0, description="Wind speed in km/h")
    uv_index: Optional[float] = Field(default=6.0, ge=0.0, le=15.0, description="UV index rating")
