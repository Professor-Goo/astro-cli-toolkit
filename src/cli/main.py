"""
Main CLI application using Click.
Demonstrates clean functional approach to command-line interfaces.
"""

import click
from datetime import datetime
from rich.console import Console
from rich.table import Table

from ..data.models import StellarObject, ObserverLocation
from ..calculations.coordinates import ra_dec_to_alt_az, format_coordinates

console = Console()


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """AstroCLI Toolkit - Astronomical data processing for stargazers."""
    pass


@cli.command()
@click.option("--ra", help="Right Ascension in hours (e.g., 14.5)")
@click.option("--dec", help="Declination in degrees (e.g., 25.3)")
@click.option("--lat", default=39.7392, help="Observer latitude (default: Denver)")
@click.option("--lon", default=-104.9903, help="Observer longitude (default: Denver)")
@click.option("--time", help="Observation time (YYYY-MM-DD HH:MM)")
def convert(ra, dec, lat, lon, time):
    """Convert RA/Dec coordinates to Alt/Az for your location."""
    
    if not ra or not dec:
        console.print("[red]Error: Both --ra and --dec are required[/red]")
        return
    
    try:
        ra_hours = float(ra)
        dec_degrees = float(dec)
        
        # Use current time if not specified
        obs_time = datetime.now() if not time else datetime.strptime(time, "%Y-%m-%d %H:%M")
        
        # Create observer location
        observer = ObserverLocation(
            latitude=lat,
            longitude=lon,
            name=f"Observer at {lat:.1f}°, {lon:.1f}°"
        )
        
        # Convert coordinates
        horizontal = ra_dec_to_alt_az(ra_hours, dec_degrees, observer, obs_time)
        
        # Display results
        table = Table(title="Coordinate Conversion Results")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="magenta")
        
        table.add_row("Input Coordinates", format_coordinates(ra_hours, dec_degrees))
        table.add_row("Observer Location", f"{lat:.4f}°N, {abs(lon):.4f}°W")
        table.add_row("Observation Time", obs_time.strftime("%Y-%m-%d %H:%M"))
        table.add_row("Altitude", f"{horizontal.altitude:.1f}°")
        table.add_row("Azimuth", f"{horizontal.azimuth:.1f}°")
        table.add_row("Visible?", "Yes" if horizontal.altitude > 0 else "No")
        
        console.print(table)
        
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")


@cli.command()
def demo():
    """Demonstrate the toolkit with some example stars."""
    
    # Create some sample stellar objects
    sample_stars = [
        StellarObject("Sirius", 6.75, -16.72, -1.46, "A1V", "Canis Major"),
        StellarObject("Vega", 18.62, 38.78, 0.03, "A0V", "Lyra"),
        StellarObject("Betelgeuse", 5.92, 7.41, 0.50, "M1-2 Ia-ab", "Orion"),
        StellarObject("Rigel", 5.24, -8.20, 0.13, "B8 Ia", "Orion"),
    ]
    
    # Default observer location (Denver)
    observer = ObserverLocation(39.7392, -104.9903, "Denver, CO")
    current_time = datetime.now()
    
    # Create results table
    table = Table(title=f"Star Visibility from {observer.name}")
    table.add_column("Star", style="cyan")
    table.add_column("Constellation", style="green")
    table.add_column("Magnitude", style="yellow")
    table.add_column("Altitude", style="magenta")
    table.add_column("Azimuth", style="blue")
    table.add_column("Visible?", style="red")
    
    for star in sample_stars:
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
            f"{horizontal.altitude:.1f}°",
            f"{horizontal.azimuth:.1f}°",
            visible
        )
    
    console.print(table)
    console.print(f"\n[dim]Calculated for {current_time.strftime('%Y-%m-%d %H:%M')} from {observer.name}[/dim]")


if __name__ == "__main__":
    cli()
