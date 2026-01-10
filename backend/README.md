# IAFA Backend - POC Version

FastAPI backend for Inspiration-to-Action Funnel Analyzer (POC - No Authentication Required).

## Setup

1. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Create data directories**:
```bash
mkdir -p data/{events,metadata,config}
```

5. **Run development server**:
```bash
uvicorn app.main:app --reload --port 8000
```

## Docker

```bash
docker-compose up --build
```

## API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation.

**Note**: This is a POC version - no authentication required. All endpoints work without login.

## Project Structure

```
backend/
├── app/
│   ├── api/v1/          # API endpoints
│   ├── core/            # Core configuration and security
│   ├── services/        # Business logic services
│   ├── storage/         # Parquet and metadata handlers
│   └── main.py          # FastAPI application
├── data/                # Data directory (not in git)
├── tests/               # Test files
├── requirements.txt     # Python dependencies
└── Dockerfile           # Docker configuration
```
