# 🧭 Raahi – AI-Powered Travel Itinerary Planner

**Raahi** is an intelligent travel planning assistant built using modern web technologies and multi-agent AI architecture. It seamlessly combines real-time flight/hotel search with itinerary generation powered by advanced LLMs and agent collaboration — designed to offer personalized, end-to-end trip planning.

---

## ✨ Features

- Destination-aware form with date, preferences, and dietary input
- Real-time flight and hotel data retrieval
- AI-generated day-by-day travel itinerary
- Multi-agent orchestration using **CrewAI** agents (Flight, Hotel, Travel)
- Gemini LLM integration for itinerary generation and refinement
- Integrated Chat UI for conversational trip planning
- One-click PDF download of your itinerary
- Fully responsive design with light/dark mode support

---

## Architecture Overview

### 1. High-Level System Architecture
![Overall Architecture](./assets/architecture-overview.jpg)

### 2. How Raahi Works
![How Raahi Works](./assets/raahi-flow.jpg)



---

##  Tech Stack

### Frontend
- **Vite + React + TypeScript**
- **TailwindCSS** for UI styling
- **Shadcn/UI** for accessible components
- **html2pdf.js** for generating PDF itineraries
- **Lucide Icons** for clean UI icons

### Backend
- **FastAPI** – ultra-fast Python backend for API endpoints
- **CrewAI** – orchestrates agents for flight, hotel, and travel logic
- **Gemini LLM (Google)** – for intelligent itinerary generation and refinements
- **SerpAPI** – real-time data source for flights and hotels

---

## AI & Agent Architecture

Raahi uses a modular **CrewAI agent architecture** to offload tasks:

| Agent         | Responsibilities                                |
|---------------|-------------------------------------------------|
|  Flight Agent | Filters flights by price, stops, duration       |
|  Hotel Agent  | Analyzes hotels by rating, location, price      |
|  Travel Agent | Plans day-by-day itinerary using Gemini LLM     |
|  Chat Agent   | Handles natural language trip conversations     |

---

## Local Development Setup

> **Minimum Requirements:** Node.js ≥ 18, Python ≥ 3.9

### 1. Clone the repository
```bash
git clone https://github.com/your-username/raahi.git
cd raahi



2. Backend (FastAPI)
cd backend
python -m venv venv
venv\Scripts\activate        # For Windows
source venv/bin/activate     # For macOS/Linux

pip install -r requirements.txt

uvicorn main:app --reload

Runs at: http://127.0.0.1:8000

Frontend (React + Vite)
cd frontend
npm install
npm run dev
Runs at: http://localhost:5173

Plan Page Flow (Client UX)
On the /plan route, users fill a multi-step form:

📍 Destination

📅 Dates (departure & return)

🧑‍🤝‍🧑 Number of travelers

🍛 Dietary preferences

💸 Budget tier

🎚️ Hotel affordability slider


This data is sent to the FastAPI backend, which:

Passes it to CrewAI agents

Fetches matching flight & hotel data

Prompts Gemini LLM for itinerary generation

Returns a complete plan to the frontend


Contributing
Pull requests are welcome! For major changes, please open an issue first.

