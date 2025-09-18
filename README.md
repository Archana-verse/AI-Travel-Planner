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

## 📸 Project Preview
- <img width="1272" height="900" alt="Screenshot 2025-09-18 124811" src="https://github.com/user-attachments/assets/99653e7f-cfbd-4b38-8eb1-a29e4f36059e" />

- <img width="1718" height="960" alt="Screenshot 2025-09-18 124313" src="https://github.com/user-attachments/assets/64b196ca-0562-45d4-90cb-3316e9d28bf2" />

- <img width="1211" height="893" alt="Screenshot 2025-09-18 124350" src="https://github.com/user-attachments/assets/e3def7b3-cbb7-4436-a29e-6124b9fd3361" />

- <img width="1165" height="908" alt="Screenshot 2025-09-18 124459" src="https://github.com/user-attachments/assets/5c69a9c3-d66a-48dd-8d91-1fbf9b8af2fd" />

- <img width="1159" height="913" alt="Screenshot 2025-09-18 124552" src="https://github.com/user-attachments/assets/bbcda92e-95c1-4a12-b42b-d3255ef5c711" />

-  <img width="1172" height="861" alt="Screenshot 2025-09-18 124744" src="https://github.com/user-attachments/assets/a60b0e21-a384-463d-b3ad-75bcd958d4fe" />

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

