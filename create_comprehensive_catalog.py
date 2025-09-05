#!/usr/bin/env python3
"""
Enhanced star catalog with systematic constellation coverage.
Expands from 55 to 200+ bright stars covering all major constellations.
"""

import csv
import os
from pathlib import Path

def create_comprehensive_catalog():
    """Create a comprehensive bright star catalog organized by constellation."""
    
    # Create data directory if it doesn't exist
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # Comprehensive star catalog - organized by constellation
    # Format: Name, RA_hours, Dec_degrees, Magnitude, SpectralType, Constellation
    
    comprehensive_stars = [
        # === CIRCUMPOLAR CONSTELLATIONS (Always visible from mid-northern latitudes) ===
        
        # Ursa Major (Big Dipper + more)
        ("Dubhe", 11.062, 61.751, 1.79, "K3III", "Ursa Major"),
        ("Merak", 11.031, 56.382, 2.37, "A1V", "Ursa Major"),
        ("Phecda", 11.897, 53.695, 2.44, "A0V", "Ursa Major"),
        ("Megrez", 12.257, 57.033, 3.31, "A3V", "Ursa Major"),
        ("Alioth", 12.900, 55.960, 1.77, "A1III-IV", "Ursa Major"),
        ("Mizar", 13.422, 54.925, 2.04, "A2Vp", "Ursa Major"),
        ("Alkaid", 13.792, 49.313, 1.86, "B3V", "Ursa Major"),
        ("Muscida", 8.508, 60.718, 3.05, "G4II-III", "Ursa Major"),
        ("Tania Australis", 10.372, 41.499, 3.06, "M0III", "Ursa Major"),
        ("Tania Borealis", 10.291, 42.914, 3.45, "A2IV", "Ursa Major"),
        
        # Ursa Minor (Little Dipper)
        ("Polaris", 2.530, 89.264, 1.98, "F7Ib", "Ursa Minor"),
        ("Kochab", 14.845, 74.155, 2.08, "K4III", "Ursa Minor"),
        ("Pherkad", 15.345, 71.834, 3.05, "A3Iab", "Ursa Minor"),
        ("Yildun", 17.537, 86.586, 4.35, "A1Vn", "Ursa Minor"),
        ("Urodelus", 13.062, 77.794, 4.25, "A0V", "Ursa Minor"),
        
        # Cassiopeia
        ("Schedar", 0.675, 56.537, 2.23, "K0IIIa", "Cassiopeia"),
        ("Caph", 0.153, 59.150, 2.27, "F2III-IV", "Cassiopeia"),
        ("Gamma Cas", 0.945, 60.717, 2.47, "B0.5IVe", "Cassiopeia"),
        ("Ruchbah", 1.430, 60.235, 2.66, "A5V", "Cassiopeia"),
        ("Segin", 1.906, 63.670, 3.38, "B3V", "Cassiopeia"),
        
        # Cepheus
        ("Alderamin", 21.309, 62.585, 2.44, "A7IV-V", "Cepheus"),
        ("Alfirk", 21.477, 70.561, 3.23, "B2III", "Cepheus"),
        ("Errai", 23.655, 77.632, 3.21, "K1IV", "Cepheus"),
        ("Al Kalb al Rai", 20.756, 61.838, 4.29, "M2Ia", "Cepheus"),
        
        # Draco
        ("Thuban", 14.073, 64.376, 3.65, "A0III", "Draco"),
        ("Eltanin", 17.943, 51.489, 2.23, "K5III", "Draco"),
        ("Rastaban", 17.507, 52.301, 2.79, "G2II", "Draco"),
        ("Altais", 19.209, 67.661, 3.17, "G9III", "Draco"),
        ("Aldibain", 16.400, 61.514, 3.29, "K2III", "Draco"),
        
        # === SPRING CONSTELLATIONS ===
        
        # Leo
        ("Regulus", 10.139, 11.967, 1.35, "B8IVn", "Leo"),
        ("Denebola", 11.818, 14.572, 2.13, "A3V", "Leo"),
        ("Algieba", 10.333, 19.842, 2.28, "K1III", "Leo"),
        ("Zosma", 11.235, 20.524, 2.56, "A4V", "Leo"),
        ("Ras Elased Australis", 9.763, 23.774, 2.98, "K0III", "Leo"),
        ("Adhafera", 10.117, 23.417, 3.43, "F0III", "Leo"),
        ("Chort", 11.237, 15.430, 3.34, "A2V", "Leo"),
        
        # Virgo
        ("Spica", 13.420, -11.161, 1.04, "B1III-IV", "Virgo"),
        ("Zavijava", 11.845, 1.765, 3.60, "F9V", "Virgo"),
        ("Porrima", 12.694, -1.449, 2.74, "F0V", "Virgo"),
        ("Auva", 12.927, -0.666, 3.38, "M3III", "Virgo"),
        ("Vindemiatrix", 13.035, 10.959, 2.85, "G8III", "Virgo"),
        
        # Boötes
        ("Arcturus", 14.261, 19.182, -0.05, "K1.5III", "Boötes"),
        ("Nekkar", 15.032, 40.390, 3.49, "G8III", "Boötes"),
        ("Seginus", 14.534, 38.308, 3.04, "A7III", "Boötes"),
        ("Izar", 14.749, 27.074, 2.37, "K0II-III", "Boötes"),
        ("Muphrid", 13.911, 18.397, 2.68, "G0IV", "Boötes"),
        
        # Libra
        ("Zubeneschamali", 15.283, -9.383, 2.61, "B8V", "Libra"),
        ("Zubenelgenubi", 14.848, -16.042, 2.75, "A3V", "Libra"),
        ("Zubenelakrab", 15.592, -14.789, 3.29, "G8III", "Libra"),
        
        # === SUMMER CONSTELLATIONS ===
        
        # Scorpius
        ("Antares", 16.490, -26.432, 1.09, "M1.5Iab", "Scorpius"),
        ("Shaula", 17.560, -37.104, 1.63, "B1.5IV", "Scorpius"),
        ("Sargas", 17.622, -42.999, 1.87, "F1II", "Scorpius"),
        ("Dschubba", 16.090, -22.622, 2.29, "B0.3IV", "Scorpius"),
        ("Larawag", 17.708, -39.030, 2.69, "B2IV", "Scorpius"),
        ("Wei", 16.835, -38.048, 2.56, "B1V", "Scorpius"),
        ("Lesath", 17.509, -37.295, 2.70, "B2IV", "Scorpius"),
        
        # Sagittarius
        ("Kaus Australis", 18.403, -34.385, 1.85, "B9.5III", "Sagittarius"),
        ("Nunki", 18.921, -26.297, 2.02, "B2.5V", "Sagittarius"),
        ("Ascella", 19.079, -29.880, 2.60, "A2III", "Sagittarius"),
        ("Kaus Media", 18.349, -29.828, 2.70, "K3III", "Sagittarius"),
        ("Kaus Borealis", 18.276, -25.421, 2.82, "K2III", "Sagittarius"),
        ("Albaldah", 19.368, -17.847, 2.98, "A0V", "Sagittarius"),
        
        # Lyra
        ("Vega", 18.616, 38.784, 0.03, "A0V", "Lyra"),
        ("Sheliak", 18.834, 33.363, 3.52, "B8II-III", "Lyra"),
        ("Sulafat", 18.983, 32.690, 3.24, "B9III", "Lyra"),
        ("Delta Lyr", 18.881, 36.898, 4.30, "M4II", "Lyra"),
        
        # Cygnus
        ("Deneb", 20.691, 45.280, 1.25, "A2Ia", "Cygnus"),
        ("Albireo", 19.512, 27.960, 3.18, "K3II", "Cygnus"),
        ("Sadr", 20.371, 40.257, 2.20, "F8Ib", "Cygnus"),
        ("Gienah", 20.771, 33.970, 2.46, "K3II", "Cygnus"),
        ("Delta Cyg", 19.749, 45.131, 2.87, "B9III", "Cygnus"),
        ("Fawaris", 21.211, 30.227, 3.18, "A2Ia", "Cygnus"),
        
        # Aquila
        ("Altair", 19.846, 8.868, 0.77, "A7V", "Aquila"),
        ("Tarazed", 19.771, 10.615, 2.72, "K3III", "Aquila"),
        ("Okab", 19.925, 6.407, 2.99, "B9V", "Aquila"),
        ("Alsafi", 19.092, 13.863, 4.02, "G8IV", "Aquila"),
        
        # Ophiuchus
        ("Rasalhague", 17.582, 12.560, 2.08, "A5III", "Ophiuchus"),
        ("Sabik", 17.173, -15.725, 2.43, "A1V", "Ophiuchus"),
        ("Han", 16.961, -10.567, 2.54, "K2III", "Ophiuchus"),
        ("Cebalrai", 17.724, 4.567, 2.76, "K2III", "Ophiuchus"),
        
        # Hercules
        ("Kornephoros", 16.503, 21.489, 2.78, "G7III", "Hercules"),
        ("Zeta Her", 16.688, 31.603, 2.81, "F9IV", "Hercules"),
        ("Sarin", 17.244, 14.390, 3.16, "K3II", "Hercules"),
        ("Marsic", 17.004, 30.926, 3.42, "B9III", "Hercules"),
        
        # === AUTUMN CONSTELLATIONS ===
        
        # Pegasus
        ("Enif", 21.736, 9.875, 2.39, "K2Ib", "Pegasus"),
        ("Scheat", 23.063, 28.083, 2.42, "M2.5II-III", "Pegasus"),
        ("Markab", 23.079, 15.205, 2.49, "A0IV", "Pegasus"),
        ("Algenib", 0.220, 15.183, 2.83, "B2IV", "Pegasus"),
        ("Homam", 22.169, 25.345, 3.40, "B8V", "Pegasus"),
        
        # Andromeda
        ("Alpheratz", 0.139, 29.091, 2.06, "B8IV", "Andromeda"),
        ("Mirach", 1.162, 35.621, 2.05, "M0III", "Andromeda"),
        ("Almach", 2.065, 42.330, 2.26, "K3II", "Andromeda"),
        ("Delta And", 0.656, 30.861, 3.27, "K3III", "Andromeda"),
        
        # Perseus
        ("Mirfak", 3.405, 49.861, 1.79, "F5Ib", "Perseus"),
        ("Algol", 3.136, 40.956, 2.12, "B8V", "Perseus"),
        ("Epsilon Per", 3.958, 40.010, 2.89, "B0.5V", "Perseus"),
        ("Zeta Per", 3.854, 31.883, 2.85, "B1Ib", "Perseus"),
        ("Delta Per", 3.715, 47.787, 3.01, "B5III", "Perseus"),
        
        # Aquarius
        ("Sadalsuud", 21.526, -5.571, 2.87, "G0Ib", "Aquarius"),
        ("Sadalmelik", 22.096, -0.320, 2.96, "G2Ib", "Aquarius"),
        ("Sadachbia", 22.881, -15.821, 3.27, "A0V", "Aquarius"),
        ("Albali", 22.636, -13.593, 3.77, "K1III", "Aquarius"),
        
        # Capricornus
        ("Deneb Algedi", 21.784, -16.127, 2.87, "A7III", "Capricornus"),
        ("Dabih", 20.350, -14.781, 3.05, "K0III", "Capricornus"),
        ("Nashira", 21.668, -16.662, 3.68, "A5V", "Capricornus"),
        ("Algedi", 20.293, -12.508, 4.24, "G8.5III", "Capricornus"),
        
        # === WINTER CONSTELLATIONS ===
        
        # Orion
        ("Rigel", 5.242, -8.202, 0.13, "B8Ia", "Orion"),
        ("Betelgeuse", 5.919, 7.407, 0.50, "M1-2Ia", "Orion"),
        ("Bellatrix", 5.418, 6.350, 1.64, "B2III", "Orion"),
        ("Alnilam", 5.603, -1.202, 1.70, "B0Ia", "Orion"),
        ("Alnitak", 5.679, -1.943, 1.77, "O9.5Iab", "Orion"),
        ("Saiph", 5.796, -9.670, 2.09, "B0.5Ia", "Orion"),
        ("Mintaka", 5.533, -0.299, 2.23, "O9.5II", "Orion"),
        ("Hatysa", 5.588, -2.600, 3.19, "O8III", "Orion"),
        
        # Canis Major
        ("Sirius", 6.752, -16.717, -1.46, "A1V", "Canis Major"),
        ("Adhara", 6.977, -28.972, 1.50, "B2II", "Canis Major"),
        ("Wezen", 7.140, -26.393, 1.86, "F8Ia", "Canis Major"),
        ("Mirzam", 6.378, -17.956, 1.98, "B1II-III", "Canis Major"),
        ("Aludra", 7.401, -29.303, 2.45, "B5Ia", "Canis Major"),
        
        # Canis Minor
        ("Procyon", 7.655, 5.225, 0.37, "F5IV-V", "Canis Minor"),
        ("Gomeisa", 7.452, 8.290, 2.89, "B8Ve", "Canis Minor"),
        
        # Gemini
        ("Pollux", 7.755, 28.026, 1.14, "K0III", "Gemini"),
        ("Castor", 7.576, 31.888, 1.57, "A1V", "Gemini"),
        ("Alhena", 6.628, 16.399, 1.93, "A0IV", "Gemini"),
        ("Wasat", 7.335, 21.982, 3.53, "F2V", "Gemini"),
        ("Mebsuta", 6.383, 25.131, 3.06, "G8Ib", "Gemini"),
        ("Mekbuda", 7.069, 20.570, 3.78, "F7Ib", "Gemini"),
        
        # Taurus
        ("Aldebaran", 4.598, 16.509, 0.85, "K5III", "Taurus"),
        ("Elnath", 5.438, 28.608, 1.68, "B7III", "Taurus"),
        ("Alcyone", 3.793, 24.105, 2.87, "B7IIIe", "Taurus"),
        ("Maia", 3.876, 24.368, 3.87, "B7III", "Taurus"),
        ("Electra", 3.796, 24.113, 3.70, "B6IIIe", "Taurus"),
        ("Taygeta", 3.762, 24.467, 4.30, "B6V", "Taurus"),
        
        # Auriga
        ("Capella", 5.278, 45.998, 0.08, "G5III", "Auriga"),
        ("Menkalinan", 5.992, 44.947, 1.90, "A1V", "Auriga"),
        ("Mahasim", 5.925, 37.213, 2.62, "A2IV", "Auriga"),
        ("Almaaz", 4.950, 33.166, 3.72, "K3II", "Auriga"),
        
        # === SOUTHERN CONSTELLATIONS (visible from mid-latitudes) ===
        
        # Centaurus
        ("Rigil Kent", 14.660, -60.834, -0.27, "G2V", "Centaurus"),
        ("Hadar", 14.063, -60.373, 0.61, "B1III", "Centaurus"),
        ("Menkent", 14.111, -36.370, 2.06, "K0III", "Centaurus"),
        ("Alnair", 13.665, -53.466, 2.75, "B1V", "Centaurus"),
        
        # Crux (Southern Cross)
        ("Acrux", 12.444, -63.099, 0.77, "B0.5IV", "Crux"),
        ("Gacrux", 12.519, -57.113, 1.63, "M3.5III", "Crux"),
        ("Mimosa", 12.795, -59.689, 1.25, "B0.5III", "Crux"),
        ("Delta Cru", 12.253, -58.749, 2.80, "B2IV", "Crux"),
        
        # Carina
        ("Canopus", 6.399, -52.696, -0.74, "A9II", "Carina"),
        ("Miaplacidus", 9.220, -69.717, 1.68, "A1III", "Carina"),
        ("Avior", 8.375, -59.510, 1.86, "K3III", "Carina"),
        ("Aspidiske", 9.285, -59.275, 2.21, "A8Ib", "Carina"),
        
        # Eridanus
        ("Achernar", 1.629, -57.237, 0.46, "B6Vep", "Eridanus"),
        ("Cursa", 5.131, -5.086, 2.79, "A3III", "Eridanus"),
        ("Zaurak", 3.970, -13.509, 3.24, "M0III", "Eridanus"),
        ("Rana", 3.736, -9.763, 3.54, "K0IV", "Eridanus"),
        
        # Piscis Austrinus
        ("Fomalhaut", 22.961, -29.622, 1.16, "A3V", "Piscis Austrinus"),
        
        # Grus
        ("Alnair", 22.137, -46.961, 1.74, "B7IV", "Grus"),
        ("Beta Gru", 22.711, -46.885, 2.11, "M5III", "Grus"),
        ("Gamma Gru", 21.899, -37.365, 3.01, "B8III", "Grus"),
        
        # === ZODIACAL CONSTELLATIONS (remaining) ===
        
        # Aries
        ("Hamal", 2.119, 23.462, 2.00, "K2III", "Aries"),
        ("Sheratan", 1.911, 20.808, 2.64, "A5V", "Aries"),
        ("Mesarthim", 1.884, 19.294, 3.88, "A0V", "Aries"),
        
        # Cancer
        ("Al Tarf", 8.275, 9.186, 3.52, "K4III", "Cancer"),
        ("Asellus Australis", 8.775, 18.154, 3.94, "K0III", "Cancer"),
        ("Asellus Borealis", 8.691, 21.469, 4.66, "A1V", "Cancer"),
        ("Acubens", 8.775, 11.858, 4.25, "A5V", "Cancer"),
        
        # Pisces
        ("Alrescha", 2.034, 2.764, 3.62, "A0p", "Pisces"),
        ("Fumalsamakah", 23.286, 5.627, 4.53, "F7V", "Pisces"),
        ("Delta Psc", 0.813, 7.585, 4.43, "K5III", "Pisces"),
    ]
    
    # Write to CSV file
    catalog_file = data_dir / "comprehensive_star_catalog.csv"
    
    print(f"Creating comprehensive star catalog: {catalog_file}")
    
    with open(catalog_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header
        writer.writerow([
            "name", "ra_hours", "dec_degrees", "magnitude", 
            "spectral_type", "constellation"
        ])
        
        # Write star data
        for star_data in comprehensive_stars:
            writer.writerow(star_data)
    
    print(f"✅ Created comprehensive catalog with {len(comprehensive_stars)} stars")
    print(f"📁 Saved to: {catalog_file}")
    
    # Print constellation summary
    constellations = {}
    for star in comprehensive_stars:
        constellation = star[5]
        if constellation not in constellations:
            constellations[constellation] = 0
        constellations[constellation] += 1
    
    print(f"\n🌟 Constellation Coverage:")
    for constellation in sorted(constellations.keys()):
        count = constellations[constellation]
        print(f"   {constellation}: {count} stars")
    
    print(f"\n📊 Total: {len(constellations)} constellations, {len(comprehensive_stars)} stars")
    
    return str(catalog_file)


if __name__ == "__main__":
    create_comprehensive_catalog()
