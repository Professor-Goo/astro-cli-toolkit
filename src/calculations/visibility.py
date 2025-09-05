"""
Advanced visibility calculations for stellar objects.
Pure functions for rise/set times, transit calculations, and visibility windows.
"""

import math
from datetime import datetime, timedelta, timezone
from typing import List, Optional, Tuple
from dataclasses import dataclass

from ..data.models import StellarObject, ObserverLocation, VisibilityInfo, HorizontalCoordinates
from .coordinates import ra_dec_to_alt_az, calculate_local_sidereal_time


@dataclass(frozen=True)
class RiseSetTimes:
    """Immutable rise/set time calculation results."""
    object_name: str
    rise_time: Optional[datetime]
    set_time: Optional[datetime]
    transit_time: Optional[datetime]
    max_altitude: float
    is_circumpolar: bool  # Never sets
    is_never_visible: bool  # Never rises


def calculate_hour_angle_for_altitude(
    dec_degrees: float, 
    observer_lat: float, 
    altitude: float = 0.0
) -> Optional[float]:
    """
    Pure function to calculate hour angle when object reaches given altitude.
    
    Args:
        dec_degrees: Declination of object
        observer_lat: Observer latitude
        altitude: Target altitude (0° for horizon)
        
    Returns:
        Hour angle in degrees, or None if never reaches altitude
    """
    # Convert to radians
    dec_rad = math.radians(dec_degrees)
    lat_rad = math.radians(observer_lat)
    alt_rad = math.radians(altitude)
    
    # Calculate hour angle using spherical trigonometry
    try:
        cos_ha = (math.sin(alt_rad) - math.sin(dec_rad) * math.sin(lat_rad)) / (
            math.cos(dec_rad) * math.cos(lat_rad)
        )
        
        # Check if object can reach this altitude
        if cos_ha < -1.0:
            # Object is circumpolar at this altitude
            return None
        elif cos_ha > 1.0:
            # Object never reaches this altitude
            return None
        else:
            # Calculate hour angle
            ha_rad = math.acos(cos_ha)
            return math.degrees(ha_rad)
            
    except (ValueError, ZeroDivisionError):
        return None


def calculate_transit_time(ra_hours: float, date, longitude: float) -> datetime:
    """
    Pure function to calculate when object crosses meridian (highest point).
    
    Args:
        ra_hours: Right Ascension in hours
        date: Date for calculation (datetime or date object)
        longitude: Observer longitude
        
    Returns:
        UTC datetime of transit
    """
    # Calculate Local Sidereal Time at midnight
    if hasattr(date, 'hour'):
        # It's a datetime object
        midnight_utc = date.replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        # It's a date object
        midnight_utc = datetime.combine(date, datetime.min.time())
    lst_midnight = calculate_local_sidereal_time(midnight_utc, longitude)
    
    # Transit occurs when LST = RA
    # So we need LST to advance from midnight value to RA
    hours_to_transit = ra_hours - lst_midnight
    
    # Handle day boundary crossing
    if hours_to_transit < 0:
        hours_to_transit += 24
    elif hours_to_transit >= 24:
        hours_to_transit -= 24
    
    # Convert sidereal hours to solar hours (sidereal day ≈ 23h 56m 4s)
    sidereal_to_solar = 23.934469591 / 24.0  # Ratio of sidereal to solar day
    solar_hours_to_transit = hours_to_transit * sidereal_to_solar
    
    transit_time = midnight_utc + timedelta(hours=solar_hours_to_transit)
    return transit_time


def calculate_rise_set_times(
    star: StellarObject, 
    observer: ObserverLocation, 
    date: datetime
) -> RiseSetTimes:
    """
    Calculate rise and set times for a stellar object.
    Pure function using spherical astronomy.
    
    Args:
        star: Stellar object
        observer: Observer location
        date: Date for calculation (time component ignored)
        
    Returns:
        RiseSetTimes with all timing information
    """
    # Calculate maximum altitude (at transit)
    # Max altitude occurs when hour angle = 0
    lat_rad = math.radians(observer.latitude)
    dec_rad = math.radians(star.dec_degrees)
    
    max_altitude_rad = math.asin(
        math.sin(dec_rad) * math.sin(lat_rad) + 
        math.cos(dec_rad) * math.cos(lat_rad)
    )
    max_altitude = math.degrees(max_altitude_rad)
    
    # Check for special cases
    is_circumpolar = (star.dec_degrees + observer.latitude) > 90
    is_never_visible = (star.dec_degrees + observer.latitude) < -90 or max_altitude < 0
    
    if is_never_visible:
        return RiseSetTimes(
            object_name=star.name,
            rise_time=None,
            set_time=None,
            transit_time=None,
            max_altitude=max_altitude,
            is_circumpolar=False,
            is_never_visible=True
        )
    
    # Calculate transit time
    transit_time = calculate_transit_time(star.ra_hours, date, observer.longitude)
    
    if is_circumpolar:
        return RiseSetTimes(
            object_name=star.name,
            rise_time=None,  # Always visible
            set_time=None,   # Never sets
            transit_time=transit_time,
            max_altitude=max_altitude,
            is_circumpolar=True,
            is_never_visible=False
        )
    
    # Calculate hour angle for horizon crossing (accounting for refraction)
    # Use -0.83° to account for atmospheric refraction and sun's diameter
    horizon_altitude = -0.5  # A bit below horizon for stars
    hour_angle_deg = calculate_hour_angle_for_altitude(
        star.dec_degrees, observer.latitude, horizon_altitude
    )
    
    if hour_angle_deg is None:
        # Shouldn't happen given our earlier checks, but handle gracefully
        return RiseSetTimes(
            object_name=star.name,
            rise_time=None,
            set_time=None,
            transit_time=transit_time,
            max_altitude=max_altitude,
            is_circumpolar=is_circumpolar,
            is_never_visible=is_never_visible
        )
    
    # Convert hour angle to time difference from transit
    hour_angle_hours = hour_angle_deg / 15.0  # 15° per hour
    sidereal_to_solar = 23.934469591 / 24.0
    
    time_before_transit = timedelta(hours=hour_angle_hours * sidereal_to_solar)
    time_after_transit = timedelta(hours=hour_angle_hours * sidereal_to_solar)
    
    rise_time = transit_time - time_before_transit
    set_time = transit_time + time_after_transit
    
    return RiseSetTimes(
        object_name=star.name,
        rise_time=rise_time,
        set_time=set_time,
        transit_time=transit_time,
        max_altitude=max_altitude,
        is_circumpolar=False,
        is_never_visible=False
    )


def calculate_visibility_for_time_range(
    stars: List[StellarObject],
    observer: ObserverLocation,
    start_time: datetime,
    end_time: datetime,
    min_altitude: float = 0.0,
    time_step_minutes: int = 60
) -> List[VisibilityInfo]:
    """
    Calculate visibility for multiple objects over a time range.
    Pure function that samples visibility at regular intervals.
    
    Args:
        stars: List of stellar objects
        observer: Observer location
        start_time: Start of time range
        end_time: End of time range
        min_altitude: Minimum altitude for visibility
        time_step_minutes: Time step for sampling
        
    Returns:
        List of VisibilityInfo for objects visible during the range
    """
    visible_objects = []
    
    for star in stars:
        # Sample visibility at several time points
        current_time = start_time
        max_altitude_seen = -90.0
        best_time = start_time
        ever_visible = False
        
        while current_time <= end_time:
            horizontal = ra_dec_to_alt_az(
                star.ra_hours,
                star.dec_degrees,
                observer,
                current_time
            )
            
            if horizontal.altitude > min_altitude:
                ever_visible = True
                
            if horizontal.altitude > max_altitude_seen:
                max_altitude_seen = horizontal.altitude
                best_time = current_time
                
            current_time += timedelta(minutes=time_step_minutes)
        
        if ever_visible:
            # Calculate final position for the best time
            best_horizontal = ra_dec_to_alt_az(
                star.ra_hours,
                star.dec_degrees,
                observer,
                best_time
            )
            
            # Calculate rise/set times for additional info
            rise_set = calculate_rise_set_times(star, observer, start_time.date())
            
            visible_objects.append(VisibilityInfo(
                object_name=star.name,
                is_visible=True,
                altitude=best_horizontal.altitude,
                azimuth=best_horizontal.azimuth,
                rise_time=rise_set.rise_time,
                set_time=rise_set.set_time,
                max_altitude_time=best_time
            ))
    
    # Sort by maximum altitude (brightest/highest first)
    return sorted(visible_objects, key=lambda x: x.altitude, reverse=True)


def calculate_current_visibility(
    stars: List[StellarObject],
    observer: ObserverLocation,
    observation_time: datetime,
    min_altitude: float = 0.0
) -> List[VisibilityInfo]:
    """
    Calculate current visibility for a list of stars.
    Pure function for real-time visibility checking.
    
    Args:
        stars: List of stellar objects
        observer: Observer location
        observation_time: Current time
        min_altitude: Minimum altitude for visibility
        
    Returns:
        List of VisibilityInfo for currently visible objects
    """
    visible_objects = []
    
    for star in stars:
        horizontal = ra_dec_to_alt_az(
            star.ra_hours,
            star.dec_degrees,
            observer,
            observation_time
        )
        
        if horizontal.altitude > min_altitude:
            # Calculate rise/set times for additional context
            rise_set = calculate_rise_set_times(star, observer, observation_time.date())
            
            visible_objects.append(VisibilityInfo(
                object_name=star.name,
                is_visible=True,
                altitude=horizontal.altitude,
                azimuth=horizontal.azimuth,
                rise_time=rise_set.rise_time,
                set_time=rise_set.set_time,
                max_altitude_time=rise_set.transit_time
            ))
    
    # Sort by altitude (highest first)
    return sorted(visible_objects, key=lambda x: x.altitude, reverse=True)


def filter_visible_objects(
    visibility_info: List[VisibilityInfo],
    min_altitude: float = 0.0,
    max_results: Optional[int] = None
) -> List[VisibilityInfo]:
    """
    Pure function to filter and limit visibility results.
    
    Args:
        visibility_info: List of visibility information
        min_altitude: Minimum altitude filter
        max_results: Maximum number of results to return
        
    Returns:
        Filtered and limited visibility information
    """
    # Filter by altitude
    filtered = [info for info in visibility_info if info.altitude >= min_altitude]
    
    # Limit results if requested
    if max_results is not None:
        filtered = filtered[:max_results]
    
    return filtered
