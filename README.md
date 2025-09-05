# AstroCLI Toolkit 🌟

A comprehensive command-line astronomical data processing toolkit for stargazers worldwide. Search through 167+ real stars, calculate visibility from any global location, and explore celestial objects using advanced functional programming principles.

## ✨ Features

### 🌍 **Flexible Location System**
- **Major World Cities**: "London", "Tokyo", "Sydney", "New York"
- **Decimal Coordinates**: "40.7128, -74.0060"
- **DMS Format**: "40°42'46\"N, 74°00'22\"W"
- **Intelligent Parsing**: Automatic validation with helpful error suggestions

### 🌟 **Comprehensive Star Database**
- **167 Stars** across **36 Constellations**
- **Complete Seasonal Coverage**: Spring, Summer, Autumn, Winter stars
- **Circumpolar Objects**: Year-round visible stars for northern latitudes
- **Real Astronomical Data**: Accurate positions, magnitudes, and spectral classifications

### 🔍 **Powerful Search & Filtering**
- **Multi-Criteria Search**: Magnitude, constellation, spectral type combinations
- **Real-Time Visibility**: Show only currently visible stars from your location
- **Spectral Classification**: Find O, B, A, F, G, K, M type stars
- **Advanced Sorting**: By brightness, name, or constellation

### ⏰ **Professional Timing Calculations**
- **Rise/Set Times**: Precise calculations using spherical astronomy
- **Transit Times**: When objects reach maximum altitude
- **Visibility Windows**: What's visible during specific time ranges
- **Circumpolar Detection**: Identifies always-visible objects

### 🎯 **Advanced Visibility Analysis**
- **Time Range Queries**: "What's visible tonight 8pm-6am?"
- **Altitude Filtering**: Minimum elevation requirements
- **Global Calculations**: Accurate for any location worldwide
- **Current Conditions**: Real-time sky analysis

## 🚀 Quick Start

```bash
# 1. Create comprehensive star catalog
python create_comprehensive_catalog.py

# 2. Install dependencies
pip install -r requirements.txt

# 3. Try location-aware demo
python main.py demo --location London

# 4. Check what's visible now from your city
python main.py search --visible-now --location "New York" --min-altitude 20
```

## 🌍 Global Usage Examples

```bash
# Location validation and information
python main.py location -l "Tokyo"
python main.py location -l "51.5074, -0.1278"

# Search from different global locations
python main.py search --constellation Orion --location Tokyo --visible-now
python main.py search --spectral-type "O,B" --location Sydney --mag-limit 3.0

# Visibility analysis from any city
python main.py visible --location London --time-range "20:00-06:00"
python main.py visible --location "35.6762, 139.6503" --min-altitude 15

# Precise timing for any location
python main.py times Vega --location Tokyo
python main.py times Sirius --location "Sydney"

# Coordinate conversion with flexible location input
python main.py convert --ra 18.6 --dec 38.8 --location "London"
```

## 📊 Example Output

### Real-Time Visibility from London
```
Star Search Results (Visible Now from London, UK)
┏━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┓
┃ Star      ┃ Constellation ┃ Magnitude ┃ Spectral Type ┃ Altitude ┃ Azimuth ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━┩
│ Vega      │ Lyra          │      0.03 │ A0V           │    46.8° │  277.5° │
│ Deneb     │ Cygnus        │      1.25 │ A2Ia          │    69.7° │  263.7° │
│ Polaris   │ Ursa Minor    │      1.98 │ F7Ib          │    51.9° │    1.0° │
└───────────┴───────────────┴───────────┴───────────────┴──────────┴─────────┘
```

### Precise Timing Information
```
Timing Information for Vega (from Tokyo, Japan)
┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Property          ┃ Value                  ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Rise Time         │ 01:59 UTC              │
│ Transit Time      │ 10:23 UTC              │
│ Set Time          │ 18:46 UTC              │
│ Maximum Altitude  │ 86.9°                  │
└───────────────────┴────────────────────────┘
```

## 🏗️ Technical Architecture

### Functional Programming Excellence
- **Pure Functions**: All astronomical calculations are side-effect free
- **Immutable Data**: Uses `@dataclass(frozen=True)` throughout
- **Function Composition**: Clean data processing pipelines
- **Error-as-Data**: Robust error handling without exceptions
- **Referential Transparency**: Predictable, testable code

### Project Structure
```
astro-cli-toolkit/
├── src/
│   ├── calculations/          # Pure mathematical functions
│   │   ├── coordinates.py     # Coordinate conversions (RA/Dec ↔ Alt/Az)
│   │   └── visibility.py      # Rise/set times, visibility windows
│   ├── data/
│   │   ├── models.py          # Immutable data structures
│   │   ├── catalog_processor.py # Functional data pipelines
│   │   └── location_parser.py # Global location handling
│   └── cli/
│       └── main.py            # Enhanced command-line interface
├── data/
│   └── comprehensive_star_catalog.csv # 167 stars, 36 constellations
├── tests/                     # Unit tests
└── README.md
```

## 📈 Development Status

✅ **Complete**: Core calculation engine  
✅ **Complete**: Real star data integration  
✅ **Complete**: Global location system & enhanced catalog  

### Current Capabilities
- [x] 167+ real stars with accurate astronomical data
- [x] 36 constellation systematic coverage
- [x] Global location parsing (cities + coordinates)
- [x] Real-time visibility calculations
- [x] Rise/set time calculations using spherical astronomy
- [x] Multi-criteria search and filtering
- [x] Professional CLI with rich output formatting
- [x] Comprehensive error handling and validation

### Astronomical Data Coverage
- **Circumpolar**: Ursa Major, Ursa Minor, Cassiopeia, Cepheus, Draco
- **Spring**: Leo, Virgo, Boötes, Libra
- **Summer**: Scorpius, Sagittarius, Lyra, Cygnus, Aquila, Hercules, Ophiuchus
- **Autumn**: Pegasus, Andromeda, Perseus, Aquarius, Capricornus
- **Winter**: Orion, Canis Major, Canis Minor, Gemini, Taurus, Auriga
- **Southern**: Centaurus, Crux, Carina, Eridanus, Grus, Piscis Austrinus

## 🎯 Key Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `location` | Validate and analyze observer location | `python main.py location -l "Tokyo"` |
| `search` | Find stars with multiple criteria | `python main.py search --visible-now --location London` |
| `visible` | Calculate visibility windows | `python main.py visible --location Tokyo --time-range "20:00-06:00"` |
| `times` | Get rise/set times for specific objects | `python main.py times Vega --location Sydney` |
| `convert` | Transform coordinates between systems | `python main.py convert --ra 18.6 --dec 38.8 --location Berlin` |
| `demo` | Interactive demonstration | `python main.py demo --constellation Orion --location Paris` |

## 🌐 Global Location Support

### Supported Cities (80+ major cities worldwide)
**North America**: New York, Los Angeles, Chicago, Toronto, Mexico City  
**Europe**: London, Paris, Berlin, Rome, Stockholm, Moscow  
**Asia**: Tokyo, Beijing, Mumbai, Singapore, Seoul  
**Australia/Oceania**: Sydney, Melbourne, Auckland  
**South America**: São Paulo, Buenos Aires, Santiago  
**Africa**: Cairo, Cape Town, Nairobi  

### Coordinate Formats
- **Decimal**: `40.7128, -74.0060`
- **DMS**: `40°42'46"N, 74°00'22"W`
- **Alternative**: `40d42m46sN, 74d00m22sW`

## 🧪 Functional Programming Showcase

This project demonstrates advanced functional programming concepts:

```python
# Pure function composition for data processing
def search_stars(catalog: List[StellarObject], criteria: SearchCriteria) -> List[StellarObject]:
    return (catalog
            |> filter_by_magnitude(criteria.max_magnitude)
            |> filter_by_constellation(criteria.constellation)
            |> filter_by_spectral_type(criteria.spectral_types)
            |> sort_by_brightness)

# Error-as-data pattern for robust parsing
@dataclass(frozen=True)
class LocationParseResult:
    success: bool
    location: Optional[ObserverLocation]
    error_message: str

# Immutable data transformations throughout
def calculate_current_visibility(
    stars: List[StellarObject],
    observer: ObserverLocation,
    observation_time: datetime
) -> List[VisibilityInfo]:
    return [calculate_object_visibility(star, observer, observation_time) 
            for star in stars]
```

## 🤝 Contributing

This is a personal learning project following the Boot.dev functional programming curriculum. The project demonstrates:
- Advanced functional programming patterns in Python
- Real-world astronomical data processing
- Professional CLI application development
- Global coordinate system handling

Built with love for astronomy and clean code! 🌟

---

*"The universe is not only stranger than we imagine, it is stranger than we can imagine." - J.B.S. Haldane*