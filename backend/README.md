# Raahi.ai Backend

Production-grade FastAPI backend for AI-powered travel planning with real-time data integration.

## Features

- 🤖 **AI-Powered Planning**: CrewAI agents with Gemini (Vertex AI) integration
- ✈️ **Real-Time Flight Data**: SerpAPI Google Flights integration
- 🏨 **Live Hotel Search**: SerpAPI Google Hotels integration
- 📋 **Smart Itineraries**: AI-generated day-wise travel plans
- 💬 **Chat Assistant**: Gemini-powered travel advice
- 📄 **PDF Generation**: Downloadable itinerary PDFs
- 🔗 **Direct Booking**: Real airline/hotel booking URLs
- 💾 **Session Management**: SQLite database with full persistence

## Quick Start

### 1. Environment Setup

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your API keys
nano .env
```

Required API keys:
- **SerpAPI**: Get from [serpapi.com](https://serpapi.com)
- **Google Cloud**: Set up Vertex AI and get service account JSON

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Server

```bash
python run.py
```

Server starts at: `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

## API Endpoints

### Core Planning
- `POST /api/generate-plan` - Generate complete travel plan
- `GET /api/flights?session_id=...` - Get flights for session
- `GET /api/hotels?session_id=...` - Get hotels for session
- `GET /api/itinerary/{session_id}` - Get complete itinerary

### Booking & Selection
- `POST /api/select-flight` - Select flight with booking URL
- `POST /api/select-hotel` - Select hotel with booking URL

### Additional Features
- `POST /api/chat` - AI travel assistant
- `GET /api/itinerary/{session_id}/pdf` - Download PDF

## Architecture

```
backend/
├── app/
│   ├── main.py              # FastAPI app setup
│   ├── config.py            # Settings & environment
│   ├── database.py          # SQLAlchemy setup
│   ├── models.py            # Database models
│   ├── schemas.py           # Pydantic schemas
│   ├── routers/             # API route handlers
│   │   ├── planning.py      # Main planning logic
│   │   ├── flights.py       # Flight endpoints
│   │   ├── hotels.py        # Hotel endpoints
│   │   ├── itinerary.py     # Itinerary & PDF
│   │   ├── chat.py          # AI chat assistant
│   │   └── booking.py       # Selection & booking URLs
│   └── services/            # Business logic
│       ├── serpapi_service.py    # Real-time data fetching
│       ├── gemini_service.py     # AI/LLM integration
│       ├── booking_service.py    # URL generation
│       └── pdf_service.py        # PDF generation
├── requirements.txt         # Dependencies
├── .env.example            # Environment template
└── run.py                  # Server startup
```

## Data Flow

1. **User submits preferences** → `POST /generate-plan`
2. **SerpAPI fetches real data** → Flights & Hotels
3. **Gemini analyzes & recommends** → AI reasoning
4. **Data saved to SQLite** → Session persistence
5. **User selects options** → `POST /select-flight|hotel`
6. **Booking URLs generated** → Real airline/hotel sites
7. **Itinerary available** → `GET /itinerary/{session_id}`

## Booking URL Examples

### Flight URLs
- **IndiGo**: `https://www.goindigo.in/booking/flight-select?from=DEL&to=BOM&departure=2025-07-20`
- **Air India**: `https://www.airindia.in/booking/flight-search?from=DEL&to=BOM&departure=2025-07-20`
- **Fallback**: Skyscanner/MakeMyTrip with search params

### Hotel URLs
- **Booking.com**: `https://www.booking.com/searchresults.html?ss=Hotel+Name+City&checkin_year=2025&checkin_month=07&checkin_monthday=20`
- **Direct**: Hotel's own booking system when available

## Environment Variables

```bash
# SerpAPI (Required)
SERPAPI_KEY=your_serpapi_key_here

# Google Cloud / Vertex AI (Required)
GOOGLE_CLOUD_PROJECT=your_project_id
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json

# Database
DATABASE_URL=sqlite:///./raahi.db

# Server Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True
```

## Production Deployment

### Docker
```bash
# Build image
docker build -t raahi-backend .

# Run container
docker run -p 8000:8000 --env-file .env raahi-backend
```

### Cloud Deployment
- **Google Cloud Run**: Deploy with Vertex AI integration
- **AWS ECS**: Use with Bedrock for AI features
- **Railway/Render**: Simple deployment with environment variables

## Database Schema

- **TravelSession**: User preferences & session management
- **Flight**: Real flight data from SerpAPI
- **Hotel**: Real hotel data from SerpAPI  
- **Itinerary**: AI-generated travel plans
- **SelectedFlight/Hotel**: User selections with booking URLs
- **ChatMessage**: AI assistant conversations

## Error Handling

- Comprehensive logging with structured error messages
- Graceful fallbacks for API failures
- Input validation with Pydantic schemas
- Database transaction management

## Performance

- Async/await for concurrent API calls
- Database connection pooling
- Response caching for repeated queries
- Optimized PDF generation

## Security

- Input sanitization and validation
- API key management via environment variables
- CORS configuration for frontend integration
- SQL injection prevention with SQLAlchemy ORM

## Testing

```bash
# Run tests
pytest

# Test specific endpoint
curl -X POST "http://localhost:8000/api/generate-plan" \
  -H "Content-Type: application/json" \
  -d '{
    "from_location": "Delhi",
    "to_location": "Mumbai", 
    "departure_date": "2025-07-20",
    "travel_class": "economy",
    "budget": "comfort",
    "travelers": "couple"
  }'
```

## Support

For issues or questions:
1. Check API documentation at `/docs`
2. Review logs for error details
3. Verify API keys and environment setup
4. Test with minimal request payload

---

**Built with ❤️ for Indian travelers by Raahi.ai**