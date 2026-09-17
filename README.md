# 🌱 Urban Rooftop Organic Farming Assistant (RAG Backend)

A production-ready Retrieval-Augmented Generation (RAG) backend application designed specifically for **Urban Rooftop & Terrace Organic Agriculture**.

The system provides verified, grounded, and structurally safe agronomic advice—combining **FastAPI**, **LangChain (LCEL)**, **Pinecone Serverless Vector Database**, and **Google Gemini API (`gemini-2.0-flash` & `models/text-embedding-004`)**.

---

## 🏗️ Architecture Overview

```
                                  ┌────────────────────────┐
                                  │   Curated Knowledge    │
                                  │   Base (.md Files)     │
                                  └───────────┬────────────┘
                                              │ Ingestion Pipeline
                                              ▼
┌─────────────────┐               ┌────────────────────────┐
│  User / Client  │               │ Recursive Character    │
│  (cURL/Web/App) │               │ Text Splitter          │
└────────┬────────┘               └───────────┬────────────┘
         │                                    │
         │ POST /ask                          ▼
         ▼                        ┌────────────────────────┐
┌─────────────────┐               │ Gemini text-embedding  │
│  FastAPI Router │               │ -004 (768-dim)         │
└────────┬────────┘               └───────────┬────────────┘
         │                                    │
         │ LangChain LCEL                     ▼
         ▼                        ┌────────────────────────┐
┌─────────────────┐  Embed Query  │   Pinecone Serverless  │
│  RAG Pipeline   ├──────────────►│   Vector Database      │
│  Orchestration  │◄──────────────┤   (k=3 Similarity)     │
└────────┬────────┘  Top-3 Chunks └────────────────────────┘
         │
         │ Agronomy Safety Prompt + Context
         ▼
┌────────────────────────┐
│ Google Gemini 2.0      │
│ Flash LLM Generation   │
└────────┬───────────────┘
         │
         ▼
┌────────────────────────┐
│ Verified JSON Response │
│ with Source Citations  │
└────────────────────────┘
```

---

## 🌿 Curated Domain Knowledge Base

The system comes pre-loaded with curated, expert agronomic documentation in the `/data` directory:

1. **Structural Load & Lightweight Mixes (`01_structural_load_and_potting_mix.md`)**:
   - Residential slab live load capacity (150–200 kg/m² / 30–40 lbs/sq ft).
   - Warnings on wet garden soil (1,800–2,200 kg/m³).
   - 3:1:1 lightweight organic potting formula (Cocopeat + Vermicompost + Perlite/Pumice, density 450–600 kg/m³).
   - Load distribution over columns and load-bearing beams.
2. **Waterproofing, Drainage & Root Protection (`02_waterproofing_and_drainage.md`)**:
   - Polyurethane/EPDM waterproofing membranes.
   - HDPE anti-root penetration barriers (1.0–1.5mm).
   - Polypropylene drainage cells (20–30mm) + Non-woven Geotextile filter fabric (120–150 GSM).
   - Raised pot stands (2–4 inches) for air-pruning and terrace floor inspection.
3. **Organic Pest & Fungal Control (`03_organic_pest_and_fungal_control.md`)**:
   - Cold-pressed Neem oil spray formulation (5ml neem + 2ml potassium castile soap per liter).
   - Fermented sour buttermilk (1:10 dilution) against powdery mildew, downy mildew, and blights.
   - Chromatic yellow/blue sticky traps and pheromone traps.
   - Absolute ban on synthetic chemical pesticides (chlorpyrifos, imidacloprid).
4. **Soil Nutrition & Bio-Fertilizers (`04_soil_nutrition_and_biofertilizers.md`)**:
   - Liquid Jeevamrut biostimulant formulation & fermentation protocol.
   - Vermiwash foliar tonics.
   - Targeted bio-fertilizers (*Azotobacter*, *Rhizobium*, PSB *Bacillus megaterium*, KMB, Mycorrhiza/VAM).
   - Enriched vermicompost, neem cake powder, rock phosphate, and wood ash top-dressing.
5. **Microclimates, Containers & Companion Planting (`05_microclimate_containers_and_companion_planting.md`)**:
   - UV-stabilized HDPE grow bags (200–240 GSM) and Sub-Irrigated Planters (SIP).
   - 50% UV-stabilized agro-shade nets (temperatures reduced by 4–6°C).
   - Living and porous windbreaks for high rooftop wind speeds.
   - Symbiotic guilds (Tomato + Basil + Marigold; Urban Three Sisters; Borage + Strawberries).

---

## 🚀 Tech Stack

- **Framework**: FastAPI with Uvicorn
- **Orchestration**: LangChain Expression Language (LCEL)
- **Vector Database**: Pinecone Serverless (AWS `us-east-1`, 768 dimensions, cosine similarity)
- **LLM**: Google Gemini (`gemini-2.0-flash`)
- **Embeddings**: Google Gemini (`models/text-embedding-004`)
- **Validation**: Pydantic v2 & Pydantic Settings
- **Configuration**: python-dotenv

---

## 📁 Project Structure

```
orliv/
├── app/
│   ├── __init__.py
│   ├── config.py                 # Pydantic Settings for environment variables
│   ├── schemas.py                # Pydantic Request & Response models
│   ├── main.py                   # FastAPI app, lifespan, endpoints, error handlers
│   ├── services/
│   │   ├── __init__.py
│   │   ├── embeddings.py         # Google Gemini Embeddings (text-embedding-004)
│   │   ├── vector_store.py       # Pinecone Serverless connection & auto-provisioning
│   │   ├── rag_chain.py          # LCEL RAG pipeline with custom Agronomy prompt
│   │   └── ingestion.py          # Document loader, Recursive splitter & Pinecone upsert
│   └── utils/
│       ├── __init__.py
│       └── logger.py             # Structured logger
├── data/                         # Markdown Knowledge Base documents
│   ├── 01_structural_load_and_potting_mix.md
│   ├── 02_waterproofing_and_drainage.md
│   ├── 03_organic_pest_and_fungal_control.md
│   ├── 04_soil_nutrition_and_biofertilizers.md
│   └── 05_microclimate_containers_and_companion_planting.md
├── scripts/
│   ├── ingest.py                 # Standalone CLI ingestion script
│   └── query_cli.py              # Terminal interactive query tool
├── tests/
│   ├── __init__.py
│   └── test_api.py               # Unit & integration test suite
├── .env.example                  # Environment variable template
├── .env                          # Local environment configuration
├── requirements.txt              # Production Python dependencies
└── README.md                     # Comprehensive documentation
```

---

## ⚙️ Installation & Setup

### 1. Prerequisites
- Python 3.10+
- Google Gemini API Key ([Get one here](https://aistudio.google.com/))
- Pinecone API Key ([Get one here](https://app.pinecone.io/))

### 2. Clone and Setup Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Edit the `.env` file (copied from `.env.example`):

```env
# Google Gemini API
GOOGLE_API_KEY=AIzaSy...your_gemini_api_key_here
GEMINI_MODEL=gemini-2.0-flash
EMBEDDING_MODEL=models/text-embedding-004

# Pinecone Vector Database
PINECONE_API_KEY=pcsk_...your_pinecone_api_key_here
PINECONE_INDEX_NAME=urban-rooftop-farming
PINECONE_CLOUD=aws
PINECONE_REGION=us-east-1
PINECONE_DIMENSION=768
PINECONE_METRIC=cosine

# Application Settings
APP_NAME="Urban Rooftop Organic Farming RAG Assistant"
APP_ENV=development
DEBUG=true
PORT=8000
HOST=0.0.0.0

# Retrieval & Ingestion Settings
TOP_K_RETRIEVAL=3
CHUNK_SIZE=600
CHUNK_OVERLAP=100
```

---

## 📥 Ingestion Pipeline

You can ingest the curated knowledge base into Pinecone via either the CLI script or the API endpoint. The system will **automatically provision the Serverless Pinecone index** if it doesn't already exist.

### Method A: Via CLI Script
```bash
python scripts/ingest.py
```

### Method B: Via API Endpoint
```bash
curl -X POST http://localhost:8000/ingest
```

---

## 🖥️ Running the Server

Start the FastAPI application with Uvicorn:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Interactive Swagger API Documentation is available at:
👉 **`http://localhost:8000/docs`**

Alternative ReDoc Documentation:
👉 **`http://localhost:8000/redoc`**

---

## 🧪 Testing via cURL

### 1. Health Check Endpoint (`GET /health`)
Check service status, Pinecone connectivity, and Gemini model availability:

```bash
curl -X GET "http://localhost:8000/health" \
  -H "Accept: application/json"
```

**Example Response:**
```json
{
  "status": "healthy",
  "app_name": "Urban Rooftop Organic Farming RAG Assistant",
  "version": "1.0.0",
  "timestamp": "2026-08-19T11:15:30.123456Z",
  "services": {
    "gemini_llm": {
      "status": "configured",
      "model": "gemini-2.0-flash",
      "embedding_model": "models/text-embedding-004"
    },
    "pinecone": {
      "status": "connected",
      "index_name": "urban-rooftop-farming",
      "dimension": 768,
      "vector_stats": {
        "total_vector_count": 28,
        "dimension": 768,
        "index_fullness": 0.0,
        "namespaces": {}
      }
    }
  }
}
```

---

### 2. Query 1: Structural Roof Load & Potting Mix

```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the recommended lightweight potting mix formula to prevent roof overload?",
    "top_k": 3,
    "include_sources": true
  }'
```

---

### 3. Query 2: Organic Pest & Fungal Control

```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "How do I prepare and apply fermented buttermilk and neem oil for powdery mildew on terrace tomatoes?",
    "top_k": 3,
    "include_sources": true
  }'
```

---

### 4. Query 3: Liquid Jeevamrut Soil Nutrition

```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the recipe for preparing liquid Jeevamrut, and how should it be applied to container plants?",
    "top_k": 3,
    "include_sources": true
  }'
```

---

### 5. Query 4: Waterproofing & Raised Stands

```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Why shouldn'\''t grow bags rest directly on terrace tiles, and what drainage system should be used?",
    "top_k": 3,
    "include_sources": true
  }'
```

---

### 6. Query 5: Microclimate, Winds & Companion Guilds

```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What agro-shade net specification is best for rooftop summer heat, and what companion plants protect tomatoes?",
    "top_k": 3,
    "include_sources": true
  }'
```

---

### 7. Interactive Terminal CLI
You can also ask questions interactively inside your terminal:

```bash
python scripts/query_cli.py
```

---

## 🧪 Running Automated Tests

Run unit and integration tests using `pytest`:

```bash
pytest tests/ -v
```

---

## 🛡️ Error Handling & Resilience

| Scenario | HTTP Status | Description |
| :--- | :--- | :--- |
| **Missing / Placeholder API Keys** | `401 Unauthorized` | Clear prompt specifying missing `GOOGLE_API_KEY` or `PINECONE_API_KEY`. |
| **Invalid Question Payload** | `422 Unprocessable` | Pydantic validation rejects empty, whitespace, or excessively long prompts. |
| **Gemini Quota / Rate Limit** | `429 Too Many Requests` | Handled gracefully with retry advisory. |
| **Pinecone Network / Timeout** | `504 Gateway Timeout` | Vector search timeout protection with structured error JSON. |
| **Index Provisioning** | Auto-managed | Serverless index is provisioned automatically with cosine distance. |

---

## 📄 License
MIT License. Built for Sustainable Urban Agriculture.
