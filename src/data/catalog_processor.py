"""
Functional data processing pipeline for star catalogs.
Demonstrates pure functions, immutable data, and error-as-data patterns.
"""

import csv
from dataclasses import dataclass
from typing import List, Optional, Tuple, Iterator
from pathlib import Path

from ..data.models import StellarObject


@dataclass(frozen=True)
class ParseResult:
    """Immutable result of parsing operation - error as data pattern."""
    success: bool
    data: Optional[List[StellarObject]]
    errors: List[str]
    total_records: int
    valid_records: int


@dataclass(frozen=True)
class CatalogEntry:
    """Raw catalog entry before validation."""
    name: str
    ra_hours: float
    dec_degrees: float
    magnitude: float
    spectral_type: str
    constellation: str


def read_catalog_file(filename: str) -> Iterator[dict]:
    """
    Pure generator function to read CSV file.
    Yields raw dictionary entries without processing.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                yield row
    except FileNotFoundError:
        # Generator that yields nothing for missing file
        return
        yield  # This line never executes but makes it a generator


def parse_catalog_entry(row: dict) -> Tuple[bool, Optional[CatalogEntry], str]:
    """
    Pure function to parse a single catalog row.
    Returns (success, entry, error_message).
    """
    try:
        entry = CatalogEntry(
            name=row.get('name', '').strip(),
            ra_hours=float(row.get('ra_hours', 0)),
            dec_degrees=float(row.get('dec_degrees', 0)),
            magnitude=float(row.get('magnitude', 0)),
            spectral_type=row.get('spectral_type', '').strip(),
            constellation=row.get('constellation', '').strip()
        )
        return True, entry, ""
    except (ValueError, TypeError) as e:
        return False, None, f"Parse error in row {row}: {str(e)}"


def validate_catalog_entry(entry: CatalogEntry) -> Tuple[bool, str]:
    """
    Pure function to validate catalog entry.
    Returns (is_valid, error_message).
    """
    errors = []
    
    # Validate name
    if not entry.name:
        errors.append("Missing name")
    
    # Validate RA (0-24 hours)
    if not (0 <= entry.ra_hours <= 24):
        errors.append(f"RA out of range: {entry.ra_hours}")
    
    # Validate Dec (-90 to +90 degrees)
    if not (-90 <= entry.dec_degrees <= 90):
        errors.append(f"Dec out of range: {entry.dec_degrees}")
    
    # Validate magnitude (reasonable range)
    if not (-2 <= entry.magnitude <= 7):
        errors.append(f"Magnitude out of range: {entry.magnitude}")
    
    # Validate constellation
    if not entry.constellation:
        errors.append("Missing constellation")
    
    if errors:
        return False, "; ".join(errors)
    
    return True, ""


def catalog_entry_to_stellar_object(entry: CatalogEntry) -> StellarObject:
    """
    Pure function to convert validated catalog entry to StellarObject.
    No validation needed here - entry is already validated.
    """
    return StellarObject(
        name=entry.name,
        ra_hours=entry.ra_hours,
        dec_degrees=entry.dec_degrees,
        magnitude=entry.magnitude,
        spectral_type=entry.spectral_type,
        constellation=entry.constellation
    )


def process_star_catalog(filename: str) -> ParseResult:
    """
    Main pipeline function - processes entire catalog using functional composition.
    Returns results as data, not exceptions (error-as-data pattern).
    """
    if not Path(filename).exists():
        return ParseResult(
            success=False,
            data=None,
            errors=[f"Catalog file not found: {filename}"],
            total_records=0,
            valid_records=0
        )
    
    stellar_objects = []
    errors = []
    total_records = 0
    valid_records = 0
    
    # Functional pipeline: read -> parse -> validate -> convert
    for row in read_catalog_file(filename):
        total_records += 1
        
        # Parse the row
        parse_success, entry, parse_error = parse_catalog_entry(row)
        if not parse_success:
            errors.append(f"Row {total_records}: {parse_error}")
            continue
        
        # Validate the entry
        valid, validation_error = validate_catalog_entry(entry)
        if not valid:
            errors.append(f"Row {total_records} ({entry.name}): {validation_error}")
            continue
        
        # Convert to stellar object
        stellar_object = catalog_entry_to_stellar_object(entry)
        stellar_objects.append(stellar_object)
        valid_records += 1
    
    return ParseResult(
        success=len(stellar_objects) > 0,
        data=stellar_objects if stellar_objects else None,
        errors=errors,
        total_records=total_records,
        valid_records=valid_records
    )


def filter_by_magnitude(
    stars: List[StellarObject], 
    max_magnitude: Optional[float] = None,
    min_magnitude: Optional[float] = None
) -> List[StellarObject]:
    """
    Pure function to filter stars by magnitude.
    Lower magnitude = brighter star.
    """
    filtered = stars
    
    if max_magnitude is not None:
        filtered = [star for star in filtered if star.magnitude <= max_magnitude]
    
    if min_magnitude is not None:
        filtered = [star for star in filtered if star.magnitude >= min_magnitude]
    
    return filtered


def filter_by_constellation(
    stars: List[StellarObject], 
    constellation: Optional[str] = None
) -> List[StellarObject]:
    """
    Pure function to filter stars by constellation.
    Case-insensitive partial matching.
    """
    if constellation is None:
        return stars
    
    constellation_lower = constellation.lower()
    return [
        star for star in stars 
        if constellation_lower in star.constellation.lower()
    ]


def filter_by_spectral_type(
    stars: List[StellarObject], 
    spectral_types: Optional[List[str]] = None
) -> List[StellarObject]:
    """
    Pure function to filter stars by spectral type.
    Matches first character of spectral type (O, B, A, F, G, K, M).
    """
    if not spectral_types:
        return stars
    
    # Convert to uppercase for comparison
    types_upper = [t.upper() for t in spectral_types]
    
    return [
        star for star in stars
        if star.spectral_type and star.spectral_type[0].upper() in types_upper
    ]


def sort_by_brightness(stars: List[StellarObject]) -> List[StellarObject]:
    """
    Pure function to sort stars by brightness (magnitude).
    Lower magnitude = brighter = appears first.
    """
    return sorted(stars, key=lambda star: star.magnitude)


def sort_by_name(stars: List[StellarObject]) -> List[StellarObject]:
    """Pure function to sort stars alphabetically by name."""
    return sorted(stars, key=lambda star: star.name)


def sort_by_constellation(stars: List[StellarObject]) -> List[StellarObject]:
    """Pure function to sort stars by constellation, then by brightness."""
    return sorted(stars, key=lambda star: (star.constellation, star.magnitude))


# Function composition helpers
def apply_filters(
    stars: List[StellarObject],
    max_magnitude: Optional[float] = None,
    min_magnitude: Optional[float] = None,
    constellation: Optional[str] = None,
    spectral_types: Optional[List[str]] = None
) -> List[StellarObject]:
    """
    Apply multiple filters in sequence using function composition.
    Each filter is a pure function that takes and returns a list.
    """
    result = stars
    
    # Apply filters in sequence
    result = filter_by_magnitude(result, max_magnitude, min_magnitude)
    result = filter_by_constellation(result, constellation)
    result = filter_by_spectral_type(result, spectral_types)
    
    return result
