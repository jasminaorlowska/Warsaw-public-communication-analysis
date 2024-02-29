"""
Defines constants for file names, directory paths, and configuration settings,
facilitating path management, data processing parameters, and date formatting across the project
to ensure consistent data handling and integrity.
"""

from typing import Final

# ----------Filenames-------------
BUS_STOPS_COORDINATES_FILE: Final = 'bus_stops_coordinates.json'
BUSES_AT_STOPS_FILE: Final = 'buses_at_stops.json'
TIMETABLES: Final = 'timetables.json'

# ----------Directory names-------------
PROCESSED: Final = "processed"
RAW: Final = "raw"
DATA_FOLDER = "data"
SRC_FOLDER = "src"
BUSES_LIVE_LOCATIONS: Final = 'buses_live_locations'

# -------Warsaw geographic boundaries--------
WARSAW_LAT_MIN, WARSAW_LAT_MAX = 52.1, 52.3
WARSAW_LON_MIN, WARSAW_LON_MAX = 20.8, 21.3

# ----------Other-------------
DATE_FORMAT: Final = "%Y-%m-%d %H:%M:%S"
TIME_FORMAT: Final = "%H:%M:%S"

