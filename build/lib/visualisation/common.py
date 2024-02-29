import os
from src.common.config import *

buses_locations_at_8 = os.path.join("..", "..", DATA_FOLDER, PROCESSED, BUSES_LIVE_LOCATIONS, "2024-02-26 08")
buses_locations_at_12 = os.path.join("..", "..", DATA_FOLDER, PROCESSED, BUSES_LIVE_LOCATIONS, "2024-02-26 12")

bus_stops_coordinates = os.path.join("..", "..", DATA_FOLDER, PROCESSED,  "bus_stops_coordinates.json")
timetables = os.path.join("..", "..", DATA_FOLDER, PROCESSED,  "timetables.json")

results_from_8AM = "results_from_8AM.json"
results_from_12AM = "results_from_12AM.json"
