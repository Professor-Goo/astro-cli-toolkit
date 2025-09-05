#!/usr/bin/env python3
"""
Entry point for AstroCLI Toolkit.
Run with: python main.py
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.cli.main import cli

if __name__ == "__main__":
    cli()
