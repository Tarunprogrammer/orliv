"""Multi-Dialect Database Engine: Supports Local MySQL with automated DB creation and graceful SQLite fallback."""

import os
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from app.config import get_settings
from app.utils.logger import logger

DB_DIR = Path(__file__).resolve().parent.parent / "data"
DB_DIR.mkdir(parents=True, exist_ok=True)
UPLOADS_DIR = DB_DIR / "uploads"
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

SQLITE_DB_PATH = DB_DIR / "rooftop_farming.db"
SQLITE_DATABASE_URL = f"sqlite:///{SQLITE_DB_PATH}"

Base = declarative_base()

_engine = None
_SessionLocal = None
_active_dialect = "sqlite"


def create_db_engine():
    """Create and return the active SQLAlchemy engine (MySQL or SQLite fallback)."""
    global _engine, _SessionLocal, _active_dialect
    settings = get_settings()
    requested_dialect = settings.db_dialect.lower()

    if requested_dialect == "mysql":
        user = settings.mysql_user
        password = settings.mysql_password or ""
        host = settings.mysql_host
        port = settings.mysql_port
        dbname = settings.mysql_database

        # Build connection URLs
        pw_str = f":{password}" if password else ""
        server_url = f"mysql+pymysql://{user}{pw_str}@{host}:{port}"
        mysql_url = f"{server_url}/{dbname}?charset=utf8mb4"

        try:
            logger.info(f"Attempting to connect to local MySQL server at {host}:{port}...")
            # Step 1: Connect to server and create database if not exists
            server_engine = create_engine(server_url, connect_args={"connect_timeout": 3})
            with server_engine.connect() as conn:
                conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{dbname}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
                conn.commit()
            server_engine.dispose()

            # Step 2: Create primary MySQL engine
            _engine = create_engine(
                mysql_url,
                pool_pre_ping=True,
                pool_recycle=3600,
                connect_args={"connect_timeout": 5},
                echo=False,
            )
            # Test connection
            with _engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            _active_dialect = "mysql"
            logger.info(f"✓ Successfully connected to local MySQL database: '{dbname}' on {host}:{port}")
        except Exception as e:
            logger.warning(
                f"⚠️ Could not connect to local MySQL server ({e}). "
                f"Falling back gracefully to local SQLite database at '{SQLITE_DB_PATH}'."
            )
            _engine = create_engine(
                SQLITE_DATABASE_URL,
                connect_args={"check_same_thread": False},
                echo=False,
            )
            _active_dialect = "sqlite"
    else:
        logger.info(f"Using SQLite database dialect at: '{SQLITE_DB_PATH}'")
        _engine = create_engine(
            SQLITE_DATABASE_URL,
            connect_args={"check_same_thread": False},
            echo=False,
        )
        _active_dialect = "sqlite"

    _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)
    return _engine


# Initialize engine
engine = create_db_engine()
SessionLocal = _SessionLocal


def get_db_dialect() -> str:
    """Return active database dialect ('mysql' or 'sqlite')."""
    return _active_dialect


def get_db() -> Session:
    """FastAPI Dependency for database sessions."""
    global _SessionLocal
    if _SessionLocal is None:
        create_db_engine()
    db = _SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all database tables on startup if they do not exist."""
    global _engine
    import app.models  # Ensure models are imported
    if _engine is None:
        create_db_engine()
    logger.info(f"Creating/verifying tables for active dialect: '{_active_dialect}'")
    Base.metadata.create_all(bind=_engine)
    logger.info(f"✓ Database tables initialized successfully ({_active_dialect}).")
