from typing import Dict, Any
import urllib.parse
from datetime import datetime
from app.config import settings

class BookingService:
    """Service to generate real booking URLs for flights and hotels"""
    
    @staticmethod
    def generate_flight_booking_url(flight: Dict[str, Any], preferences: Dict[str, Any] = None) -> str:
        """Generate Skyscanner booking URL with pre-filled data"""
        
        departure_airport = flight.get('departure_airport', '')
        arrival_airport = flight.get('arrival_airport', '')
        departure_date = flight.get('departure_date', '')
        return_date = flight.get('return_date', '')
        
        # Format date for Skyscanner (YYMMDD format)
        try:
            dep_date_obj = datetime.strptime(departure_date, '%Y-%m-%d')
            formatted_dep_date = dep_date_obj.strftime('%y%m%d')
            
            if return_date:
                ret_date_obj = datetime.strptime(return_date, '%Y-%m-%d')
                formatted_ret_date = ret_date_obj.strftime('%y%m%d')
                # Round trip
                skyscanner_url = f"https://www.skyscanner.com/flights/{departure_airport}/{arrival_airport}/{formatted_dep_date}/{formatted_ret_date}"
            else:
                # One way
                skyscanner_url = f"https://www.skyscanner.com/flights/{departure_airport}/{arrival_airport}/{formatted_dep_date}"
                
        except:
            # Fallback format
            skyscanner_url = f"https://www.skyscanner.com/flights/{departure_airport}/{arrival_airport}/{departure_date}"
        
        # Add additional parameters
        params = {
            'adults': 1,
            'children': 0,
            'infants': 0,
            'cabinclass': flight.get('flight_class', 'economy').lower(),
            'rtn': '1' if return_date else '0'
        }
        
        # Add query parameters
        query_string = urllib.parse.urlencode(params)
        final_url = f"{skyscanner_url}?{query_string}"
        
        return final_url
    
    @staticmethod
    def generate_hotel_booking_url(hotel: Dict[str, Any], preferences: Dict[str, Any] = None) -> str:
        """Generate Booking.com URL with pre-filled data"""
        
        hotel_name = hotel.get('name', '')
        location = hotel.get('location', '')
        check_in_date = preferences.get('departure_date', '') if preferences else ''
        check_out_date = preferences.get('return_date', '') if preferences else ''
        
        # Format dates for Booking.com
        try:
            if check_in_date:
                checkin_obj = datetime.strptime(check_in_date, '%Y-%m-%d')
                checkin_year = checkin_obj.year
                checkin_month = checkin_obj.month
                checkin_day = checkin_obj.day
            else:
                # Default to next month
                from datetime import datetime, timedelta
                checkin_obj = datetime.now() + timedelta(days=30)
                checkin_year = checkin_obj.year
                checkin_month = checkin_obj.month
                checkin_day = checkin_obj.day
            
            if check_out_date:
                checkout_obj = datetime.strptime(check_out_date, '%Y-%m-%d')
                checkout_year = checkout_obj.year
                checkout_month = checkout_obj.month
                checkout_day = checkout_obj.day
            else:
                # Default to 3 days after check-in
                checkout_obj = checkin_obj + timedelta(days=3)
                checkout_year = checkout_obj.year
                checkout_month = checkout_obj.month
                checkout_day = checkout_obj.day
                
        except:
            # Fallback dates
            from datetime import datetime, timedelta
            checkin_obj = datetime.now() + timedelta(days=30)
            checkout_obj = checkin_obj + timedelta(days=3)
            checkin_year, checkin_month, checkin_day = checkin_obj.year, checkin_obj.month, checkin_obj.day
            checkout_year, checkout_month, checkout_day = checkout_obj.year, checkout_obj.month, checkout_obj.day
        
        # Create search query (hotel name + location)
        search_term = f"{hotel_name} {location}".strip()
        encoded_search = urllib.parse.quote_plus(search_term)
        
        # Build Booking.com URL
        booking_url = f"https://www.booking.com/searchresults.html"
        
        params = {
            'ss': encoded_search,
            'checkin_year': checkin_year,
            'checkin_month': f"{checkin_month:02d}",
            'checkin_monthday': f"{checkin_day:02d}",
            'checkout_year': checkout_year,
            'checkout_month': f"{checkout_month:02d}",
            'checkout_monthday': f"{checkout_day:02d}",
            'group_adults': 2,
            'no_rooms': 1,
            'group_children': 0
        }
        
        query_string = urllib.parse.urlencode(params)
        final_url = f"{booking_url}?{query_string}"
        
        return final_url
    
    @staticmethod
    def generate_skyscanner_url(origin: str, destination: str, departure_date: str, return_date: str = None) -> str:
        """Generate generic Skyscanner search URL"""
        
        try:
            dep_date_obj = datetime.strptime(departure_date, '%Y-%m-%d')
            formatted_dep_date = dep_date_obj.strftime('%y%m%d')
            
            if return_date:
                ret_date_obj = datetime.strptime(return_date, '%Y-%m-%d')
                formatted_ret_date = ret_date_obj.strftime('%y%m%d')
                url = f"https://www.skyscanner.com/flights/{origin}/{destination}/{formatted_dep_date}/{formatted_ret_date}"
            else:
                url = f"https://www.skyscanner.com/flights/{origin}/{destination}/{formatted_dep_date}"
                
        except:
            # Fallback format
            if return_date:
                url = f"https://www.skyscanner.com/flights/{origin}/{destination}/{departure_date}/{return_date}"
            else:
                url = f"https://www.skyscanner.com/flights/{origin}/{destination}/{departure_date}"
        
        return url
    
    @staticmethod
    def generate_booking_com_url(location: str, check_in: str, check_out: str) -> str:
        """Generate generic Booking.com search URL"""
        
        encoded_location = urllib.parse.quote_plus(location)
        
        try:
            checkin_obj = datetime.strptime(check_in, '%Y-%m-%d')
            checkout_obj = datetime.strptime(check_out, '%Y-%m-%d')
            
            params = {
                'ss': encoded_location,
                'checkin_year': checkin_obj.year,
                'checkin_month': f"{checkin_obj.month:02d}",
                'checkin_monthday': f"{checkin_obj.day:02d}",
                'checkout_year': checkout_obj.year,
                'checkout_month': f"{checkout_obj.month:02d}",
                'checkout_monthday': f"{checkout_obj.day:02d}",
                'group_adults': 2,
                'no_rooms': 1
            }
            
        except:
            # Fallback with current date + offset
            from datetime import datetime, timedelta
            checkin_obj = datetime.now() + timedelta(days=30)
            checkout_obj = checkin_obj + timedelta(days=3)
            
            params = {
                'ss': encoded_location,
                'checkin_year': checkin_obj.year,
                'checkin_month': f"{checkin_obj.month:02d}",
                'checkin_monthday': f"{checkin_obj.day:02d}",
                'checkout_year': checkout_obj.year,
                'checkout_month': f"{checkout_obj.month:02d}",
                'checkout_monthday': f"{checkout_obj.day:02d}",
                'group_adults': 2,
                'no_rooms': 1
            }
        
        query_string = urllib.parse.urlencode(params)
        return f"https://www.booking.com/searchresults.html?{query_string}"