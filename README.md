# Inspiration-to-Action Funnel Analyzer (IAFA)

**A Pinterest-inspired analytics tool for Product Data Scientists to measure inspiration-to-action journeys**

---

## 🎯 What is IAFA?

IAFA helps Product Data Scientists analyze multi-stage user journeys from inspiration to action, with segment-aware analytics and leadership-ready reporting.

### Key Features
- 📊 **Journey Analytics**: Stage-by-stage progression analysis
- 🎯 **Segment Analysis**: Break down by user intent, tenure, surface, content category
- 📈 **Visual Charts**: Interactive bar charts for journey and segment comparison
- 📄 **Report Export**: Generate HTML, CSV, or Text reports for leadership
- 🔍 **Multi-Stage Tracking**: Analyze complex user journeys (up to 5 stages)
- 💡 **Pinterest-Themed UI**: Clean, professional interface

---

## 🚀 Quick Start

### Local Setup (5 minutes)

**Prerequisites**: Python 3.11+, Node.js 18+

```bash
# 1. Clone repository
git clone https://github.com/lokesh75-kank/Inspiration-to-Action-Funnel-Analyzer-IAFA-.git
cd "Inspiration-to-Action-Funnel-Analyzer-IAFA-"

# 2. Setup Backend
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python populate_sample_data.py
uvicorn app.main:app --reload --port 8000

# 3. Setup Frontend (new terminal)
cd frontend
npm install
npm run dev
```

**Open browser**: `http://localhost:5173` ✨

📖 **Full Setup Instructions**: See [QUICK_START.md](./QUICK_START.md)

---

## ☁️ Free Cloud Deployment

Deploy for free and share with others:

- **Render.com** (Recommended): See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)
- **Railway.app**: See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)
- **Vercel + Railway**: See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)

All options include free tiers perfect for demos and portfolios!

---

## 📚 Documentation

- **Quick Start**: [QUICK_START.md](./QUICK_START.md) - Get running in 5 minutes
- **Deployment Guide**: [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) - Deploy to cloud for free
- **User Guide**: [documents/05-product/USER_GUIDE.md](./documents/05-product/USER_GUIDE.md) - Complete user documentation
- **Demo Guide**: [LIVE_DEMO_GUIDE.md](./LIVE_DEMO_GUIDE.md) - Step-by-step demo script
- **GenAI Strategy**: [documents/06-genai/GENAI_RECOMMENDATIONS_STRATEGY.md](./documents/06-genai/GENAI_RECOMMENDATIONS_STRATEGY.md) - AI-powered recommendations (future)

---

## 🎯 Use Cases

### For Product Data Scientists
- Analyze user journey progression rates
- Compare segment performance (Planner vs Actor, New vs Retained)
- Identify drop-off points and optimization opportunities
- Generate leadership-ready reports

### For Leadership
- Executive dashboard view
- Export reports for presentations
- Segment-aware insights
- Data-driven decision making

---

## 🏗️ Architecture

- **Backend**: FastAPI (Python) with DuckDB + Parquet for analytics
- **Frontend**: React + TypeScript + Vite
- **Charts**: Recharts
- **Storage**: Parquet files (columnar format) for efficient analytics
- **Styling**: Tailwind CSS with Pinterest theme

---

## 📦 Project Structure

```
.
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/v1/      # API endpoints
│   │   ├── services/    # Business logic
│   │   ├── storage/     # Data storage (Parquet, DuckDB)
│   │   └── main.py      # FastAPI app
│   └── populate_sample_data.py  # Pre-populate demo data
│
├── frontend/            # React frontend
│   ├── src/
│   │   ├── components/  # UI components
│   │   ├── pages/       # Page components
│   │   ├── services/    # API clients
│   │   └── utils/       # Utilities (report generator)
│   └── package.json
│
└── documents/           # Documentation
    ├── 05-product/      # User guides
    └── 06-genai/        # GenAI strategy
```

---

## 🎨 Features in Detail

### Journey Analytics
- Multi-stage funnel visualization
- Conversion rate calculation
- Drop-off analysis
- Date range filtering

### Segment Analysis
- Filter by: User Intent, User Tenure, Surface, Content Category
- Break down by: Any segment dimension
- Segment comparison tables and charts
- Side-by-side segment performance

### Visualizations
- Journey performance bar charts
- Segment comparison charts
- Interactive tooltips
- Pinterest-themed styling

### Report Export
- **HTML**: Formatted report with styling (best for sharing)
- **CSV**: Data for Excel/Google Sheets analysis
- **Text**: Plain text format
- Automatic insights generation
- Executive summary included

---

## 🔧 Development

### Backend
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

API docs available at: `http://localhost:8000/docs`

### Frontend
```bash
cd frontend
npm run dev
```

Development server: `http://localhost:5173`

### Pre-populate Data
```bash
cd backend
python populate_sample_data.py
```

This creates sample events for:
- `pin_view`, `save`, `click`, `purchase` events
- Planner and Actor user segments
- New and Retained user tenure
- Various content categories

---

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend (run in frontend directory)
npm test
```

---

## 📄 License

See [LICENSE](./LICENSE) file

---

## 🤝 Contributing

This is a POC project for a Pinterest Data Scientist position. Contributions welcome!

---

## 🙏 Acknowledgments

- Inspired by Pinterest's inspiration-to-action framework
- Built for Product Data Scientists
- Designed for decision-making and experimentation

---

## 📞 Support

- **Issues**: Open an issue on GitHub
- **Documentation**: See `/documents` folder
- **Quick Help**: See [QUICK_START.md](./QUICK_START.md)

---

**Built with ❤️ for Product Data Scientists**
