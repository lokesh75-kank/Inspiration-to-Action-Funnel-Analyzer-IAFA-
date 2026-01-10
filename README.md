# IAFA - Inspiration-to-Action Funnel Analyzer

**🎯 Complete User Guide**: See [USER_GUIDE.md](./USER_GUIDE.md) for step-by-step instructions on how to use the tool.

--- (POC)

**Proof of Concept** for data science demonstration - Parquet-based funnel analytics.

**Note**: This is a POC for localhost only. No authentication required. Perfect for demonstrating data science capabilities.

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose (optional)

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
# No .env needed for POC - uses defaults
mkdir -p data/{events,metadata,config}
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup (Optional)

```bash
cd frontend
npm install
# VITE_API_URL defaults to http://localhost:8000/api/v1
npm run dev
```

**Note**: For POC, you can use the API directly at http://localhost:8000/docs without frontend.

### Docker Setup

```bash
docker-compose up --build
```

## 📚 Documentation

See [documents/README.md](./documents/README.md) for complete documentation.

- **Business**: [Product Vision](./documents/01-business/01-Product-Vision-Strategy.md)
- **Data Science**: [Data Strategy](./documents/02-data-science/01-Data-Strategy-Architecture.md)
- **Development**: [Technical Implementation Plan](./documents/03-development/IAFA_Technical_Implementation_Plan_MVP.md)

## 🏗️ Project Structure

```
.
├── backend/           # FastAPI backend
│   ├── app/          # Application code
│   ├── data/         # Parquet files and metadata
│   └── tests/        # Test files
├── frontend/         # React frontend
│   ├── src/          # Source code
│   └── public/       # Static files
├── documents/        # Documentation
└── docker-compose.yml
```

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 📝 License

MIT
