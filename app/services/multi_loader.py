"""Multi-Source Document Loader for RAG Training: Parses PDFs, Excel/CSV sheets, URLs, and Text."""

import io
import csv
from pathlib import Path
from typing import List, Dict, Any, Union, Optional
import httpx
from bs4 import BeautifulSoup
from pypdf import PdfReader
import openpyxl
from langchain_core.documents import Document
from app.utils.logger import logger


def load_pdf_file(file_path_or_bytes: Union[str, Path, bytes, io.BytesIO], filename: str = "document.pdf") -> List[Document]:
    """Extract text from a PDF file page-by-page with page metadata."""
    logger.info(f"Extracting text from PDF: '{filename}'")
    
    if isinstance(file_path_or_bytes, (str, Path)):
        reader = PdfReader(str(file_path_or_bytes))
    elif isinstance(file_path_or_bytes, bytes):
        reader = PdfReader(io.BytesIO(file_path_or_bytes))
    else:
        reader = PdfReader(file_path_or_bytes)

    docs: List[Document] = []
    total_pages = len(reader.pages)
    title = Path(filename).stem.replace("_", " ").title()

    for idx, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        text = text.strip()
        if not text:
            continue
        
        metadata = {
            "source": filename,
            "title": f"{title} (Page {idx})",
            "document_title": title,
            "page_number": idx,
            "total_pages": total_pages,
            "file_type": "pdf",
        }
        docs.append(Document(page_content=text, metadata=metadata))

    logger.info(f"✓ Extracted {len(docs)} readable pages from PDF '{filename}'.")
    return docs


def load_excel_file(file_path_or_bytes: Union[str, Path, bytes, io.BytesIO], filename: str = "data.xlsx") -> List[Document]:
    """Parse Excel spreadsheets (.xlsx, .xls) and CSVs into structured tabular documents."""
    logger.info(f"Parsing spreadsheet: '{filename}'")
    title = Path(filename).stem.replace("_", " ").title()
    docs: List[Document] = []

    # Handle CSV format
    if filename.lower().endswith(".csv"):
        if isinstance(file_path_or_bytes, (str, Path)):
            with open(file_path_or_bytes, "r", encoding="utf-8", errors="replace") as fh:
                csv_data = fh.read()
        elif isinstance(file_path_or_bytes, bytes):
            csv_data = file_path_or_bytes.decode("utf-8", errors="replace")
        else:
            csv_data = file_path_or_bytes.read().decode("utf-8", errors="replace")

        reader = list(csv.reader(io.StringIO(csv_data)))
        if not reader:
            return []
        
        headers = [h.strip() for h in reader[0]]
        rows_text = []
        for row_idx, row in enumerate(reader[1:], start=2):
            row_dict = {headers[i]: row[i].strip() for i in range(min(len(headers), len(row)))}
            row_str = " | ".join([f"{k}: {v}" for k, v in row_dict.items() if v])
            if row_str:
                rows_text.append(f"Row {row_idx}: {row_str}")

        if rows_text:
            docs.append(
                Document(
                    page_content=f"Dataset: {title}\n" + "\n".join(rows_text),
                    metadata={"source": filename, "title": title, "file_type": "csv"},
                )
            )
        return docs

    # Handle Excel format (.xlsx, .xls)
    if isinstance(file_path_or_bytes, (str, Path)):
        wb = openpyxl.load_workbook(str(file_path_or_bytes), data_only=True)
    elif isinstance(file_path_or_bytes, bytes):
        wb = openpyxl.load_workbook(io.BytesIO(file_path_or_bytes), data_only=True)
    else:
        wb = openpyxl.load_workbook(file_path_or_bytes, data_only=True)

    for sheet_name in wb.sheetnames:
        sheet = wb[sheet_name]
        rows = list(sheet.iter_rows(values_only=True))
        if not rows:
            continue

        header_row = [str(c).strip() if c is not None else f"Column_{i+1}" for i, c in enumerate(rows[0])]
        sheet_rows = []

        for row_idx, row in enumerate(rows[1:], start=2):
            cells = [f"{header_row[i]}: {str(v).strip()}" for i, v in enumerate(row) if v is not None and str(v).strip()]
            if cells:
                sheet_rows.append(f"Row {row_idx}: " + " | ".join(cells))

        if sheet_rows:
            chunk_size = 25
            for i in range(0, len(sheet_rows), chunk_size):
                chunk = sheet_rows[i : i + chunk_size]
                content = f"Workbook: {title} | Sheet: {sheet_name} (Rows {i+2} to {i+len(chunk)+1})\n" + "\n".join(chunk)
                docs.append(
                    Document(
                        page_content=content,
                        metadata={
                            "source": filename,
                            "title": f"{title} - {sheet_name}",
                            "sheet_name": sheet_name,
                            "file_type": "excel",
                        },
                    )
                )

    logger.info(f"✓ Parsed {len(docs)} structured chunks from spreadsheet '{filename}'.")
    return docs


async def load_url_page(url: str) -> List[Document]:
    """Scrape and clean readable article text from a public website URL."""
    logger.info(f"Scraping website URL: '{url}'")

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36 UrbanRooftopRAG/1.0"
        )
    }

    async with httpx.AsyncClient(timeout=25.0, follow_redirects=True) as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        html = response.text

    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "nav", "footer", "header", "noscript", "aside", "form"]):
        tag.decompose()

    title = soup.title.string.strip() if soup.title and soup.title.string else url

    text_blocks = []
    for el in soup.find_all(["h1", "h2", "h3", "h4", "p", "li", "table"]):
        txt = el.get_text(separator=" ", strip=True)
        if len(txt) > 20:
            text_blocks.append(txt)

    combined_text = "\n\n".join(text_blocks)
    if not combined_text.strip():
        combined_text = soup.get_text(separator="\n", strip=True)

    if not combined_text.strip():
        raise ValueError(f"No readable content could be extracted from {url}")

    logger.info(f"✓ Scraped URL '{url}' ({len(combined_text)} characters) - '{title}'")

    return [
        Document(
            page_content=combined_text,
            metadata={
                "source": url,
                "title": title[:100],
                "file_type": "url",
                "url": url,
            },
        )
    ]
