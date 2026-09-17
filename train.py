"""Developer CLI Tool: Train, Reset, or Delete Data from RAG Vector Database."""

import sys
import time
import asyncio
import argparse
from pathlib import Path
from typing import List

# Ensure project root is first in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from langchain_core.documents import Document

from app.config import get_settings
from app.services.vector_store import (
    get_pinecone_client,
    get_vector_store,
    ensure_pinecone_index,
)
from app.services.multi_loader import (
    load_pdf_file,
    load_excel_file,
    load_url_page,
)
from app.services.ingestion import ingest_raw_documents

console = Console()


def clear_vector_store():
    """Wipe all vector embeddings from the Pinecone index."""
    settings = get_settings()
    backend = settings.vector_store_backend.lower()

    if backend in ("ram", "memory", "in_memory"):
        console.print("[bold yellow]🧹 Clearing In-Memory RAM vector store...[/bold yellow]")
        vector_store = get_vector_store()
        if hasattr(vector_store, "clear"):
            vector_store.clear()
        console.print("[bold green]✓ RAM store cleared successfully.[/bold green]")
        return

    console.print(f"[bold yellow]🧹 Clearing all vectors from Pinecone index '{settings.pinecone_index_name}'...[/bold yellow]")
    pc = get_pinecone_client()
    try:
        index = pc.Index(settings.pinecone_index_name)
        index.delete(delete_all=True)
        console.print("[bold green]✓ All vectors deleted from Pinecone index successfully![/bold green]")
    except Exception as e:
        console.print(f"[bold red]❌ Failed to clear Pinecone vectors: {e}[/bold red]")


def delete_source_from_pinecone(source_name: str):
    """Delete all vectors matching a specific document source or filename."""
    settings = get_settings()
    backend = settings.vector_store_backend.lower()

    console.print(f"[bold yellow]🗑️ Deleting data for source: '{source_name}'...[/bold yellow]")
    pc = get_pinecone_client()
    try:
        index = pc.Index(settings.pinecone_index_name)
        index.delete(filter={"source": {"$eq": source_name}})
        console.print(f"[bold green]✓ Deleted all vectors associated with '{source_name}' from Pinecone![/bold green]")
    except Exception as e:
        console.print(f"[bold red]❌ Failed to delete source '{source_name}': {e}[/bold red]")


async def train_rag_pipeline(reset: bool = False):
    """Scan /data directory for raw documents and train the RAG vector store."""
    if reset:
        clear_vector_store()
        console.print("[bold cyan]🔄 Performing fresh full re-training...[/bold cyan]\n")

    console.print(
        Panel(
            "[bold green]🌱 Urban Rooftop Farming RAG Model Training Tool[/bold green]\n"
            "[dim]Scans all raw PDFs, Excel spreadsheets, CSVs, Markdown notes, and Web URLs in /data[/dim]",
            border_style="green",
        )
    )

    settings = get_settings()
    data_dir = PROJECT_ROOT / "data"

    if not data_dir.exists():
        console.print(f"[bold red]❌ Data directory '{data_dir}' does not exist.[/bold red]")
        return

    all_raw_docs: List[Document] = []
    scanned_items = []

    # 1. Load Markdown & Text guides (.md, .txt)
    md_files = sorted(list(data_dir.glob("*.md")) + [f for f in data_dir.glob("*.txt") if f.name != "urls.txt"])
    for f in md_files:
        try:
            with open(f, "r", encoding="utf-8", errors="replace") as fh:
                content = fh.read().strip()
            title = f.stem.replace("_", " ").title()
            for line in content.splitlines():
                if line.startswith("# "):
                    title = line.replace("# ", "").strip()
                    break
            doc = Document(
                page_content=content,
                metadata={"source": f.name, "title": title, "file_type": f.suffix.lstrip(".")},
            )
            all_raw_docs.append(doc)
            scanned_items.append((f.name, f.suffix.upper().lstrip("."), f"{len(content)} chars", "[green]✓ Ready[/green]"))
        except Exception as e:
            scanned_items.append((f.name, f.suffix.upper().lstrip("."), "Error", f"[red]❌ {e}[/red]"))

    # 2. Load PDF files (.pdf)
    pdf_files = sorted(list(data_dir.glob("*.pdf")))
    for f in pdf_files:
        try:
            docs = load_pdf_file(f, filename=f.name)
            all_raw_docs.extend(docs)
            scanned_items.append((f.name, "PDF", f"{len(docs)} pages", "[green]✓ Ready[/green]"))
        except Exception as e:
            scanned_items.append((f.name, "PDF", "Error", f"[red]❌ {e}[/red]"))

    # 3. Load Excel & CSV spreadsheets (.xlsx, .xls, .csv)
    excel_files = sorted(list(data_dir.glob("*.xlsx")) + list(data_dir.glob("*.xls")) + list(data_dir.glob("*.csv")))
    for f in excel_files:
        try:
            docs = load_excel_file(f, filename=f.name)
            all_raw_docs.extend(docs)
            scanned_items.append((f.name, "SPREADSHEET", f"{len(docs)} chunks", "[green]✓ Ready[/green]"))
        except Exception as e:
            scanned_items.append((f.name, "SPREADSHEET", "Error", f"[red]❌ {e}[/red]"))

    # 4. Load Website URLs from urls.txt
    urls_file = data_dir / "urls.txt"
    if urls_file.exists():
        with open(urls_file, "r", encoding="utf-8") as fh:
            urls = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

        for url in urls:
            try:
                console.print(f"[dim]🌐 Fetching & scraping web guide: {url}...[/dim]")
                url_docs = await load_url_page(url)
                all_raw_docs.extend(url_docs)
                title = url_docs[0].metadata.get("title", url)[:38] if url_docs else url
                scanned_items.append((title, "WEB URL", f"{len(url_docs)} docs", "[green]✓ Scraped[/green]"))
            except Exception as e:
                scanned_items.append((url[:38], "WEB URL", "Error", f"[red]❌ {e}[/red]"))

    # Summary table
    table = Table(title="Discovered Raw Data Sources in /data", border_style="dim")
    table.add_column("File / Source Name", style="cyan")
    table.add_column("Type", style="magenta")
    table.add_column("Size / Count", style="yellow")
    table.add_column("Scan Status", style="green")

    for row in scanned_items:
        table.add_row(*row)
    console.print(table)

    if not all_raw_docs:
        console.print("[bold yellow]⚠️ No documents found to index.[/bold yellow]")
        return

    console.print(f"\n[bold green]🚀 Training & Embedding {len(all_raw_docs)} source documents into Pinecone...[/bold green]")
    result = ingest_raw_documents(all_raw_docs, source_name="Full Data Directory Training")

    # Output Results Table
    res_table = Table(title="RAG Model Training Results", border_style="green")
    res_table.add_column("Parameter", style="bold white")
    res_table.add_column("Value", style="bold green")

    res_table.add_row("Training Status", result["status"].upper())
    res_table.add_row("Raw Documents Processed", str(result["documents_processed"]))
    res_table.add_row("Semantic Chunks Created", str(result["chunks_created"]))
    res_table.add_row("Vectors Upserted", str(result["vectors_upserted"]))
    res_table.add_row("Pinecone Index Target", result["index_name"])
    res_table.add_row("Vector Dimension", str(result["dimension"]))
    res_table.add_row("Total Training Time", f"{result['duration_seconds']}s")

    console.print(res_table)
    console.print(
        Panel(
            "[bold green]✨ RAG Training Complete![/bold green]\n"
            "Your model is now updated with all active materials.\n"
            "Start the app with [cyan]python run.py[/cyan] and open [underline cyan]http://localhost:8080/[/underline cyan]",
            border_style="green",
        )
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Urban Rooftop RAG Training & Data Management CLI")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Wipe all existing vector embeddings and re-train fresh from /data directory",
    )
    parser.add_argument(
        "--clear",
        action="store_true",
        help="Wipe all vector data from the database without re-training",
    )
    parser.add_argument(
        "--delete",
        type=str,
        default=None,
        help="Delete vectors for a specific file or URL source (e.g., --delete crop_guide.pdf)",
    )

    args = parser.parse_args()

    if args.clear:
        clear_vector_store()
    elif args.delete:
        delete_source_from_pinecone(args.delete)
    else:
        asyncio.run(train_rag_pipeline(reset=args.reset))
