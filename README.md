# AstroCLI Toolkit 🌟

A command-line astronomical data processing toolkit for stargazers. Search star catalogs, calculate visibility, convert coordinates, and explore celestial objects using functional programming principles.

## Features

- **Coordinate Conversion**: Convert RA/Dec to Alt/Az for any location and time
- **Star Visibility**: Calculate which objects are visible from your location
- **Pure Functional Design**: Built with immutable data structures and pure functions
- **Rich CLI Interface**: Beautiful command-line output with tables and colors

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Try the demo
python main.py demo

# Convert coordinates for your location
python main.py convert --ra 6.75 --dec -16.72 --lat 39.7 --lon -104.9

# Get help
python main.py --help
```

## Example Output

```
Star Visibility from Denver, CO
┏━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┓
┃ Star      ┃ Constellation ┃ Magnitude ┃ Altitude ┃ Azimuth  ┃ Visible? ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━┩
│ Sirius    │ Canis Major   │ -1.46     │ 45.2°    │ 187.3°   │ ✓        │
│ Vega      │ Lyra          │ 0.03      │ 78.1°    │ 295.7°   │ ✓        │
└───────────┴───────────────┴───────────┴──────────┴──────────┴──────────┘
```

## Development Status

🚧 **Week 1 Complete**: Core calculation engine and basic CLI
- [x] Coordinate conversion functions
- [x] Immutable data models
- [x] Basic CLI commands
- [x] Demonstration mode

🎯 **Coming Next**:
- Real star catalog integration
- Search and filtering commands
- Rise/set time calculations
- Export functionality

## Technical Highlights

### Functional Programming Showcase
- **Pure Functions**: All calculations are side-effect free
- **Immutable Data**: Uses `@dataclass(frozen=True)` throughout
- **Function Composition**: Clean data processing pipelines
- **Predictable Behavior**: Same inputs always produce same outputs

### Architecture
```
src/
├── calculations/    # Pure mathematical functions
├── data/           # Immutable data structures
└── cli/            # Command-line interface
```

## License

MIT License - see LICENSE file for details.

## Contributing

This is a personal learning project following the Boot.dev curriculum. Feedback and suggestions welcome!
