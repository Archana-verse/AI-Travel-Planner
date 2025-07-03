# 🚀 Complete Tutorial: Free Raahi.ai Backend

**Build a production-grade AI travel planner backend with ZERO costs!**

## 📋 Table of Contents

1. [What You'll Build](#what-youll-build)
2. [Prerequisites](#prerequisites)
3. [Quick Start (5 Minutes)](#quick-start-5-minutes)
4. [Understanding the Architecture](#understanding-the-architecture)
5. [Testing the API](#testing-the-api)
6. [Connecting to Frontend](#connecting-to-frontend)
7. [Customization Guide](#customization-guide)
8. [Deployment Options](#deployment-options)
9. [Troubleshooting](#troubleshooting)

## 🎯 What You'll Build

A complete travel planning backend that:
- ✅ Generates realistic flight and hotel data
- ✅ Creates intelligent itineraries using rule-based AI
- ✅ Provides travel chat assistance
- ✅ Generates booking URLs for real airline/hotel websites
- ✅ Creates downloadable PDF itineraries
- ✅ Stores everything in SQLite database
- ✅ **Costs absolutely NOTHING to run!**

## 📚 Prerequisites

### Required (Free)
- **Python 3.8+** - [Download here](https://python.org/downloads)
- **Git** - [Download here](https://git-scm.com/downloads)
- **Text Editor** - VS Code, PyCharm, or any editor

### Optional (Free)
- **Postman** - For API testing
- **Docker** - For containerized deployment

## 🚀 Quick Start (5 Minutes)

### Step 1: Clone & Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

**That's it!** No API keys, no configuration needed.

### Step 3: Run the Server

```bash
python run.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
```

### Step 4: Test It Works

Open your browser and go to:
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

🎉 **Congratulations!** Your free AI travel backend is running!

## 🏗️ Understanding the Architecture

### Project Structure
```
backend/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Settings (no API keys needed!)
│   ├── models.py            # Database models
│   ├── schemas.py           # API request/response models
│   ├── database.py          # SQLite database setup
│   ├── routers/             # API endpoints
│   │   ├── planning.py      # Main trip planning
│   │   ├── flights.py       # Flight data
│   │   ├── hotels.py        # Hotel data
│   │   ├── itinerary.py     # Itinerary & PDF
│   │   ├── chat.py          # AI chat assistant
│   │   └── booking.py       # Flight/hotel selection
│   └── services/            # Business logic
│       ├── free_data_service.py    # Realistic data generation
│       ├── free_ai_service.py      # Rule-based AI
│       ├── booking_service.py      # Real booking URLs
│       └── pdf_service.py          # PDF generation
├── requirements.txt         # Dependencies (all free!)
├── run.py                  # Server startup
└── .env.example            # Environment template
```

### How It Works (No Paid APIs!)

#### 1. **Realistic Data Generation**
```python
# In free_data_service.py
async def search_flights(self, origin, destination, departure_date):
    # Generates realistic flights using:
    # - Real airline data (IndiGo, Air India, etc.)
    # - Distance-based pricing
    # - Authentic flight schedules
    # - Market-accurate costs
```

#### 2. **Rule-Based AI Intelligence**
```python
# In free_ai_service.py
async def analyze_flight_recommendations(self, flights, preferences):
    # Smart recommendations based on:
    # - Budget compatibility
    # - Airline reputation
    # - Flight timing analysis
    # - Duration optimization
```

#### 3. **Real Booking Integration**
```python
# In booking_service.py
def generate_flight_booking_url(self, flight_data, departure_date):
    # Creates real URLs like:
    # https://www.goindigo.in/booking/flight-select?from=DEL&to=BOM&departure=2025-07-20
```

## 🧪 Testing the API

### Method 1: Using the Interactive Docs

1. Go to http://localhost:8000/docs
2. Click on any endpoint to expand it
3. Click "Try it out"
4. Fill in the parameters
5. Click "Execute"

### Method 2: Using curl Commands

#### Generate a Complete Travel Plan
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
    "interests": ["sightseeing", "food"],
    "diet": "vegetarian"
  }'
```

**Response**: You'll get a `session_id` and complete flight/hotel/itinerary data!

#### Get Flights for a Session
```bash
curl "http://localhost:8000/api/flights?session_id=YOUR_SESSION_ID"
```

#### Chat with AI Assistant
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are the best places to visit in Mumbai?",
    "session_id": "YOUR_SESSION_ID"
  }'
```

#### Select a Flight
```bash
curl -X POST "http://localhost:8000/api/select-flight" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "YOUR_SESSION_ID",
    "flight_id": "FLIGHT_ID_FROM_RESPONSE"
  }'
```

#### Download PDF Itinerary
```bash
curl "http://localhost:8000/api/itinerary/YOUR_SESSION_ID/pdf" \
  --output itinerary.pdf
```

### Method 3: Using Postman

1. Import the API from http://localhost:8000/openapi.json
2. Create requests for each endpoint
3. Test the complete workflow

## 🔗 Connecting to Frontend

### Update Frontend API Base URL

In your React frontend, update the API base URL:

```typescript
// In your frontend config
const API_BASE_URL = "http://localhost:8000/api";

// Example API call
const generatePlan = async (preferences) => {
  const response = await fetch(`${API_BASE_URL}/generate-plan`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(preferences)
  });
  return response.json();
};
```

### Complete Frontend Integration

```typescript
// Complete workflow example
class TravelPlannerAPI {
  private baseURL = "http://localhost:8000/api";

  async generatePlan(preferences: TravelPreferences) {
    const response = await fetch(`${this.baseURL}/generate-plan`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(preferences)
    });
    return response.json();
  }

  async selectFlight(sessionId: string, flightId: string) {
    const response = await fetch(`${this.baseURL}/select-flight`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ session_id: sessionId, flight_id: flightId })
    });
    return response.json();
  }

  async getItinerary(sessionId: string) {
    const response = await fetch(`${this.baseURL}/itinerary/${sessionId}`);
    return response.json();
  }

  async downloadPDF(sessionId: string) {
    const response = await fetch(`${this.baseURL}/itinerary/${sessionId}/pdf`);
    const blob = await response.blob();
    
    // Create download link
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `itinerary-${sessionId}.pdf`;
    a.click();
  }
}
```

## 🎨 Customization Guide

### Add New Destinations

```python
# In app/services/free_ai_service.py
activities_db = {
    "YourNewCity": {
        "sightseeing": ["Monument 1", "Park 2", "Museum 3"],
        "food": ["Local dish 1", "Street food 2"],
        "culture": ["Temple 1", "Market 2"],
        "adventure": ["Activity 1", "Experience 2"]
    }
}
```

### Modify Flight Pricing

```python
# In app/services/free_data_service.py
route_prices = {
    ("Delhi", "YourCity"): 8500,  # Base price in INR
    ("Mumbai", "YourCity"): 6000,
    # Add more routes...
}
```

### Customize AI Responses

```python
# In app/services/free_ai_service.py
def _get_destination_response(self, message: str) -> str:
    custom_responses = [
        "Your custom travel advice here!",
        "Add destination-specific recommendations",
        # Add more responses...
    ]
    return random.choice(custom_responses)
```

### Add New Airlines

```python
# In app/services/free_data_service.py
airlines = [
    {"name": "YourAirline", "code": "YA", "logo": "logo_url"},
    # Add more airlines...
]
```

### Modify Hotel Types

```python
# In app/services/free_data_service.py
hotel_types = [
    {"suffix": "Boutique Hotel", "rating": 4.7, "price_multiplier": 1.8},
    # Add more hotel types...
]
```

## 🌐 Deployment Options

### Option 1: Heroku (Free Tier)

```bash
# Install Heroku CLI
# Create Procfile
echo "web: python run.py" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

### Option 2: Railway (Free)

1. Connect your GitHub repo to Railway
2. Railway auto-detects Python and deploys
3. Your API will be available at `https://your-app.railway.app`

### Option 3: Render (Free)

1. Connect GitHub repo to Render
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `python run.py`

### Option 4: Docker

```bash
# Build image
docker build -t raahi-backend .

# Run container
docker run -p 8000:8000 raahi-backend
```

### Option 5: VPS/Cloud Server

```bash
# On your server
git clone <your-repo>
cd backend
pip install -r requirements.txt
python run.py

# Use PM2 for production
npm install -g pm2
pm2 start run.py --name raahi-backend
```

## 🔧 Environment Configuration

### Create .env file (Optional)

```bash
cp .env.example .env
```

Edit `.env`:
```env
# Database (SQLite by default)
DATABASE_URL=sqlite:///./raahi.db

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# Free alternatives - no API keys needed!
USE_MOCK_DATA=true
ENABLE_WEB_SCRAPING=true

# Optional: Add OpenAI key for enhanced AI (but free version works great!)
OPENAI_API_KEY=your_key_here_or_leave_empty
```

## 🐛 Troubleshooting

### Common Issues & Solutions

#### 1. **Port Already in Use**
```bash
# Error: Address already in use
# Solution: Use different port
python run.py --port 8001
```

#### 2. **Module Not Found**
```bash
# Error: ModuleNotFoundError
# Solution: Install requirements
pip install -r requirements.txt
```

#### 3. **Database Issues**
```bash
# Error: Database locked
# Solution: Delete and recreate
rm raahi.db
python run.py  # Will recreate automatically
```

#### 4. **CORS Issues**
```python
# In app/main.py - CORS is already configured for:
allow_origins=["http://localhost:8080", "http://localhost:3000", "*"]
```

#### 5. **PDF Generation Issues**
```bash
# Error: ReportLab issues
# Solution: Reinstall reportlab
pip uninstall reportlab
pip install reportlab
```

### Debug Mode

Enable detailed logging:
```python
# In app/config.py
DEBUG = True

# Check logs for detailed error information
```

### Performance Optimization

```python
# For production, consider:
# 1. Use PostgreSQL instead of SQLite
DATABASE_URL=postgresql://user:pass@localhost/raahi

# 2. Add Redis for caching
# 3. Use Gunicorn for production server
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 📊 API Response Examples

### Generate Plan Response
```json
{
  "session_id": "abc123-def456",
  "flights": [
    {
      "id": "flight_1",
      "airline": "IndiGo",
      "flight_number": "6E234",
      "departure_airport": "DEL",
      "arrival_airport": "BOM",
      "departure_time": "08:30",
      "arrival_time": "11:15",
      "duration": "2h 45m",
      "price": 8500,
      "booking_url": "https://www.goindigo.in/booking/...",
      "ai_recommended": true,
      "ai_reasoning": {
        "price": "Great value for budget travelers",
        "duration": "Quick and convenient flight time"
      }
    }
  ],
  "hotels": [
    {
      "id": "hotel_1",
      "name": "Mumbai Grand Hotel",
      "rating": 4.5,
      "price_per_night": 5000,
      "booking_url": "https://www.booking.com/...",
      "ai_recommended": true
    }
  ],
  "itinerary": {
    "title": "Amazing 3-Day Mumbai Adventure",
    "total_days": 3,
    "estimated_cost": 15000,
    "daily_plans": [...]
  }
}
```

## 🎯 Next Steps

### Enhance Your Backend

1. **Add More Destinations**: Expand the activities database
2. **Improve AI Logic**: Add more sophisticated recommendation rules
3. **Add Features**: Weather integration, currency conversion
4. **Scale Up**: Move to PostgreSQL, add Redis caching
5. **Monitor**: Add logging and analytics

### Production Checklist

- [ ] Set `DEBUG=False` in production
- [ ] Use PostgreSQL for database
- [ ] Add proper logging
- [ ] Set up monitoring
- [ ] Configure HTTPS
- [ ] Add rate limiting
- [ ] Set up backups

## 🤝 Support & Community

### Getting Help

1. **Check the logs** - Most issues are logged with details
2. **Review the API docs** - http://localhost:8000/docs
3. **Test with curl** - Verify endpoints work independently
4. **Check database** - Use SQLite browser to inspect data

### Contributing

1. Fork the repository
2. Add new features or destinations
3. Test thoroughly
4. Submit pull request

---

## 🎉 Congratulations!

You now have a **completely FREE, production-grade AI travel planning backend** that:

✅ **Costs nothing to run**  
✅ **Generates realistic travel data**  
✅ **Provides intelligent recommendations**  
✅ **Creates real booking URLs**  
✅ **Generates professional PDFs**  
✅ **Scales to handle real users**  

**Start building amazing travel experiences today!** 🚀

---

*Built with ❤️ for developers who want powerful features without the costs.*