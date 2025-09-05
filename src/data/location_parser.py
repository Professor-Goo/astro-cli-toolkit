"""
Enhanced location input and management system.
Functional approach to handling custom observer locations.
"""

from dataclasses import dataclass
from typing import Optional, Dict, List, Tuple
import re

from ..data.models import ObserverLocation


@dataclass(frozen=True)
class LocationParseResult:
    """Immutable result of location parsing - error as data pattern."""
    success: bool
    location: Optional[ObserverLocation]
    error_message: str


# Common city coordinates for quick lookup
CITY_COORDINATES = {
    # North America
    "new york": (40.7128, -74.0060, "New York, NY"),
    "nyc": (40.7128, -74.0060, "New York, NY"),
    "los angeles": (34.0522, -118.2437, "Los Angeles, CA"),
    "la": (34.0522, -118.2437, "Los Angeles, CA"),
    "chicago": (41.8781, -87.6298, "Chicago, IL"),
    "denver": (39.7392, -104.9903, "Denver, CO"),
    "seattle": (47.6062, -122.3321, "Seattle, WA"),
    "boston": (42.3601, -71.0589, "Boston, MA"),
    "miami": (25.7617, -80.1918, "Miami, FL"),
    "san francisco": (37.7749, -122.4194, "San Francisco, CA"),
    "sf": (37.7749, -122.4194, "San Francisco, CA"),
    "phoenix": (33.4484, -112.0740, "Phoenix, AZ"),
    "philadelphia": (39.9526, -75.1652, "Philadelphia, PA"),
    "houston": (29.7604, -95.3698, "Houston, TX"),
    "dallas": (32.7767, -96.7970, "Dallas, TX"),
    "atlanta": (33.7490, -84.3880, "Atlanta, GA"),
    "toronto": (43.6532, -79.3832, "Toronto, ON"),
    "vancouver": (49.2827, -123.1207, "Vancouver, BC"),
    "montreal": (45.5017, -73.5673, "Montreal, QC"),
    "mexico city": (19.4326, -99.1332, "Mexico City, Mexico"),
    
    # Europe
    "london": (51.5074, -0.1278, "London, UK"),
    "paris": (48.8566, 2.3522, "Paris, France"),
    "berlin": (52.5200, 13.4050, "Berlin, Germany"),
    "rome": (41.9028, 12.4964, "Rome, Italy"),
    "madrid": (40.4168, -3.7038, "Madrid, Spain"),
    "amsterdam": (52.3676, 4.9041, "Amsterdam, Netherlands"),
    "vienna": (48.2082, 16.3738, "Vienna, Austria"),
    "prague": (50.0755, 14.4378, "Prague, Czech Republic"),
    "stockholm": (59.3293, 18.0686, "Stockholm, Sweden"),
    "oslo": (59.9139, 10.7522, "Oslo, Norway"),
    "copenhagen": (55.6761, 12.5683, "Copenhagen, Denmark"),
    "helsinki": (60.1699, 24.9384, "Helsinki, Finland"),
    "athens": (37.9838, 23.7275, "Athens, Greece"),
    "lisbon": (38.7223, -9.1393, "Lisbon, Portugal"),
    "zurich": (47.3769, 8.5417, "Zurich, Switzerland"),
    "moscow": (55.7558, 37.6176, "Moscow, Russia"),
    
    # Asia
    "tokyo": (35.6762, 139.6503, "Tokyo, Japan"),
    "beijing": (39.9042, 116.4074, "Beijing, China"),
    "shanghai": (31.2304, 121.4737, "Shanghai, China"),
    "hong kong": (22.3193, 114.1694, "Hong Kong"),
    "singapore": (1.3521, 103.8198, "Singapore"),
    "mumbai": (19.0760, 72.8777, "Mumbai, India"),
    "delhi": (28.7041, 77.1025, "Delhi, India"),
    "bangalore": (12.9716, 77.5946, "Bangalore, India"),
    "seoul": (37.5665, 126.9780, "Seoul, South Korea"),
    "bangkok": (13.7563, 100.5018, "Bangkok, Thailand"),
    "jakarta": (-6.2088, 106.8456, "Jakarta, Indonesia"),
    "manila": (14.5995, 120.9842, "Manila, Philippines"),
    "kuala lumpur": (3.1390, 101.6869, "Kuala Lumpur, Malaysia"),
    
    # Australia & Oceania
    "sydney": (-33.8688, 151.2093, "Sydney, Australia"),
    "melbourne": (-37.8136, 144.9631, "Melbourne, Australia"),
    "brisbane": (-27.4698, 153.0251, "Brisbane, Australia"),
    "perth": (-31.9505, 115.8605, "Perth, Australia"),
    "auckland": (-36.8485, 174.7633, "Auckland, New Zealand"),
    "wellington": (-41.2865, 174.7762, "Wellington, New Zealand"),
    
    # South America
    "buenos aires": (-34.6118, -58.3960, "Buenos Aires, Argentina"),
    "sao paulo": (-23.5558, -46.6396, "São Paulo, Brazil"),
    "rio de janeiro": (-22.9068, -43.1729, "Rio de Janeiro, Brazil"),
    "santiago": (-33.4489, -70.6693, "Santiago, Chile"),
    "lima": (-12.0464, -77.0428, "Lima, Peru"),
    "bogota": (4.7110, -74.0721, "Bogotá, Colombia"),
    
    # Africa
    "cairo": (30.0444, 31.2357, "Cairo, Egypt"),
    "cape town": (-33.9249, 18.4241, "Cape Town, South Africa"),
    "johannesburg": (-26.2041, 28.0473, "Johannesburg, South Africa"),
    "nairobi": (-1.2921, 36.8219, "Nairobi, Kenya"),
    "lagos": (6.5244, 3.3792, "Lagos, Nigeria"),
    "casablanca": (33.5731, -7.5898, "Casablanca, Morocco"),
}


def parse_coordinate_string(coord_str: str) -> Tuple[bool, float, str]:
    """
    Parse coordinate string in various formats.
    
    Supports formats like:
    - "40.7128" (decimal degrees)
    - "40°42'46\"N" (degrees, minutes, seconds)
    - "40d42m46s" (alternative DMS format)
    - "-74.0060" (negative for West/South)
    
    Returns: (success, value, error_message)
    """
    coord_str = coord_str.strip().upper()
    
    # Try decimal degrees first
    try:
        value = float(coord_str)
        return True, value, ""
    except ValueError:
        pass
    
    # Try DMS format: 40°42'46"N or 40d42m46sN
    dms_pattern = r"(\d+)[°D]\s*(\d+)[\'M]\s*(\d+(?:\.\d+)?)[\"S]?\s*([NSEW]?)"
    match = re.match(dms_pattern, coord_str)
    
    if match:
        degrees = int(match.group(1))
        minutes = int(match.group(2))
        seconds = float(match.group(3))
        direction = match.group(4)
        
        # Convert to decimal degrees
        decimal = degrees + minutes/60.0 + seconds/3600.0
        
        # Apply direction
        if direction in ['S', 'W']:
            decimal = -decimal
        
        return True, decimal, ""
    
    # Try simple degrees and minutes: 40°42'N
    dm_pattern = r"(\d+)[°D]\s*(\d+(?:\.\d+)?)[\'M]?\s*([NSEW]?)"
    match = re.match(dm_pattern, coord_str)
    
    if match:
        degrees = int(match.group(1))
        minutes = float(match.group(2))
        direction = match.group(3)
        
        decimal = degrees + minutes/60.0
        
        if direction in ['S', 'W']:
            decimal = -decimal
        
        return True, decimal, ""
    
    return False, 0.0, f"Could not parse coordinate: {coord_str}"


def parse_location_input(location_str: str) -> LocationParseResult:
    """
    Parse various location input formats.
    
    Supports:
    - City names: "London", "New York", "San Francisco"
    - Coordinates: "40.7128, -74.0060"
    - Mixed formats: "40.7128N, 74.0060W"
    - DMS: "40°42'46\"N, 74°00'22\"W"
    
    Returns LocationParseResult with success/error information.
    """
    location_str = location_str.strip()
    
    if not location_str:
        return LocationParseResult(
            success=False,
            location=None,
            error_message="Location cannot be empty"
        )
    
    # Check if it's a known city
    city_key = location_str.lower()
    if city_key in CITY_COORDINATES:
        lat, lon, name = CITY_COORDINATES[city_key]
        return LocationParseResult(
            success=True,
            location=ObserverLocation(lat, lon, name),
            error_message=""
        )
    
    # Try to parse as coordinates
    if ',' in location_str:
        parts = location_str.split(',')
        if len(parts) == 2:
            lat_str, lon_str = parts
            
            # Parse latitude
            lat_success, lat_value, lat_error = parse_coordinate_string(lat_str)
            if not lat_success:
                return LocationParseResult(
                    success=False,
                    location=None,
                    error_message=f"Invalid latitude: {lat_error}"
                )
            
            # Parse longitude
            lon_success, lon_value, lon_error = parse_coordinate_string(lon_str)
            if not lon_success:
                return LocationParseResult(
                    success=False,
                    location=None,
                    error_message=f"Invalid longitude: {lon_error}"
                )
            
            # Validate ranges
            if not (-90 <= lat_value <= 90):
                return LocationParseResult(
                    success=False,
                    location=None,
                    error_message=f"Latitude must be between -90 and 90 degrees, got {lat_value}"
                )
            
            if not (-180 <= lon_value <= 180):
                return LocationParseResult(
                    success=False,
                    location=None,
                    error_message=f"Longitude must be between -180 and 180 degrees, got {lon_value}"
                )
            
            # Create descriptive name
            lat_dir = "N" if lat_value >= 0 else "S"
            lon_dir = "E" if lon_value >= 0 else "W"
            name = f"{abs(lat_value):.4f}°{lat_dir}, {abs(lon_value):.4f}°{lon_dir}"
            
            return LocationParseResult(
                success=True,
                location=ObserverLocation(lat_value, lon_value, name),
                error_message=""
            )
    
    # If we get here, it's an unknown format
    return LocationParseResult(
        success=False,
        location=None,
        error_message=f"Unknown location format: '{location_str}'. Try a city name or coordinates like '40.7128, -74.0060'"
    )


def suggest_similar_cities(input_str: str, max_suggestions: int = 5) -> List[str]:
    """
    Find city names similar to the input string.
    Pure function for providing helpful suggestions.
    """
    input_lower = input_str.lower()
    suggestions = []
    
    for city_key, (lat, lon, display_name) in CITY_COORDINATES.items():
        # Check if input is a substring of the city name
        if input_lower in city_key or any(word in city_key for word in input_lower.split()):
            suggestions.append(display_name)
    
    # Remove duplicates and limit
    unique_suggestions = list(dict.fromkeys(suggestions))
    return unique_suggestions[:max_suggestions]


def get_all_supported_cities() -> List[str]:
    """Get list of all supported city names for help display."""
    cities = [display_name for _, _, display_name in CITY_COORDINATES.values()]
    return sorted(list(set(cities)))


def format_location_help() -> str:
    """
    Generate help text for location input formats.
    Pure function for user guidance.
    """
    return """
Location Input Formats:

1. City Names:
   - London
   - New York
   - San Francisco
   - Tokyo

2. Decimal Coordinates:
   - 40.7128, -74.0060
   - -33.8688, 151.2093

3. Degrees/Minutes/Seconds:
   - 40°42'46"N, 74°00'22"W
   - 40d42m46sN, 74d00m22sW

4. Degrees and Minutes:
   - 40°42.8'N, 74°00.4'W

Note: Use negative values for South latitude and West longitude.
      Or use N/S/E/W direction indicators.
"""


def validate_location_for_astronomy(location: ObserverLocation) -> Tuple[bool, str]:
    """
    Validate if location is suitable for astronomical observations.
    Pure function checking practical constraints.
    """
    # Check for extreme latitudes where calculations might be unstable
    if abs(location.latitude) > 85:
        return False, f"Latitude {location.latitude}° is too close to the poles for reliable calculations"
    
    # Check for locations where some algorithms might have issues
    if abs(location.latitude) < 0.1 and abs(location.longitude) < 0.1:
        return False, "Location appears to be in the middle of the ocean (0°, 0°)"
    
    # All other locations are fine
    return True, ""


def get_location_info(location: ObserverLocation) -> Dict[str, str]:
    """
    Get descriptive information about a location.
    Pure function returning location metadata.
    """
    # Determine hemisphere
    lat_hemisphere = "Northern" if location.latitude >= 0 else "Southern"
    lon_hemisphere = "Eastern" if location.longitude >= 0 else "Western"
    
    # Determine climate zone (rough approximation)
    abs_lat = abs(location.latitude)
    if abs_lat <= 23.5:
        climate_zone = "Tropical"
    elif abs_lat <= 35:
        climate_zone = "Subtropical"
    elif abs_lat <= 50:
        climate_zone = "Temperate"
    elif abs_lat <= 66.5:
        climate_zone = "Subarctic/Subantarctic"
    else:
        climate_zone = "Arctic/Antarctic"
    
    # Determine visibility characteristics
    if abs_lat <= 35:
        visibility_note = "Can see both northern and southern sky objects"
    elif abs_lat <= 55:
        visibility_note = "Good view of circumpolar stars, limited southern sky"
    else:
        visibility_note = "Many circumpolar stars, very limited southern sky"
    
    return {
        "hemisphere": f"{lat_hemisphere} Hemisphere, {lon_hemisphere} Longitude",
        "climate_zone": climate_zone,
        "visibility": visibility_note,
        "latitude_dms": format_coordinate_dms(location.latitude, is_latitude=True),
        "longitude_dms": format_coordinate_dms(location.longitude, is_latitude=False)
    }


def format_coordinate_dms(coord: float, is_latitude: bool) -> str:
    """
    Format coordinate in degrees, minutes, seconds.
    Pure function for display formatting.
    """
    direction = ""
    if is_latitude:
        direction = "N" if coord >= 0 else "S"
    else:
        direction = "E" if coord >= 0 else "W"
    
    abs_coord = abs(coord)
    degrees = int(abs_coord)
    minutes_float = (abs_coord - degrees) * 60
    minutes = int(minutes_float)
    seconds = (minutes_float - minutes) * 60
    
    return f"{degrees}°{minutes:02d}'{seconds:05.2f}\"{direction}"
