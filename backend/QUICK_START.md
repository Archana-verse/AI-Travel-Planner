# ⚡ Quick Start Guide - Raahi.ai Free Backend

**Get your AI travel backend running in under 5 minutes!**

## 🚀 Super Quick Setup

### 1. Prerequisites
- Python 3.8+ installed
- Git installed

### 2. One-Command Setup

```bash
# Clone, install, and run in one go!
git clone <your-repo> && cd backend && pip install -r requirements.txt && python run.py
```

### 3. Test It Works

Open: http://localhost:8000/docs

## 🧪 Test the API (Copy & Paste)

### Generate a Trip Plan
```bash
curl -X POST "http://localhost:8000/api/generate-plan" \
  -H "Content-Type: application/json" \
  -d '{
    "from_location": "Delhi",
    "to_location": "Mumbai", 
    "departure_date": "2025-07-20",
    "return_date": "2025-07-23",
    "travel_class": "economy",
    "budget": "comfort",
    "travelers": "couple",
    "interests": ["sightseeing", "food"]
  }'
```

**Copy the `session_id` from the response!**

### Get Flights
```bash
curl "http://localhost:8000/api/flights?session_id=YOUR_SESSION_ID"
```

### Chat with AI
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are the best places to visit in Mumbai?"
  }'
```

### Download PDF
```bash
curl "http://localhost:8000/api/itinerary/YOUR_SESSION_ID/pdf" --output trip.pdf
```

## 🔗 Connect to Frontend

Update your React app's API calls:

```typescript
const API_BASE = "http://localhost:8000/api";

// Generate plan
const response = await fetch(`${API_BASE}/generate-plan`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(preferences)
});
```

## ✅ What You Get (100% Free!)

- ✈️ **Realistic flight data** with real airline pricing
- 🏨 **Smart hotel recommendations** with amenities
- 🤖 **AI-powered itineraries** using rule-based intelligence  
- 💬 **Travel chat assistant** for instant help
- 📄 **PDF generation** for professional itineraries
- 🔗 **Real booking URLs** to airline/hotel websites
- 💾 **Full database persistence** with SQLite

## 🎯 Key Endpoints

| Endpoint | What It Does |
|----------|-------------|
| `POST /api/generate-plan` | Creates complete trip with flights, hotels, itinerary |
| `GET /api/flights?session_id=X` | Gets all flights for a session |
| `GET /api/hotels?session_id=X` | Gets all hotels for a session |
| `POST /api/select-flight` | Selects flight & generates booking URL |
| `POST /api/select-hotel` | Selects hotel & generates booking URL |
| `GET /api/itinerary/{session_id}` | Gets complete itinerary with selections |
| `GET /api/itinerary/{session_id}/pdf` | Downloads PDF itinerary |
| `POST /api/chat` | Chat with AI travel assistant |

## 🐛 Quick Fixes

**Port in use?**
```bash
python run.py --port 8001
```

**Missing modules?**
```bash
pip install -r requirements.txt
```

**Database issues?**
```bash
rm raahi.db && python run.py
```

## 🌐 Deploy for Free

**Heroku:**
```bash
echo "web: python run.py" > Procfile
heroku create your-app && git push heroku main
```

**Railway:** Connect GitHub repo → Auto-deploy

**Render:** Connect repo → Deploy

## 🎉 You're Ready!

Your free AI travel backend is now running with:
- Zero API costs
- Realistic data generation  
- Smart recommendations
- Real booking integration
- Professional PDF output

**Start building amazing travel experiences!** 🚀

---

*Need help? Check the full [TUTORIAL.md](TUTORIAL.md) for detailed explanations.*