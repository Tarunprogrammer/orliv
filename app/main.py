"""FastAPI Backend Application: Urban Rooftop Organic Farming Assistant, Project Tracker, AI Plant Doctor & Organic Knowledge APIs."""

import os
import sys
import uuid
import shutil
from pathlib import Path
from contextlib import asynccontextmanager
from typing import AsyncGenerator, List, Optional, Dict, Any
from datetime import datetime, date

from fastapi import FastAPI, HTTPException, status, Request, Depends, UploadFile, File, Form, Query
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app import __version__
from app.config import get_settings
from app.database import get_db, init_db, get_db_dialect, UPLOADS_DIR
from app.models import CropProject, CropTask, ProjectLog, DiseaseDiagnosis
from app.schemas import (
    AskRequest,
    AskResponse,
    HealthResponse,
    IngestResponse,
    ErrorResponse,
    ProjectCreateRequest,
    ProjectSummaryResponse,
    ProjectDetailResponse,
    ProjectLogCreateRequest,
    ProjectLogResponse,
    CropTaskResponse,
    DiagnosisResponse,
    RoofLoadRequest,
    WeatherAdviceRequest,
)
from app.services.rag_chain import run_rag_pipeline
from app.services.vector_store import get_index_stats
from app.services.ingestion import ingest_knowledge_base
from app.services.crop_engine import get_crop_realtime_status, CROP_TEMPLATES
from app.services.vision_doctor import analyze_plant_photo
from app.services.organic_knowledge import (
    ORGANIC_REMEDIES,
    ORGANIC_FERTILIZERS,
    COMPANION_MATRIX,
    SEED_TREATMENTS,
    ROOFTOP_CROPS,
    GOVERNMENT_SCHEMES,
    calculate_rooftop_load,
    get_weather_microclimate_advice,
)
from app.utils.logger import logger

STATIC_DIR = Path(__file__).resolve().parent / "static"


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Startup initialization: initialize database tables and verify vector store."""
    settings = get_settings()
    backend = settings.vector_store_backend.lower()
    logger.info(f"Starting {settings.app_name} v{__version__} [{settings.app_env}] (Backend: {backend})...")

    # Initialize Database tables (MySQL or SQLite fallback)
    init_db()

    logger.info(f"Application startup completed successfully with active DB: '{get_db_dialect()}'.")
    yield
    logger.info("Shutting down Urban Rooftop Organic Farming Assistant...")


# Initialize FastAPI instance
settings = get_settings()
app = FastAPI(
    title=settings.app_name,
    description=(
        "Production-grade Real-Time Rooftop Organic Agriculture Platform with MySQL Database Support, "
        "Crop Project Tracking, AI Vision Plant Disease Diagnostics, RAG Intelligence, and Organic Knowledge APIs."
    ),
    version=__version__,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount uploads static folder to serve diagnostic images
app.mount("/uploads", StaticFiles(directory=str(UPLOADS_DIR)), name="uploads")


# ==============================================================================
# Global Exception Handlers
# ==============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.warning(f"HTTPException [{exc.status_code}] on {request.url.path}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error="HTTPException",
            message=str(exc.detail),
            status_code=exc.status_code,
        ).model_dump(mode="json"),
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.critical(f"Unhandled Exception on {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error="InternalServerError",
            message="An unexpected server error occurred. Please consult the system logs.",
            status_code=500,
        ).model_dump(mode="json"),
    )


# ==============================================================================
# Web UI Endpoint
# ==============================================================================

@app.get(
    "/",
    response_class=HTMLResponse,
    tags=["Web UI"],
    summary="Interactive Web User Interface",
)
async def web_ui():
    """Serve the interactive Urban Rooftop Organic Farming Assistant Web Interface."""
    index_path = STATIC_DIR / "index.html"
    if index_path.exists():
        with open(index_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Urban Rooftop Organic Farming Assistant</h1><p>Web UI is loading...</p>")


# ==============================================================================
# Health & Status
# ==============================================================================

@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["Health"],
    summary="Application Health & Connectivity Check",
)
async def health_check():
    """Check API connectivity, active database dialect (MySQL / SQLite), vector store health, and environment configuration."""
    api_key_configured = bool(settings.google_api_key and not settings.google_api_key.startswith("your_"))
    pinecone_key_configured = bool(settings.pinecone_api_key and not settings.pinecone_api_key.startswith("your_"))
    stats = get_index_stats()
    index_healthy = stats.get("status") in ("connected", "ready") or stats.get("total_vectors", 0) >= 0
    overall_status = "healthy" if (api_key_configured and index_healthy) else "degraded"

    return HealthResponse(
        status=overall_status,
        app_name=settings.app_name,
        version=__version__,
        environment=settings.app_env,
        database_dialect=get_db_dialect(),
        gemini_api_configured=api_key_configured,
        pinecone_configured=pinecone_key_configured,
        vector_store_stats=stats,
        timestamp=datetime.utcnow(),
    )


# ==============================================================================
# SPECIALIZED ORGANIC FARMING KNOWLEDGE APIS
# ==============================================================================

@app.get(
    "/api/organic/remedies",
    tags=["Organic Knowledge"],
    summary="Get 100% Organic Pest & Fungal Remedies Library",
)
async def get_remedies(
    search: Optional[str] = Query(None, description="Search query for pest, disease, or ingredient (e.g. 'mildew', 'aphids', 'neem')"),
    category: Optional[str] = Query(None, description="Category filter (e.g. 'Botanical', 'Microbial', 'Mineral')"),
):
    """Retrieve verified natural pest and disease remedies with exact household recipes and application methods."""
    results = ORGANIC_REMEDIES
    if search:
        s = search.lower()
        results = [
            r for r in results
            if s in r["name"].lower()
            or s in r["category"].lower()
            or any(s in p.lower() for p in r["target_pests"])
        ]
    if category:
        c = category.lower()
        results = [r for r in results if c in r["category"].lower()]

    return {"total": len(results), "remedies": results}


@app.get(
    "/api/organic/fertilizers",
    tags=["Organic Knowledge"],
    summary="Get Organic Bio-Fertilizer Recipes & NPK Formulations",
)
async def get_fertilizers(
    search: Optional[str] = Query(None, description="Search query for fertilizer or nutrient (e.g. 'potassium', 'jeevamrut', 'calcium')"),
):
    """Retrieve complete bio-fertilizer recipes (Jeevamrut, Panchagavya, Vermicompost, Banana peel tea, Eggshell calcium) with NPK profiles and dosage."""
    results = ORGANIC_FERTILIZERS
    if search:
        s = search.lower()
        results = [
            f for f in results
            if s in f["name"].lower()
            or s in f["category"].lower()
            or s in f["npk_profile"].lower()
        ]
    return {"total": len(results), "fertilizers": results}


@app.get(
    "/api/organic/companion-guide",
    tags=["Organic Knowledge"],
    summary="Get Companion Planting Matrix & Guild Synergies",
)
async def get_companion_guide(
    crop: Optional[str] = Query(None, description="Crop name to look up companions (e.g. 'tomato', 'chilli', 'cucumber', 'spinach')"),
):
    """Get synergistic companion plant pairings, pest repellence guilds, and antagonist warnings."""
    if crop:
        c = crop.lower().strip()
        data = COMPANION_MATRIX.get(c)
        if not data:
            # Fallback search
            for k, v in COMPANION_MATRIX.items():
                if c in k or k in c:
                    return {"crop": k, "data": v}
            raise HTTPException(status_code=404, detail=f"Companion data for '{crop}' not found. Available crops: {list(COMPANION_MATRIX.keys())}")
        return {"crop": c, "data": data}
    return {"crops_available": list(COMPANION_MATRIX.keys()), "companion_matrix": COMPANION_MATRIX}


@app.get(
    "/api/organic/seed-treatment",
    tags=["Organic Knowledge"],
    summary="Get Thermal Hot Water Seed Treatment Chart",
)
async def get_seed_treatments(
    crop: Optional[str] = Query(None, description="Crop name to look up (e.g. 'tomato', 'potato', 'cabbage', 'radish')"),
):
    """Retrieve hot water immersion temperatures (°C / °F) and durations to eliminate seed-borne bacterial and fungal pathogens."""
    if crop:
        c = crop.lower()
        matched = [
            t for t in SEED_TREATMENTS
            if any(c in x.lower() for x in t["crops"]) or c in t["crop_group"].lower()
        ]
        return {"total": len(matched), "results": matched}
    return {"total": len(SEED_TREATMENTS), "seed_treatments": SEED_TREATMENTS}


@app.post(
    "/api/organic/roof-calculator",
    tags=["Organic Knowledge"],
    summary="Calculate Rooftop Structural Weight Load & 3:1:1 Potting Mix Volumes",
)
async def calculate_roof_weight(payload: RoofLoadRequest):
    """Calculate total wet saturated weight in kg/m², safety compliance vs 150 kg/m² building code, and exact 3:1:1 cocopeat mix volumes in liters."""
    return calculate_rooftop_load(
        container_count=payload.container_count,
        container_size_liters=payload.container_size_liters,
        terrace_area_sqm=payload.terrace_area_sqm,
        soil_type=payload.soil_type or "3:1:1_cocopeat_mix",
    )


@app.get(
    "/api/organic/schemes",
    tags=["Organic Knowledge"],
    summary="Get Indian Government Organic Farming Schemes & Subsidies",
)
async def get_schemes():
    """Retrieve financial assistance details, eligibility criteria, and APEDA Tracenet certification workflows for major government organic schemes (PKVY, MOVCDNER, CISS, NPOP)."""
    return {"total": len(GOVERNMENT_SCHEMES), "schemes": GOVERNMENT_SCHEMES}


@app.get(
    "/api/organic/crops",
    tags=["Organic Knowledge"],
    summary="Get Rooftop Crop Catalog & Sowing Calendar",
)
async def get_crops_catalog(
    season: Optional[str] = Query(None, description="Filter by season (e.g. 'Kharif', 'Rabi', 'Summer')"),
):
    """Retrieve catalog of 15+ urban rooftop crops with container depths, germination temps, sunlight hours, water ml/day, and pH ranges."""
    results = ROOFTOP_CROPS
    if season:
        s = season.lower()
        results = [c for c in results if s in c["season"].lower()]
    return {"total": len(results), "crops": results}


@app.post(
    "/api/organic/weather-advisor",
    tags=["Organic Knowledge"],
    summary="Get Real-Time Rooftop Microclimate & Heatwave Care Advice",
)
async def get_weather_advice(payload: WeatherAdviceRequest):
    """Evaluate temperature, humidity, wind, and UV conditions to produce actionable rooftop gardening alerts (shade netting, watering frequency, fungal protection)."""
    return get_weather_microclimate_advice(
        temp_celsius=payload.temp_celsius,
        humidity_pct=payload.humidity_pct or 60.0,
        wind_kmh=payload.wind_kmh or 12.0,
        uv_index=payload.uv_index or 6.0,
    )


# ==============================================================================
# Crop Projects API (Real-Time Tracking & Management)
# ==============================================================================

@app.post(
    "/api/projects",
    response_model=ProjectSummaryResponse,
    tags=["Projects"],
    summary="Create a new Rooftop Crop Project",
)
async def create_crop_project(payload: ProjectCreateRequest, db: Session = Depends(get_db)):
    """Create a new crop project and populate its automated care timeline tasks."""
    crop_type = payload.crop_type.lower()
    template = CROP_TEMPLATES.get(crop_type, CROP_TEMPLATES["tomato"])
    crop_name = payload.crop_name or f"{template['name']} Project"
    variety = payload.variety or template["default_variety"]

    project = CropProject(
        crop_type=crop_type,
        crop_name=crop_name,
        variety=variety,
        planted_date=payload.planted_date,
        container_type=payload.container_type or template["recommended_pot"],
        container_count=payload.container_count or 2,
        soil_mix=payload.soil_mix or "3:1:1 Cocopeat + Vermicompost + Perlite",
        rooftop_location=payload.rooftop_location or "East Wall / Structural Beam",
        notes=payload.notes,
        status="active",
    )
    db.add(project)
    db.commit()
    db.refresh(project)

    # Populate preset tasks
    for t in template.get("preset_tasks", []):
        task = CropTask(
            project_id=project.id,
            day_number=t["day"],
            stage=t["stage"],
            title=t["title"],
            description=t["desc"],
            category=t["cat"],
            is_completed=False,
        )
        db.add(task)

    # Initial creation log
    log = ProjectLog(
        project_id=project.id,
        log_type="observation",
        note=f"Project started! Planted {project.crop_name} ({project.variety}) in {project.container_count}x {project.container_type}.",
    )
    db.add(log)
    db.commit()

    rt = get_crop_realtime_status(project.crop_type, project.planted_date)
    return ProjectSummaryResponse(
        id=project.id,
        crop_type=project.crop_type,
        crop_name=project.crop_name,
        variety=project.variety,
        icon=rt["icon"],
        planted_date=project.planted_date,
        crop_age_days=rt["crop_age_days"],
        total_days=rt["total_days"],
        days_to_harvest=rt["days_to_harvest"],
        progress_percentage=rt["progress_percentage"],
        current_stage=rt["current_stage"],
        stage_summary=rt["stage_summary"],
        today_water_ml=rt["today_water_ml"],
        status=project.status,
        created_at=project.created_at,
    )


@app.get(
    "/api/projects",
    response_model=List[ProjectSummaryResponse],
    tags=["Projects"],
    summary="List all User Crop Projects with Real-Time Status",
)
async def list_crop_projects(db: Session = Depends(get_db)):
    """Fetch all active crop projects with dynamically calculated real-time days and stages."""
    projects = db.query(CropProject).order_by(CropProject.created_at.desc()).all()
    results = []
    for p in projects:
        rt = get_crop_realtime_status(p.crop_type, p.planted_date)
        results.append(
            ProjectSummaryResponse(
                id=p.id,
                crop_type=p.crop_type,
                crop_name=p.crop_name,
                variety=p.variety,
                icon=rt["icon"],
                planted_date=p.planted_date,
                crop_age_days=rt["crop_age_days"],
                total_days=rt["total_days"],
                days_to_harvest=rt["days_to_harvest"],
                progress_percentage=rt["progress_percentage"],
                current_stage=rt["current_stage"],
                stage_summary=rt["stage_summary"],
                today_water_ml=rt["today_water_ml"],
                status=p.status,
                created_at=p.created_at,
            )
        )
    return results


@app.get(
    "/api/projects/{project_id}",
    response_model=ProjectDetailResponse,
    tags=["Projects"],
    summary="Get Comprehensive Real-Time Crop Project Details",
)
async def get_project_details(project_id: int, db: Session = Depends(get_db)):
    """Fetch dedicated project hub data: real-time care advice, tasks, activity logs, and disease diagnoses."""
    p = db.query(CropProject).filter(CropProject.id == project_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Crop project not found.")

    rt = get_crop_realtime_status(p.crop_type, p.planted_date)

    summary = ProjectSummaryResponse(
        id=p.id,
        crop_type=p.crop_type,
        crop_name=p.crop_name,
        variety=p.variety,
        icon=rt["icon"],
        planted_date=p.planted_date,
        crop_age_days=rt["crop_age_days"],
        total_days=rt["total_days"],
        days_to_harvest=rt["days_to_harvest"],
        progress_percentage=rt["progress_percentage"],
        current_stage=rt["current_stage"],
        stage_summary=rt["stage_summary"],
        today_water_ml=rt["today_water_ml"],
        status=p.status,
        created_at=p.created_at,
    )

    tasks = [CropTaskResponse.model_validate(t) for t in p.tasks]
    logs = [ProjectLogResponse.model_validate(l) for l in p.logs]
    diagnoses = [
        DiagnosisResponse(
            id=d.id,
            project_id=d.project_id,
            crop_name=d.crop_name,
            image_url=f"/uploads/{Path(d.image_path).name}",
            disease_name=d.disease_name,
            confidence=d.confidence,
            severity=d.severity,
            symptoms=d.symptoms,
            organic_remedy=d.organic_remedy,
            preventive_measures=d.preventive_measures,
            created_at=d.created_at,
        )
        for d in p.diagnoses
    ]

    return ProjectDetailResponse(
        project=summary,
        container_type=p.container_type,
        container_count=p.container_count,
        soil_mix=p.soil_mix,
        rooftop_location=p.rooftop_location,
        notes=p.notes,
        realtime_care=rt,
        tasks=tasks,
        logs=logs,
        diagnoses=diagnoses,
    )


@app.delete(
    "/api/projects/{project_id}",
    tags=["Projects"],
    summary="Delete Crop Project",
)
async def delete_project(project_id: int, db: Session = Depends(get_db)):
    """Remove a crop project and its associated history."""
    p = db.query(CropProject).filter(CropProject.id == project_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Crop project not found.")
    db.delete(p)
    db.commit()
    return {"status": "success", "message": f"Project '{p.crop_name}' deleted."}


@app.post(
    "/api/projects/{project_id}/logs",
    response_model=ProjectLogResponse,
    tags=["Projects"],
    summary="Add an Activity Log or Note to Project",
)
async def add_project_log(
    project_id: int,
    payload: ProjectLogCreateRequest,
    db: Session = Depends(get_db),
):
    """Add a care note, watering entry, or pest observation."""
    p = db.query(CropProject).filter(CropProject.id == project_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Crop project not found.")

    log = ProjectLog(
        project_id=project_id,
        log_type=payload.log_type,
        note=payload.note,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return ProjectLogResponse.model_validate(log)


@app.patch(
    "/api/tasks/{task_id}/toggle",
    tags=["Projects"],
    summary="Toggle Task Completed Status",
)
async def toggle_task_status(task_id: int, db: Session = Depends(get_db)):
    """Mark a care task as completed or pending."""
    task = db.query(CropTask).filter(CropTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found.")
    task.is_completed = not task.is_completed
    task.completed_at = datetime.utcnow() if task.is_completed else None
    db.commit()
    return {"status": "success", "task_id": task.id, "is_completed": task.is_completed}


# ==============================================================================
# AI Vision Plant Disease Doctor Endpoints
# ==============================================================================

@app.post(
    "/api/projects/{project_id}/diagnose",
    response_model=DiagnosisResponse,
    tags=["Disease Doctor"],
    summary="Upload Leaf Photo for AI Disease Diagnosis (Attached to Project)",
)
async def diagnose_crop_disease(
    project_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """Upload a leaf or plant photo to diagnose disease with Gemini Vision and get 100% organic cures."""
    p = db.query(CropProject).filter(CropProject.id == project_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Crop project not found.")

    contents = await file.read()
    if not contents:
        raise HTTPException(status_code=400, detail="Uploaded photo is empty.")

    file_ext = Path(file.filename or "leaf.jpg").suffix or ".jpg"
    saved_filename = f"crop_{project_id}_{uuid.uuid4().hex[:8]}{file_ext}"
    saved_path = UPLOADS_DIR / saved_filename
    with open(saved_path, "wb") as f:
        f.write(contents)

    diag_data = analyze_plant_photo(contents, crop_context=p.crop_name)

    diagnosis = DiseaseDiagnosis(
        project_id=p.id,
        crop_name=diag_data.get("crop_identified", p.crop_name),
        image_path=str(saved_path),
        disease_name=diag_data.get("disease_name", "Foliar Stress"),
        confidence=float(diag_data.get("confidence", 0.90)),
        severity=diag_data.get("severity", "Moderate"),
        symptoms=diag_data.get("symptoms", "Visible spotting"),
        organic_remedy=diag_data.get("organic_remedy", "Spray Neem oil emulsion"),
        preventive_measures=diag_data.get("preventive_measures", "Maintain airflow"),
    )
    db.add(diagnosis)

    log = ProjectLog(
        project_id=p.id,
        log_type="pest",
        note=f"AI Plant Doctor Diagnosis: Detected '{diagnosis.disease_name}' ({diagnosis.severity} severity).",
        photo_path=f"/uploads/{saved_filename}",
    )
    db.add(log)
    db.commit()
    db.refresh(diagnosis)

    return DiagnosisResponse(
        id=diagnosis.id,
        project_id=diagnosis.project_id,
        crop_name=diagnosis.crop_name,
        image_url=f"/uploads/{saved_filename}",
        disease_name=diagnosis.disease_name,
        confidence=diagnosis.confidence,
        severity=diagnosis.severity,
        symptoms=diagnosis.symptoms,
        organic_remedy=diagnosis.organic_remedy,
        preventive_measures=diagnosis.preventive_measures,
        created_at=diagnosis.created_at,
    )


@app.post(
    "/api/diagnose-standalone",
    response_model=DiagnosisResponse,
    tags=["Disease Doctor"],
    summary="Upload Photo for Standalone AI Plant Disease Diagnosis",
)
async def diagnose_standalone(
    file: UploadFile = File(...),
    crop_name: Optional[str] = Form("Rooftop Plant"),
    db: Session = Depends(get_db),
):
    """Diagnose any plant photo without linking to a specific project."""
    contents = await file.read()
    if not contents:
        raise HTTPException(status_code=400, detail="Uploaded photo is empty.")

    file_ext = Path(file.filename or "plant.jpg").suffix or ".jpg"
    saved_filename = f"quick_{uuid.uuid4().hex[:8]}{file_ext}"
    saved_path = UPLOADS_DIR / saved_filename
    with open(saved_path, "wb") as f:
        f.write(contents)

    diag_data = analyze_plant_photo(contents, crop_context=crop_name)

    diagnosis = DiseaseDiagnosis(
        project_id=None,
        crop_name=diag_data.get("crop_identified", crop_name or "Rooftop Plant"),
        image_path=str(saved_path),
        disease_name=diag_data.get("disease_name", "General Stress"),
        confidence=float(diag_data.get("confidence", 0.90)),
        severity=diag_data.get("severity", "Moderate"),
        symptoms=diag_data.get("symptoms", "Leaf discoloration"),
        organic_remedy=diag_data.get("organic_remedy", "Apply organic neem spray"),
        preventive_measures=diag_data.get("preventive_measures", "Improve sunlight and spacing"),
    )
    db.add(diagnosis)
    db.commit()
    db.refresh(diagnosis)

    return DiagnosisResponse(
        id=diagnosis.id,
        project_id=None,
        crop_name=diagnosis.crop_name,
        image_url=f"/uploads/{saved_filename}",
        disease_name=diagnosis.disease_name,
        confidence=diagnosis.confidence,
        severity=diagnosis.severity,
        symptoms=diagnosis.symptoms,
        organic_remedy=diagnosis.organic_remedy,
        preventive_measures=diagnosis.preventive_measures,
        created_at=diagnosis.created_at,
    )


# ==============================================================================
# RAG Q&A Endpoint
# ==============================================================================

@app.post(
    "/ask",
    response_model=AskResponse,
    tags=["RAG"],
    summary="Ask Rooftop Organic Agriculture Question",
)
async def ask_question_endpoint(payload: AskRequest):
    """Submit a question to the Urban Rooftop Organic Farming Assistant."""
    settings = get_settings()
    if not settings.google_api_key or settings.google_api_key.startswith("your_"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="GOOGLE_API_KEY is not configured.",
        )

    try:
        answer, sources, chunk_count, model_used, latency_ms = await run_rag_pipeline(
            question=payload.question,
            top_k=payload.top_k,
            include_sources=payload.include_sources,
        )

        return AskResponse(
            question=payload.question,
            answer=answer,
            sources=sources,
            retrieved_chunks_count=chunk_count,
            model_used=model_used,
            latency_ms=round(latency_ms, 2),
            timestamp=datetime.utcnow(),
        )
    except Exception as e:
        logger.error(f"Error during RAG execution: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}",
        )


# ==============================================================================
# Knowledge Base Ingestion Endpoint
# ==============================================================================

@app.post(
    "/ingest",
    response_model=IngestResponse,
    tags=["Ingestion"],
    summary="Ingest/Reload Knowledge Base Directory into Pinecone or RAM",
)
async def trigger_ingestion():
    """Trigger on-demand document loading and upserting into Pinecone or RAM."""
    try:
        result = ingest_knowledge_base()
        return IngestResponse(**result)
    except Exception as e:
        logger.error(f"Ingestion failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Knowledge base ingestion failed: {str(e)}")
