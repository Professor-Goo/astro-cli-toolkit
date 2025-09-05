"""
Core data models for astronomical objects and calculations.
Built with functional programming principles - immutable data structures.
"""

from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime


@dataclass(frozen=True)
class StellarObject:
    """Immutable representation of a stellar object."""
    name: str
    ra_hours: float  # Right Ascension in hours (0-24)
    dec_degrees: float  # Declination in degrees (-90 to +90)
    magnitude: float  # Visual magnitude (lower = brighter)
    spectral_type: str  # Stellar classification (O, B, A, F, G, K, M)
    constellation: str  # Constellation name
    
    def __post_init__(self):
        """Validate data ranges."""
        if not (0 <= self.ra_hours <= 24):
            raise ValueError(f"RA must be 0-24 hours, got {self.ra_hours}")
        if not (-90 <= self.dec_degrees <= 90):
            raise ValueError(f"Dec must be -90 to +90 degrees, got {self.dec_degrees}")


@dataclass(frozen=True)
class ObserverLocation:
    """Immutable representation of an observer's location."""
    latitude: float  # Degrees North (-90 to +90)
    longitude: float  # Degrees East (-180 to +180)
    name: str  # Human-readable location name
    timezone_offset: float = 0.0  # Hours from UTC
    
    def __post_init__(self):
        """Validate coordinates."""
        if not (-90 <= self.latitude <= 90):
            raise ValueError(f"Latitude must be -90 to +90, got {self.latitude}")
        if not (-180 <= self.longitude <= 180):
            raise ValueError(f"Longitude must be -180 to +180, got {self.longitude}")


@dataclass(frozen=True)
class HorizontalCoordinates:
    """Immutable representation of horizontal (Alt/Az) coordinates."""
    altitude: float  # Degrees above horizon (0-90)
    azimuth: float  # Degrees from North (0-360)
    
    def __post_init__(self):
        """Validate ranges."""
        if not (0 <= self.altitude <= 90):
            raise ValueError(f"Altitude must be 0-90 degrees, got {self.altitude}")
        if not (0 <= self.azimuth <= 360):
            raise ValueError(f"Azimuth must be 0-360 degrees, got {self.azimuth}")


@dataclass(frozen=True)
class VisibilityInfo:
    """Immutable representation of object visibility data."""
    object_name: str
    is_visible: bool
    altitude: float
    azimuth: float
    rise_time: Optional[datetime] = None
    set_time: Optional[datetime] = None
    max_altitude_time: Optional[datetime] = None
    
    
@dataclass(frozen=True)
class SearchCriteria:
    """Immutable search criteria for filtering stellar objects."""
    max_magnitude: Optional[float] = None
    min_magnitude: Optional[float] = None
    constellation: Optional[str] = None
    spectral_types: Optional[List[str]] = None
    min_altitude: Optional[float] = None  # For visibility filtering
