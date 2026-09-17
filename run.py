"""Entrypoint script to start the Urban Rooftop Organic Farming Assistant FastAPI Server."""

import sys
from pathlib import Path

# Guarantee the local project directory is first in sys.path
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import uvicorn
from app.config import get_settings


def main():
    """Start the Uvicorn ASGI server."""
    settings = get_settings()
    print("=" * 70)
    print(f"🌱 Starting {settings.app_name}")
    print(f"📡 Serving at: http://127.0.0.1:{settings.port}/")
    print(f"📚 API Docs: http://127.0.0.1:{settings.port}/docs")
    print("=" * 70)

    from app.main import app
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=settings.port,
        log_level="info",
        access_log=True,
    )


if __name__ == "__main__":
    main()
