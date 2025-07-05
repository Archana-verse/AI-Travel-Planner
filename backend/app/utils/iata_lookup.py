# Airport code lookup (IATA) for Indian cities

iata_map = {
    "Delhi": "DEL",
    "New Delhi": "DEL",
    "Mumbai": "BOM",
    "Kolkata": "CCU",
    "Chennai": "MAA",
    "Bangalore": "BLR",
    "Hyderabad": "HYD",
    "Goa": "GOI",
    "Ahmedabad": "AMD",
    "Pune": "PNQ",
    "Jaipur": "JAI",
    "Lucknow": "LKO",
    "Guwahati": "GAU",
    "Varanasi": "VNS",
    "Indore": "IDR",
    "Patna": "PAT",
    "Nagpur": "NAG"
}

def get_iata_code(city_name: str) -> str:
    return iata_map.get(city_name.strip(), city_name.strip().upper())
