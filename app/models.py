"""SQLAlchemy ORM Models for Crop Projects, Tasks, Growth Logs, and Disease Diagnoses."""

from datetime import datetime, date
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Float,
    Boolean,
    DateTime,
    Date,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from app.database import Base


class CropProject(Base):
    """User-created Rooftop Crop Project."""
    __tablename__ = "crop_projects"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    crop_type = Column(String(50), nullable=False, index=True)  # 'tomato', 'chilli', 'eggplant', etc.
    crop_name = Column(String(100), nullable=False)            # e.g., 'Tomato (Arka Rakshak)'
    variety = Column(String(100), default="Heirloom / Standard")
    planted_date = Column(Date, nullable=False, default=date.today)
    container_type = Column(String(100), default="12x12 HDPE Grow Bag")
    container_count = Column(Integer, default=2)
    soil_mix = Column(String(100), default="3:1:1 Cocopeat + Vermicompost + Perlite")
    sunlight_hours = Column(Integer, default=6)
    rooftop_location = Column(String(100), default="East Wall / Structural Beam")
    notes = Column(Text, nullable=True)
    status = Column(String(30), default="active", index=True)  # 'active', 'harvested', 'archived'
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    tasks = relationship("CropTask", back_populates="project", cascade="all, delete-orphan", order_by="CropTask.day_number")
    logs = relationship("ProjectLog", back_populates="project", cascade="all, delete-orphan", order_by="ProjectLog.created_at.desc()")
    diagnoses = relationship("DiseaseDiagnosis", back_populates="project", cascade="all, delete-orphan", order_by="DiseaseDiagnosis.created_at.desc()")


class CropTask(Base):
    """Automated and custom care tasks scheduled for a specific day in the crop lifecycle."""
    __tablename__ = "crop_tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("crop_projects.id", ondelete="CASCADE"), nullable=False, index=True)
    day_number = Column(Integer, nullable=False)
    stage = Column(String(50), nullable=False)  # 'Germination', 'Vegetative', 'Flowering', 'Fruiting', 'Harvest'
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(50), default="general")  # 'water', 'nutrient', 'pruning', 'pest', 'roof_safety'
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)

    project = relationship("CropProject", back_populates="tasks")


class ProjectLog(Base):
    """Daily user activity or growth observations."""
    __tablename__ = "project_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("crop_projects.id", ondelete="CASCADE"), nullable=False, index=True)
    log_date = Column(Date, default=date.today)
    log_type = Column(String(50), default="observation")  # 'watering', 'fertilizer', 'observation', 'pest', 'harvest'
    note = Column(Text, nullable=False)
    photo_path = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("CropProject", back_populates="logs")


class DiseaseDiagnosis(Base):
    """AI Vision plant disease diagnostic records."""
    __tablename__ = "disease_diagnoses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("crop_projects.id", ondelete="CASCADE"), nullable=True, index=True)
    crop_name = Column(String(100), default="Rooftop Plant")
    image_path = Column(String(255), nullable=False)
    disease_name = Column(String(150), nullable=False)
    confidence = Column(Float, default=0.90)
    severity = Column(String(50), default="Moderate")  # 'Low', 'Moderate', 'High', 'Critical'
    symptoms = Column(Text, nullable=False)
    organic_remedy = Column(Text, nullable=False)
    preventive_measures = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("CropProject", back_populates="diagnoses")
