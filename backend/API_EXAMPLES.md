# 📚 API Examples - Raahi.ai Free Backend

**Real examples you can copy and paste to test every feature!**

## 🎯 Complete Workflow Example

### Step 1: Generate Travel Plan

```bash
curl -X POST "http://localhost:8000/api/generate-plan" \
  -H "Content-Type: application/json" \
  -d '{
    "from_location": "Delhi",
    "to_location": "Goa",
    "departure_date": "2025-08-15",
    "return_date": "2025-08-20",
    "travel_class": "economy",
    "budget": "comfort",
    "travelers": "couple",
    "interests": ["beaches", "nightlife", "food"],
    "diet": "non-vegetarian"
  }'
```

**Response:**
```json
{
  "session_id": "abc123-def456-ghi789",
  "flights": [
    {
      "id": "flight_001",
      "airline": "IndiGo",
      "flight_number": "6E456",
      "departure_airport": "DEL",
      "arrival_airport": "GOI",
      "departure_time": "08:30",
      "arrival_time": "11:15",
      "duration": "2h 45m",
      "price": 8500,
      "currency": "INR",
      "booking_url": "https://www.goindigo.in/booking/flight-select?from=DEL&to=GOI&departure=2025-08-15",
      "ai_recommended": true,
      "ai_reasoning": {
        "price": "Great value for budget travelers",
        "duration": "Quick and convenient flight time",
        "airline": "Known for punctuality and value",
        "departure": "Morning flight - full day at destination"
      }
    }
  ],
  "hotels": [
    {
      "id": "hotel_001", 
      "name": "Goa Grand Hotel",
      "location": "Goa City Center",
      "rating": 4.5,
      "reviews_count": 1250,
      "price_per_night": 6000,
      "currency": "INR",
      "amenities": [
        {"icon": "wifi", "label": "Free WiFi"},
        {"icon": "pool", "label": "Swimming Pool"},
        {"icon": "spa", "label": "Spa & Wellness"}
      ],
      "booking_url": "https://www.booking.com/searchresults.html?ss=Goa+Grand+Hotel&checkin=2025-08-15&checkout=2025-08-20",
      "ai_recommended": true,
      "ai_reasoning": {
        "rating": "Excellent guest reviews and high ratings",
        "location": "Centrally located with easy access to attractions",
        "amenities": "Excellent facilities for relaxation",
        "value": "Great balance of comfort and price"
      }
    }
  ],
  "itinerary": {
    "id": "itinerary_001",
    "session_id": "abc123-def456-ghi789",
    "title": "Amazing 5-Day Goa Adventure",
    "description": "Discover the best of Goa with this carefully crafted itinerary featuring beaches, nightlife, food.",
    "total_days": 5,
    "estimated_cost": 25000,
    "currency": "INR",
    "daily_plans": [
      {
        "day": 1,
        "date": "2025-08-15",
        "title": "Arrival & Local Exploration",
        "activities": [
          {
            "time": "10:00 AM",
            "icon": "✈️",
            "activity": "Arrive at destination",
            "duration": "1 hour",
            "cost": 0
          },
          {
            "time": "12:00 PM", 
            "icon": "🏨",
            "activity": "Check-in to hotel",
            "duration": "1 hour",
            "cost": 0
          },
          {
            "time": "2:00 PM",
            "icon": "🍽️",
            "activity": "Local lunch",
            "duration": "1 hour", 
            "cost": 500
          },
          {
            "time": "4:00 PM",
            "icon": "🏖️",
            "activity": "Visit Baga Beach",
            "duration": "2 hours",
            "cost": 300
          }
        ]
      }
    ]
  }
}
```

### Step 2: Select a Flight

```bash
curl -X POST "http://localhost:8000/api/select-flight" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "abc123-def456-ghi789",
    "flight_id": "flight_001"
  }'
```

**Response:**
```json
{
  "message": "Flight selected successfully",
  "booking_url": "https://www.goindigo.in/booking/flight-select?from=DEL&to=GOI&departure=2025-08-15",
  "flight_details": {
    "airline": "IndiGo",
    "flight_number": "6E456",
    "route": "DEL → GOI",
    "price": 8500
  }
}
```

### Step 3: Select a Hotel

```bash
curl -X POST "http://localhost:8000/api/select-hotel" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "abc123-def456-ghi789",
    "hotel_id": "hotel_001",
    "check_in_date": "2025-08-15",
    "check_out_date": "2025-08-20"
  }'
```

**Response:**
```json
{
  "message": "Hotel selected successfully",
  "booking_url": "https://www.booking.com/searchresults.html?ss=Goa+Grand+Hotel&checkin_year=2025&checkin_month=08&checkin_monthday=15&checkout_year=2025&checkout_month=08&checkout_monthday=20",
  "hotel_details": {
    "name": "Goa Grand Hotel",
    "location": "Goa City Center",
    "rating": 4.5,
    "price_per_night": 6000,
    "check_in": "2025-08-15",
    "check_out": "2025-08-20"
  }
}
```

### Step 4: Get Complete Itinerary

```bash
curl "http://localhost:8000/api/itinerary/abc123-def456-ghi789"
```

**Response:**
```json
{
  "id": "itinerary_001",
  "session_id": "abc123-def456-ghi789",
  "title": "Amazing 5-Day Goa Adventure",
  "description": "Discover the best of Goa...",
  "total_days": 5,
  "estimated_cost": 25000,
  "currency": "INR",
  "daily_plans": [...],
  "selected_flight": {
    "id": "flight_001",
    "airline": "IndiGo",
    "flight_number": "6E456",
    "booking_url": "https://www.goindigo.in/booking/flight-select?from=DEL&to=GOI&departure=2025-08-15"
  },
  "selected_hotel": {
    "id": "hotel_001",
    "name": "Goa Grand Hotel",
    "booking_url": "https://www.booking.com/searchresults.html?ss=Goa+Grand+Hotel&checkin_year=2025..."
  }
}
```

### Step 5: Download PDF

```bash
curl "http://localhost:8000/api/itinerary/abc123-def456-ghi789/pdf" \
  --output goa_trip_itinerary.pdf
```

## 💬 Chat Examples

### General Travel Question

```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are the best places to visit in Rajasthan?"
  }'
```

**Response:**
```json
{
  "response": "Rajasthan offers incredible diversity! Must-visit places include Jaipur for palaces and forts, Udaipur for lakes and romance, Jodhpur for the blue city experience, and Jaisalmer for desert adventures. Each city has unique architecture, culture, and experiences. The best time to visit is October to March when the weather is pleasant.",
  "session_id": null
}
```

### Context-Aware Chat

```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What should I pack for my trip?",
    "session_id": "abc123-def456-ghi789"
  }'
```

**Response:**
```json
{
  "response": "For your Goa trip in August, pack light cotton clothes, swimwear, sunscreen, sunglasses, and a light rain jacket as it's monsoon season. Don't forget comfortable sandals for the beach and closed shoes for exploring. Since you're interested in nightlife, pack some nice evening wear for clubs and restaurants.",
  "session_id": "abc123-def456-ghi789"
}
```

### Budget Question

```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "How much should I budget for a 5-day trip to Kerala?"
  }'
```

**Response:**
```json
{
  "response": "For a comfortable 5-day Kerala trip, budget ₹20,000-30,000 per person including accommodation (₹3,000-5,000/night), meals (₹1,000-1,500/day), local transport (₹500-800/day), and activities like backwater cruises (₹2,000-4,000). Budget travelers can manage with ₹15,000-20,000, while luxury experiences start from ₹40,000+.",
  "session_id": null
}
```

## 🔍 Query Examples

### Get Flights for Session

```bash
curl "http://localhost:8000/api/flights?session_id=abc123-def456-ghi789"
```

### Get Hotels for Session

```bash
curl "http://localhost:8000/api/hotels?session_id=abc123-def456-ghi789"
```

## 🌍 Different Destination Examples

### Mumbai Business Trip

```bash
curl -X POST "http://localhost:8000/api/generate-plan" \
  -H "Content-Type: application/json" \
  -d '{
    "from_location": "Bangalore",
    "to_location": "Mumbai",
    "departure_date": "2025-09-10",
    "return_date": "2025-09-12",
    "travel_class": "business",
    "budget": "luxury",
    "travelers": "solo",
    "interests": ["sightseeing", "food", "nightlife"],
    "diet": "vegetarian"
  }'
```

### Family Trip to Rajasthan

```bash
curl -X POST "http://localhost:8000/api/generate-plan" \
  -H "Content-Type: application/json" \
  -d '{
    "from_location": "Delhi",
    "to_location": "Jaipur",
    "departure_date": "2025-12-20",
    "return_date": "2025-12-25",
    "travel_class": "economy",
    "budget": "comfort",
    "travelers": "family",
    "interests": ["culture", "heritage", "shopping"],
    "diet": "vegetarian"
  }'
```

### Budget Backpacking

```bash
curl -X POST "http://localhost:8000/api/generate-plan" \
  -H "Content-Type: application/json" \
  -d '{
    "from_location": "Chennai",
    "to_location": "Kolkata",
    "departure_date": "2025-10-15",
    "return_date": "2025-10-20",
    "travel_class": "economy",
    "budget": "budget",
    "travelers": "friends",
    "interests": ["culture", "food", "heritage"],
    "diet": "non-vegetarian"
  }'
```

## 🧪 Testing Different Scenarios

### Weekend Getaway

```bash
curl -X POST "http://localhost:8000/api/generate-plan" \
  -H "Content-Type: application/json" \
  -d '{
    "from_location": "Mumbai",
    "to_location": "Goa",
    "departure_date": "2025-11-08",
    "return_date": "2025-11-10",
    "travel_class": "economy",
    "budget": "comfort",
    "travelers": "couple",
    "interests": ["beaches", "food"],
    "diet": "non-vegetarian"
  }'
```

### Luxury Honeymoon

```bash
curl -X POST "http://localhost:8000/api/generate-plan" \
  -H "Content-Type: application/json" \
  -d '{
    "from_location": "Delhi",
    "to_location": "Udaipur",
    "departure_date": "2025-02-14",
    "return_date": "2025-02-18",
    "travel_class": "business",
    "budget": "luxury",
    "travelers": "couple",
    "interests": ["culture", "wellness", "heritage"],
    "diet": "vegetarian"
  }'
```

## 📊 Response Data Structure

### Flight Object
```json
{
  "id": "unique_flight_id",
  "airline": "IndiGo",
  "flight_number": "6E456",
  "departure_airport": "DEL",
  "arrival_airport": "BOM",
  "departure_time": "08:30",
  "arrival_time": "11:15",
  "duration": "2h 45m",
  "price": 8500,
  "currency": "INR",
  "flight_class": "economy",
  "stops": 0,
  "booking_url": "https://airline-booking-url",
  "thumbnail": "airline-logo-url",
  "ai_recommended": true,
  "ai_reasoning": {
    "price": "Analysis of price competitiveness",
    "duration": "Flight duration assessment",
    "airline": "Airline quality evaluation",
    "departure": "Departure time convenience"
  }
}
```

### Hotel Object
```json
{
  "id": "unique_hotel_id",
  "name": "Hotel Name",
  "location": "City Area",
  "rating": 4.5,
  "reviews_count": 1250,
  "price_per_night": 5000,
  "currency": "INR",
  "amenities": [
    {"icon": "wifi", "label": "Free WiFi"},
    {"icon": "pool", "label": "Swimming Pool"}
  ],
  "description": "Hotel description",
  "booking_url": "https://hotel-booking-url",
  "thumbnail": "hotel-image-url",
  "ai_recommended": true,
  "ai_reasoning": {
    "rating": "Rating analysis",
    "location": "Location convenience",
    "amenities": "Amenities evaluation",
    "value": "Value for money assessment"
  }
}
```

## 🔧 Error Handling Examples

### Invalid Session ID

```bash
curl "http://localhost:8000/api/flights?session_id=invalid-session"
```

**Response:**
```json
{
  "detail": "No flights found for this session"
}
```

### Missing Required Fields

```bash
curl -X POST "http://localhost:8000/api/generate-plan" \
  -H "Content-Type: application/json" \
  -d '{
    "from_location": "Delhi"
  }'
```

**Response:**
```json
{
  "detail": [
    {
      "loc": ["body", "to_location"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

## 🎯 Integration Tips

### Frontend Integration

```javascript
// React example
const api = {
  baseURL: 'http://localhost:8000/api',
  
  async generatePlan(preferences) {
    const response = await fetch(`${this.baseURL}/generate-plan`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(preferences)
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return response.json();
  },
  
  async selectFlight(sessionId, flightId) {
    const response = await fetch(`${this.baseURL}/select-flight`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        session_id: sessionId,
        flight_id: flightId
      })
    });
    
    return response.json();
  }
};
```

### Mobile App Integration

```dart
// Flutter example
class TravelAPI {
  static const String baseURL = 'http://localhost:8000/api';
  
  static Future<Map<String, dynamic>> generatePlan(Map<String, dynamic> preferences) async {
    final response = await http.post(
      Uri.parse('$baseURL/generate-plan'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode(preferences),
    );
    
    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to generate plan');
    }
  }
}
```

---

**🎉 You now have complete examples for every API endpoint!**

Copy these examples and start building your amazing travel application with zero API costs! 🚀