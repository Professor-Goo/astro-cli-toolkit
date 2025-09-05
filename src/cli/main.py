"""
Enhanced CLI with search, visibility, and data processing commands.
Showcases functional programming with real astronomical data and flexible location input.
"""

import click
from datetime import datetime, timedelta
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from typing import List, Optional

from ..data.models import StellarObject, ObserverLocation, SearchCriteria
from ..data.catalog_processor import (
    process_star_catalog, apply_filters, sort_by_brightness, 
    sort_by_name, sort_by_constellation
)
from ..data.location_parser import parse_location_input
from ..calculations.coordinates import ra_dec_to_alt_az, format_coordinates
from ..calculations.visibility import (
    calculate_current_visibility, calculate_visibility_for_time_range,
    calculate_rise_set_times, filter_visible_objects
)

console = Console()

# Global catalog cache for performance
_star_catalog: Optional[List[StellarObject]] = None


def load_star_catalog() -> List[StellarObject]:
    """Load star catalog with caching for performance."""
    global _star_catalog
    
    if _star_catalog is not None:
        return _star_catalog
    
    # Try comprehensive catalog first, fall back to basic
    catalog_paths = [
        Path("data/comprehensive_star_catalog.csv"),
        Path("data/bright_stars_catalog.csv")
    ]
    
    for catalog_path in catalog_paths:
        if catalog_path.exists():
            with Progress() as progress:
                task = progress.add_task("Loading star catalog...", total=100)
                
                result = process_star_catalog(str(catalog_path))
                progress.update(task, completed=50)
                
                if not result.success:
                    console.print(f"[red]Error loading catalog:[/red]")
                    for error in result.errors[:5]:  # Show first 5 errors
                        console.print(f"  • {error}")
                    if len(result.errors) > 5:
                        console.print(f"  • ... and {len(result.errors) - 5} more errors")
                    continue
                
                progress.update(task, completed=100)
                
                _star_catalog = result.data
                console.print(f"[green]✅ Loaded {result.valid_records} stars from {catalog_path.name}[/green]")
                
                if result.errors:
                    console.print(f"[yellow]⚠️  {len(result.errors)} records had issues[/yellow]")
                
                return _star_catalog
    
    console.print("[red]Error: No star catalog found![/red]")
    console.print("Run: [cyan]python create_comprehensive_catalog.py[/cyan] to create the catalog")
    return []


def parse_observer_location(location_str: Optional[str]) -> ObserverLocation:
    """Parse location string or return default Denver location."""
    if not location_str:
        return ObserverLocation(39.7392, -104.9903, "Denver, CO (default)")
    
    result = parse_location_input(location_str)
    if result.success:
        return result.location
    else:
        console.print(f"[yellow]Warning: {result.error_message}[/yellow]")
        console.print("[yellow]Using default location: Denver, CO[/yellow]")
        return ObserverLocation(39.7392, -104.9903, "Denver, CO (default)")


@click.group()
@click.version_option(version="2.0.0")
def cli():
    """AstroCLI Toolkit - Astronomical data processing for stargazers with enhanced location support."""
    pass


@cli.command()
@click.option("--location", "-l", help="Observer location (city name or coordinates)")
def location(location):
    """Set or validate observer location with detailed information."""
    
    if not location:
        console.print("[yellow]Please specify a location[/yellow]")
        console.print("\nExamples:")
        console.print("  astro location -l London")
        console.print("  astro location -l \"New York\"")
        console.print("  astro location -l \"40.7128, -74.0060\"")
        console.print("  astro location -l \"40°42'46\"N, 74°00'22\"W\"")
        return
    
    from ..data.location_parser import (
        parse_location_input, validate_location_for_astronomy, 
        get_location_info, suggest_similar_cities
    )
    
    # Parse the location
    result = parse_location_input(location)
    
    if not result.success:
        console.print(f"[red]Error: {result.error_message}[/red]")
        
        # Provide suggestions for city names
        if "Unknown location format" in result.error_message:
            suggestions = suggest_similar_cities(location)
            if suggestions:
                console.print("\n[yellow]Did you mean one of these?[/yellow]")
                for suggestion in suggestions:
                    console.print(f"  • {suggestion}")
        return
    
    observer = result.location
    
    # Validate for astronomy
    valid, validation_message = validate_location_for_astronomy(observer)
    if not valid:
        console.print(f"[red]Warning: {validation_message}[/red]")
        return
    
    # Get location information
    location_info = get_location_info(observer)
    
    # Create detailed information table
    table = Table(title=f"Location Information: {observer.name}")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="magenta")
    
    table.add_row("Location Name", observer.name)
    table.add_row("Latitude (Decimal)", f"{observer.latitude:.6f}°")
    table.add_row("Longitude (Decimal)", f"{observer.longitude:.6f}°")
    table.add_row("Latitude (DMS)", location_info["latitude_dms"])
    table.add_row("Longitude (DMS)", location_info["longitude_dms"])
    table.add_row("Hemisphere", location_info["hemisphere"])
    table.add_row("Climate Zone", location_info["climate_zone"])
    table.add_row("Sky Visibility", location_info["visibility"])
    
    console.print(table)
    
    # Show currently visible bright stars as example
    console.print("\n[dim]Checking current visibility...[/dim]")
    
    stars = load_star_catalog()
    if stars:
        current_time = datetime.now()
        bright_stars = [star for star in stars if star.magnitude <= 2.0]
        
        visibility_info = calculate_current_visibility(
            bright_stars, observer, current_time, min_altitude=15.0
        )
        
        if visibility_info:
            console.print(f"\n✨ {len(visibility_info)} bright stars currently visible above 15°:")
            for i, info in enumerate(visibility_info[:5]):  # Show top 5
                console.print(f"  {i+1}. {info.object_name} ({info.altitude:.1f}°)")
            if len(visibility_info) > 5:
                console.print(f"  ... and {len(visibility_info) - 5} more")
        else:
            console.print("\n[yellow]No bright stars currently visible above 15°[/yellow]")


@cli.command()
@click.option("--mag-limit", type=float, help="Maximum magnitude (brighter stars)")
@click.option("--min-mag", type=float, help="Minimum magnitude (dimmer stars)")
@click.option("--constellation", help="Filter by constellation name")
@click.option("--spectral-type", help="Filter by spectral type (e.g., 'O,B,A')")
@click.option("--sort-by", type=click.Choice(['brightness', 'name', 'constellation']), 
              default='brightness', help="Sort results by")
@click.option("--limit", type=int, default=20, help="Maximum number of results")
@click.option("--visible-now", is_flag=True, help="Show only currently visible stars")
@click.option("--location", "-l", help="Observer location (city name or coordinates)")
@click.option("--min-altitude", default=0.0, help="Minimum altitude for visibility")
def search(mag_limit, min_mag, constellation, spectral_type, sort_by, limit, 
           visible_now, location, min_altitude):
    """Search the star catalog with powerful filtering options."""
    
    # Load the star catalog
    stars = load_star_catalog()
    if not stars:
        return
    
    # Parse spectral types if provided
    spectral_types_list = None
    if spectral_type:
        spectral_types_list = [t.strip().upper() for t in spectral_type.split(',')]
    
    # Apply filters using functional composition
    filtered_stars = apply_filters(
        stars=stars,
        max_magnitude=mag_limit,
        min_magnitude=min_mag,
        constellation=constellation,
        spectral_types=spectral_types_list
    )
    
    # Apply visibility filter if requested
    if visible_now:
        observer = parse_observer_location(location)
        current_time = datetime.now()
        
        # Calculate current visibility
        visibility_info = calculate_current_visibility(
            filtered_stars, observer, current_time, min_altitude
        )
        
        # Extract the stellar objects that are visible
        visible_star_names = {info.object_name for info in visibility_info}
        filtered_stars = [star for star in filtered_stars if star.name in visible_star_names]
    
    # Sort results
    if sort_by == 'brightness':
        filtered_stars = sort_by_brightness(filtered_stars)
    elif sort_by == 'name':
        filtered_stars = sort_by_name(filtered_stars)
    elif sort_by == 'constellation':
        filtered_stars = sort_by_constellation(filtered_stars)
    
    # Limit results
    filtered_stars = filtered_stars[:limit]
    
    if not filtered_stars:
        console.print("[yellow]No stars match your search criteria.[/yellow]")
        return
    
    # Create results table
    title = "Star Search Results"
    if visible_now:
        observer = parse_observer_location(location)
        title += f" (Visible Now from {observer.name})"
    
    table = Table(title=title)
    table.add_column("Star", style="cyan")
    table.add_column("Constellation", style="green")
    table.add_column("Magnitude", style="yellow", justify="right")
    table.add_column("Spectral Type", style="blue")
    table.add_column("Coordinates", style="magenta")
    
    if visible_now:
        table.add_column("Altitude", style="red", justify="right")
        table.add_column("Azimuth", style="red", justify="right")
    
    for star in filtered_stars:
        coords = format_coordinates(star.ra_hours, star.dec_degrees)
        
        if visible_now:
            # Calculate current position
            observer = parse_observer_location(location)
            horizontal = ra_dec_to_alt_az(star.ra_hours, star.dec_degrees, observer, datetime.now())
            
            table.add_row(
                star.name,
                star.constellation,
                f"{star.magnitude:.2f}",
                star.spectral_type,
                coords,
                f"{horizontal.altitude:.1f}°",
                f"{horizontal.azimuth:.1f}°"
            )
        else:
            table.add_row(
                star.name,
                star.constellation,
                f"{star.magnitude:.2f}",
                star.spectral_type,
                coords
            )
    
    console.print(table)
    console.print(f"\n[dim]Found {len(filtered_stars)} stars matching criteria[/dim]")


@cli.command()
@click.option("--location", "-l", help="Observer location (city name or coordinates)")
@click.option("--date", help="Date for calculation (YYYY-MM-DD)")
@click.option("--time-range", help="Time range (e.g., '20:00-06:00' for tonight)")
@click.option("--min-altitude", default=15.0, help="Minimum altitude for visibility")
@click.option("--mag-limit", default=3.0, help="Magnitude limit (brighter stars only)")
@click.option("--limit", default=15, help="Maximum number of results")
def visible(location, date, time_range, min_altitude, mag_limit, limit):
    """Calculate which stars are visible from your location."""
    
    # Load catalog
    stars = load_star_catalog()
    if not stars:
        return
    
    # Parse location
    observer = parse_observer_location(location)
    
    # Filter by magnitude first to reduce computation
    bright_stars = apply_filters(stars, max_magnitude=mag_limit)
    
    # Parse date
    if date:
        try:
            obs_date = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            console.print("[red]Error: Date must be in YYYY-MM-DD format[/red]")
            return
    else:
        obs_date = datetime.now()
    
    # Calculate visibility
    if time_range:
        # Parse time range like "20:00-06:00"
        try:
            start_str, end_str = time_range.split('-')
            start_hour, start_min = map(int, start_str.split(':'))
            end_hour, end_min = map(int, end_str.split(':'))
            
            start_time = obs_date.replace(hour=start_hour, minute=start_min, second=0)
            
            if end_hour < start_hour:  # Crosses midnight
                end_time = (obs_date + timedelta(days=1)).replace(hour=end_hour, minute=end_min, second=0)
            else:
                end_time = obs_date.replace(hour=end_hour, minute=end_min, second=0)
            
            visibility_info = calculate_visibility_for_time_range(
                bright_stars, observer, start_time, end_time, min_altitude, time_step_minutes=30
            )
            
            title = f"Stars Visible {time_range} from {observer.name}"
            
        except ValueError:
            console.print("[red]Error: Time range must be in HH:MM-HH:MM format[/red]")
            return
    else:
        # Current visibility
        visibility_info = calculate_current_visibility(
            bright_stars, observer, obs_date, min_altitude
        )
        title = f"Currently Visible Stars from {observer.name}"
    
    # Filter and limit results
    visible_objects = filter_visible_objects(visibility_info, min_altitude, limit)
    
    if not visible_objects:
        console.print(f"[yellow]No stars visible above {min_altitude}° altitude.[/yellow]")
        return
    
    # Create visibility table
    table = Table(title=title)
    table.add_column("Star", style="cyan")
    table.add_column("Altitude", style="yellow", justify="right")
    table.add_column("Azimuth", style="blue", justify="right")
    table.add_column("Rise Time", style="green")
    table.add_column("Set Time", style="red")
    table.add_column("Transit", style="magenta")
    
    for info in visible_objects:
        rise_str = info.rise_time.strftime("%H:%M") if info.rise_time else "Circumpolar"
        set_str = info.set_time.strftime("%H:%M") if info.set_time else "Circumpolar"
        transit_str = info.max_altitude_time.strftime("%H:%M") if info.max_altitude_time else "N/A"
        
        table.add_row(
            info.object_name,
            f"{info.altitude:.1f}°",
            f"{info.azimuth:.1f}°",
            rise_str,
            set_str,
            transit_str
        )
    
    console.print(table)
    console.print(f"\n[dim]Showing {len(visible_objects)} stars above {min_altitude}° altitude[/dim]")


@cli.command()
@click.argument("object_name")
@click.option("--location", "-l", help="Observer location (city name or coordinates)")
@click.option("--date", help="Date for calculation (YYYY-MM-DD)")
def times(object_name, location, date):
    """Calculate rise, set, and transit times for a specific object."""
    
    # Load catalog
    stars = load_star_catalog()
    if not stars:
        return
    
    # Parse location
    observer = parse_observer_location(location)
    
    # Find the requested star
    matching_stars = [star for star in stars if object_name.lower() in star.name.lower()]
    
    if not matching_stars:
        console.print(f"[red]No star found matching '{object_name}'[/red]")
        
        # Suggest similar names
        suggestions = [star.name for star in stars if 
                      any(part.lower() in star.name.lower() for part in object_name.lower().split())]
        if suggestions:
            console.print("Did you mean one of these?")
            for suggestion in suggestions[:5]:
                console.print(f"  • {suggestion}")
        return
    
    if len(matching_stars) > 1:
        console.print(f"Multiple stars match '{object_name}':")
        for star in matching_stars:
            console.print(f"  • {star.name} ({star.constellation})")
        console.print("Please be more specific.")
        return
    
    star = matching_stars[0]
    
    # Parse date
    if date:
        try:
            obs_date = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            console.print("[red]Error: Date must be in YYYY-MM-DD format[/red]")
            return
    else:
        obs_date = datetime.now()
    
    # Calculate rise/set times
    rise_set = calculate_rise_set_times(star, observer, obs_date)
    
    # Create detailed information table
    table = Table(title=f"Timing Information for {star.name}")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="magenta")
    
    table.add_row("Star Name", star.name)
    table.add_row("Constellation", star.constellation)
    table.add_row("Magnitude", f"{star.magnitude:.2f}")
    table.add_row("Spectral Type", star.spectral_type)
    table.add_row("Coordinates", format_coordinates(star.ra_hours, star.dec_degrees))
    table.add_row("Observer Location", observer.name)
    table.add_row("Date", obs_date.strftime("%Y-%m-%d"))
    
    if rise_set.is_never_visible:
        table.add_row("Status", "[red]Never visible from this location[/red]")
    elif rise_set.is_circumpolar:
        table.add_row("Status", "[green]Circumpolar (always visible)[/green]")
        table.add_row("Transit Time", rise_set.transit_time.strftime("%H:%M UTC") if rise_set.transit_time else "N/A")
        table.add_row("Maximum Altitude", f"{rise_set.max_altitude:.1f}°")
    else:
        table.add_row("Rise Time", rise_set.rise_time.strftime("%H:%M UTC") if rise_set.rise_time else "N/A")
        table.add_row("Transit Time", rise_set.transit_time.strftime("%H:%M UTC") if rise_set.transit_time else "N/A")
        table.add_row("Set Time", rise_set.set_time.strftime("%H:%M UTC") if rise_set.set_time else "N/A")
        table.add_row("Maximum Altitude", f"{rise_set.max_altitude:.1f}°")
    
    console.print(table)


@cli.command()
@click.option("--ra", help="Right Ascension in hours (e.g., 14.5)")
@click.option("--dec", help="Declination in degrees (e.g., 25.3)")
@click.option("--location", "-l", help="Observer location (city name or coordinates)")
@click.option("--time", help="Observation time (YYYY-MM-DD HH:MM)")
def convert(ra, dec, location, time):
    """Convert RA/Dec coordinates to Alt/Az for your location."""
    
    if not ra or not dec:
        console.print("[red]Error: Both --ra and --dec are required[/red]")
        return
    
    try:
        ra_hours = float(ra)
        dec_degrees = float(dec)
        
        # Parse location
        observer = parse_observer_location(location)
        
        # Use current time if not specified
        obs_time = datetime.now() if not time else datetime.strptime(time, "%Y-%m-%d %H:%M")
        
        # Convert coordinates
        horizontal = ra_dec_to_alt_az(ra_hours, dec_degrees, observer, obs_time)
        
        # Display results
        table = Table(title="Coordinate Conversion Results")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="magenta")
        
        table.add_row("Input Coordinates", format_coordinates(ra_hours, dec_degrees))
        table.add_row("Observer Location", observer.name)
        table.add_row("Observation Time", obs_time.strftime("%Y-%m-%d %H:%M"))
        table.add_row("Altitude", f"{horizontal.altitude:.1f}°")
        table.add_row("Azimuth", f"{horizontal.azimuth:.1f}°")
        table.add_row("Visible?", "Yes" if horizontal.altitude > 0 else "No")
        
        console.print(table)
        
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")


@cli.command()
@click.option("--constellation", help="Show only stars from specific constellation")
@click.option("--location", "-l", help="Observer location (city name or coordinates)")
@click.option("--limit", default=10, help="Number of stars to show")
def demo(constellation, location, limit):
    """Demonstrate the toolkit with real star data."""
    
    # Load the full catalog
    stars = load_star_catalog()
    if not stars:
        return
    
    # Parse location
    observer = parse_observer_location(location)
    
    # Filter by constellation if specified
    if constellation:
        demo_stars = apply_filters(stars, constellation=constellation)
        demo_stars = sort_by_brightness(demo_stars)[:limit]
        title_suffix = f" from {constellation}"
    else:
        # Show brightest stars overall
        demo_stars = sort_by_brightness(stars)[:limit]
        title_suffix = " (Brightest Stars)"
    
    if not demo_stars:
        console.print(f"[yellow]No stars found for constellation '{constellation}'[/yellow]")
        return
    
    current_time = datetime.now()
    
    # Create results table
    table = Table(title=f"Star Visibility from {observer.name}{title_suffix}")
    table.add_column("Star", style="cyan")
    table.add_column("Constellation", style="green")
    table.add_column("Magnitude", style="yellow", justify="right")
    table.add_column("Spectral Type", style="blue")
    table.add_column("Altitude", style="magenta", justify="right")
    table.add_column("Azimuth", style="red", justify="right")
    table.add_column("Visible?", style="white")
    
    for star in demo_stars:
        horizontal = ra_dec_to_alt_az(
            star.ra_hours, 
            star.dec_degrees, 
            observer, 
            current_time
        )
        
        visible = "✓" if horizontal.altitude > 0 else "✗"
        
        table.add_row(
            star.name,
            star.constellation,
            f"{star.magnitude:.2f}",
            star.spectral_type,
            f"{horizontal.altitude:.1f}°",
            f"{horizontal.azimuth:.1f}°",
            visible
        )
    
    console.print(table)
    console.print(f"\n[dim]Calculated for {current_time.strftime('%Y-%m-%d %H:%M')} from {observer.name}[/dim]")
    console.print(f"[dim]Showing {len(demo_stars)} stars from catalog of {len(stars)} total[/dim]")


if __name__ == "__main__":
    cli()
