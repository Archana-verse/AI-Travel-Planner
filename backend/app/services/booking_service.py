from typing import Dict, Any
import urllib.parse
from datetime import datetime

class BookingService:
    """Service to generate real booking URLs for flights and hotels"""
    
    @staticmethod
    def generate_flight_booking_url(flight_data: Dict[str, Any], 
                                  departure_date: str) -> str:
        """Generate airline-specific booking URL with pre-filled data"""
        
        airline = flight_data.get('airline', '').lower()
        departure_airport = flight_data.get('departure_airport', '')
        arrival_airport = flight_data.get('arrival_airport', '')
        
        # Airline-specific URL patterns
        airline_urls = {
            'indigo': f"https://www.goindigo.in/booking/flight-select?from={departure_airport}&to={arrival_airport}&departure={departure_date}",
            'air india': f"https://www.airindia.in/booking/flight-search?from={departure_airport}&to={arrival_airport}&departure={departure_date}",
            'spicejet': f"https://www.spicejet.com/flight-booking?from={departure_airport}&to={arrival_airport}&departure={departure_date}",
            'vistara': f"https://www.airvistara.com/booking/flight-search?origin={departure_airport}&destination={arrival_airport}&departure={departure_date}",
            'akasa air': f"https://www.akasaair.com/booking?from={departure_airport}&to={arrival_airport}&departure={departure_date}",
            'go first': f"https://www.flygofirst.com/booking?from={departure_airport}&to={arrival_airport}&departure={departure_date}"
        }
        
        # Check for airline-specific URL
        for airline_key, url in airline_urls.items():
            if airline_key in airline:
                return url
        
        # Fallback to aggregator sites
        if flight_data.get('booking_url'):
            return flight_data['booking_url']
        
        # Skyscanner fallback
        skyscanner_url = f"https://www.skyscanner.co.in/transport/flights/{departure_airport}/{arrival_airport}/{departure_date}/"
        return skyscanner_url
    
    @staticmethod
    def generate_hotel_booking_url(hotel_data: Dict[str, Any], 
                                 check_in_date: str, 
                                 check_out_date: str,
                                 location: str) -> str:
        """Generate hotel booking URL with pre-filled data"""
        
        hotel_name = hotel_data.get('name', '')
        
        # Parse dates for URL formatting
        try:
            check_in = datetime.strptime(check_in_date, '%Y-%m-%d')
            check_out = datetime.strptime(check_out_date, '%Y-%m-%d')
        except:
            # Fallback to current date if parsing fails
            from datetime import datetime, timedelta
            check_in = datetime.now()
            check_out = check_in + timedelta(days=2)
        
        # If hotel has direct booking URL, use it
        if hotel_data.get('booking_url') and 'booking.com' not in hotel_data.get('booking_url', ''):
            return hotel_data['booking_url']
        
        # Booking.com URL with search parameters
        search_query = f"{hotel_name} {location}".strip()
        encoded_query = urllib.parse.quote_plus(search_query)
        
        booking_url = (
            f"https://www.booking.com/searchresults.html?"
            f"ss={encoded_query}&"
            f"checkin_year={check_in.year}&"
            f"checkin_month={check_in.month:02d}&"
            f"checkin_monthday={check_in.day:02d}&"
            f"checkout_year={check_out.year}&"
            f"checkout_month={check_out.month:02d}&"
            f"checkout_monthday={check_out.day:02d}&"
            f"group_adults=2&"
            f"no_rooms=1"
        )
        
        return booking_url
    
    @staticmethod
    def generate_fallback_flight_url(departure_airport: str, 
                                   arrival_airport: str, 
                                   departure_date: str) -> str:
        """Generate fallback flight search URL"""
        return f"https://www.makemytrip.com/flight/search?from={departure_airport}&to={arrival_airport}&departure={departure_date}"
    
    @staticmethod
    def generate_fallback_hotel_url(location: str, 
                                  check_in_date: str, 
                                  check_out_date: str) -> str:
        """Generate fallback hotel search URL"""
        encoded_location = urllib.parse.quote_plus(location)
        return f"https://www.makemytrip.com/hotels/hotel-listing?city={encoded_location}&checkin={check_in_date}&checkout={check_out_date}"