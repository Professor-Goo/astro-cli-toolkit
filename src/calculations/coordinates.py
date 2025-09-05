"""
Pure functions for astronomical coordinate conversions.
No side effects, predictable outputs - perfect for functional programming.
"""

import math
from datetime import datetime, timezone
from typing import Tuple

from ..data.models import HorizontalCoordinates, ObserverLocation


def degrees_to_radians(degrees: float) -> float:
    """Convert degrees to radians."""
    return degrees * math.pi / 180.0


def radians_to_degrees(radians: float) -> float:
    """Convert radians to degrees."""
    return radians * 180.0 / math.pi


def hours_to_degrees(hours: float) -> float:
    """Convert hours to degrees (15 degrees per hour)."""
    return hours * 15.0


def degrees_to_hours(degrees: float) -> float:
    """Convert degrees to hours."""
    return degrees / 15.0


def calculate_julian_day(dt: datetime) -> float:
    """
    Calculate Julian Day Number from datetime.
    Pure function - same input always gives same output.
    """
    # Convert to UTC if timezone-aware
    if dt.tzinfo is not None:
        dt = dt.astimezone(timezone.utc).replace(tzinfo=None)
    
    year = dt.year
    month = dt.month
    day = dt.day
    hour = dt.hour + dt.minute/60.0 + dt.second/3600.0
    
    # Julian Day calculation
    if month <= 2:
        year -= 1
        month += 12
    
    a = year // 100
    b = 2 - a + a // 4
    
    jd = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + b - 1524.5 + hour/24.0
    
    return jd


def calculate_local_sidereal_time(dt: datetime, longitude: float) -> float:
    """
    Calculate Local Sidereal Time in hours.
    Pure function for time conversion.
    """
    jd = calculate_julian_day(dt)
    
    # Days since J2000.0
    d = jd - 2451545.0
    
    # Greenwich Mean Sidereal Time at 0h UT
    gmst = 18.697374558 + 24.06570982441908 * d
    
    # Normalize to 0-24 hours
    gmst = gmst % 24.0
    if gmst < 0:
        gmst += 24.0
    
    # Convert to Local Sidereal Time
    lst = gmst + longitude / 15.0
    lst = lst % 24.0
    if lst < 0:
        lst += 24.0
    
    return lst


def ra_dec_to_alt_az(
    ra_hours: float, 
    dec_degrees: float, 
    observer: ObserverLocation, 
    dt: datetime
) -> HorizontalCoordinates:
    """
    Convert Right Ascension/Declination to Altitude/Azimuth.
    
    This is the core coordinate conversion function - pure and predictable.
    
    Args:
        ra_hours: Right Ascension in hours (0-24)
        dec_degrees: Declination in degrees (-90 to +90)
        observer: Observer location
        dt: Observation time
        
    Returns:
        HorizontalCoordinates with altitude and azimuth
    """
    # Calculate Local Sidereal Time
    lst_hours = calculate_local_sidereal_time(dt, observer.longitude)
    
    # Hour Angle = LST - RA
    hour_angle_hours = lst_hours - ra_hours
    hour_angle_degrees = hour_angle_hours * 15.0
    
    # Convert to radians for trigonometry
    lat_rad = degrees_to_radians(observer.latitude)
    dec_rad = degrees_to_radians(dec_degrees)
    ha_rad = degrees_to_radians(hour_angle_degrees)
    
    # Calculate altitude
    sin_alt = (math.sin(dec_rad) * math.sin(lat_rad) + 
               math.cos(dec_rad) * math.cos(lat_rad) * math.cos(ha_rad))
    altitude_rad = math.asin(sin_alt)
    altitude_deg = radians_to_degrees(altitude_rad)
    
    # Calculate azimuth
    cos_az = ((math.sin(dec_rad) - math.sin(altitude_rad) * math.sin(lat_rad)) /
              (math.cos(altitude_rad) * math.cos(lat_rad)))
    
    # Clamp to avoid domain errors
    cos_az = max(-1.0, min(1.0, cos_az))
    azimuth_rad = math.acos(cos_az)
    azimuth_deg = radians_to_degrees(azimuth_rad)
    
    # Adjust azimuth quadrant based on hour angle
    if math.sin(ha_rad) > 0:
        azimuth_deg = 360.0 - azimuth_deg
    
    return HorizontalCoordinates(
        altitude=max(0.0, altitude_deg),  # Don't show negative altitudes
        azimuth=azimuth_deg % 360.0
    )


def is_object_visible(horizontal_coords: HorizontalCoordinates, min_altitude: float = 0.0) -> bool:
    """
    Determine if an object is visible above the horizon.
    Pure function - no side effects.
    """
    return horizontal_coords.altitude > min_altitude


def format_coordinates(ra_hours: float, dec_degrees: float) -> str:
    """
    Format coordinates in human-readable form.
    Pure function for display formatting.
    """
    # Convert RA to hours:minutes
    ra_h = int(ra_hours)
    ra_m = int((ra_hours - ra_h) * 60)
    
    # Convert Dec to degrees:minutes
    dec_sign = "+" if dec_degrees >= 0 else "-"
    dec_abs = abs(dec_degrees)
    dec_d = int(dec_abs)
    dec_m = int((dec_abs - dec_d) * 60)
    
    return f"RA {ra_h:02d}h{ra_m:02d}m, Dec {dec_sign}{dec_d:02d}°{dec_m:02d}'"
