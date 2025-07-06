from fastapi import APIRouter, Query
from fastapi.responses import RedirectResponse

router = APIRouter()

@router.get("/redirect/flight")
def redirect_flight(
    airline: str = Query(...),
    origin: str = Query(...),
    destination: str = Query(...),
    date: str = Query(...)
):
    airline = airline.lower()
    booking_url = ""

    if "indigo" in airline:
        booking_url = f"https://www.goindigo.in/?bookingType=flight&origin={origin}&destination={destination}&departureDate={date}"
    elif "air india" in airline:
        booking_url = f"https://www.airindia.com/in/en/book/book-flight.html?origin={origin}&destination={destination}&departureDate={date}"
    elif "vistara" in airline:
        booking_url = "https://www.airvistara.com/in/en"
    else:
        # fallback: Google search
        booking_url = f"https://www.google.com/search?q=book+{airline}+flight+from+{origin}+to+{destination}+on+{date}"

    return RedirectResponse(url=booking_url)
