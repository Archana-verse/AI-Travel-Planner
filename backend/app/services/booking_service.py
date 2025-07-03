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
        
        # Free booking sites (no commission needed)
        free_booking_sites = {
            'indigo': f"https://www.goindigo.in/booking/flight-select?from={departure_airport}&to={arrival_airport}&departure={departure_date}",
            'air india': f"https://www.airindia.in/booking/flight-search?from={departure_airport}&to={arrival_airport}&departure={departure_date}",
            'spicejet': f"https://www.spicejet.com/flight-booking?from={departure_airport}&to={arrival_airport}&departure={departure_date}",
            'vistara': f"https://www.airvistara.com/booking/flight-search?origin={departure_airport}&destination={arrival_airport}&departure={departure_date}",
            'akasaair': f"https://www.akasaair.com/booking?from={departure_airport}&to={arrival_airport}&departure={departure_date}",
        }
        
        # Check for airline-specific URL
        for airline_key, url in free_booking_sites.items():
            if airline_key in airline:
                return url
        
        # Free fallback options
        fallback_sites = [
            f"https://www.makemytrip.com/flight/search?from={departure_airport}&to={arrival_airport}&departure={departure_date}",
            f"https://www.cleartrip.com/flights/results?from={departure_airport}&to={arrival_airport}&depart={departure_date}",
            f"https://www.ixigo.com/search/result/flight/{departure_airport}-{arrival_airport}/{departure_date}",
            f"https://www.yatra.com/flights/search?from={departure_airport}&to={arrival_airport}&departure={departure_date}"
        ]
        
        return fallback_sites[0]  # Default to MakeMyTrip
    
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
            from datetime import datetime, timedelta
            check_in = datetime.now()
            check_out = check_in + timedelta(days=2)
        
        # Free hotel booking sites
        search_query = f"{hotel_name} {location}".strip()
        encoded_query = urllib.parse.quote_plus(search_query)
        encoded_location = urllib.parse.quote_plus(location)
        
        free_booking_options = [
            # Booking.com (free to use)
            f"https://www.booking.com/searchresults.html?ss={encoded_query}&checkin_year={check_in.year}&checkin_month={check_in.month:02d}&checkin_monthday={check_in.day:02d}&checkout_year={check_out.year}&checkout_month={check_out.month:02d}&checkout_monthday={check_out.day:02d}&group_adults=2&no_rooms=1",
            
            # MakeMyTrip
            f"https://www.makemytrip.com/hotels/hotel-listing?city={encoded_location}&checkin={check_in_date}&checkout={check_out_date}",
            
            # Cleartrip
            f"https://www.cleartrip.com/hotels/results?where={encoded_location}&checkin={check_in_date}&checkout={check_out_date}",
            
            # OYO (Indian budget hotels)
            f"https://www.oyorooms.com/search?location={encoded_location}&checkin={check_in_date}&checkout={check_out_date}",
            
            # Goibibo
            f"https://www.goibibo.com/hotels/search/?city={encoded_location}&checkin={check_in_date}&checkout={check_out_date}"
        ]
        
        return free_booking_options[0]  # Default to Booking.com
    
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