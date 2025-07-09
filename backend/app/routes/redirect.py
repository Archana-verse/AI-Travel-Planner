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
    
    elif "air india express" in airline:
        booking_url = "https://www.airindiaexpress.com/"
    
    elif "vistara" in airline:
        booking_url = "https://www.airvistara.com/in/en"
    
    elif "spicejet" in airline:
        booking_url = f"https://book.spicejet.com/Search.aspx?origin={origin}&destination={destination}&date={date}"
    
    elif "akasa" in airline:
        booking_url = "https://www.akasaair.com/"

    elif "goair" in airline or "go first" in airline:
        booking_url = f"https://www.google.com/search?q=book+go+first+flight+from+{origin}+to+{destination}+on+{date}"

    else:
        # Fallback: Google search
        booking_url = f"https://www.google.com/search?q=book+{airline}+flight+from+{origin}+to+{destination}+on+{date}"

    return RedirectResponse(url=booking_url)
