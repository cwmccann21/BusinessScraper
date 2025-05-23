import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change'
    GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')
    
    # Application paths
    DOWNLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance', 'downloads')
    
    # Default search parameters
    DEFAULT_RADIUS = 50000  # 50km
    MAX_RESULTS = 100
    
    # Search radius options (in meters)
    RADIUS_OPTIONS = [
        (1000, '1 km'),
        (5000, '5 km'),
        (10000, '10 km'),
        (25000, '25 km'),
        (50000, '50 km')
    ]
    
    # Business status options
    STATUS_OPTIONS = [
        ('all', 'All'),
        ('operational', 'Operational Only'),
        ('temporarily_closed', 'Include Temporarily Closed')
    ]
    
    # Rating filter options
    RATING_OPTIONS = [
        (0, 'Any Rating'),
        (3, '3+ Stars'),
        (4, '4+ Stars'),
        (4.5, '4.5+ Stars')
    ]
    
    # Fields to retrieve from Google Places API
    PLACE_FIELDS = [
        "name",
        "formatted_address",
        "formatted_phone_number",
        "website",
        "opening_hours",
        "email",
        "rating",
        "business_status",
        "price_level",
        "url"  # Google Maps URL
    ] 