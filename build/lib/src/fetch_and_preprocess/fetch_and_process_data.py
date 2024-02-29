import argparse
from fetch_data import *
from process_data import *
from scheduled_function_runner import start

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Program description")
    parser.add_argument("API KEY", type=str, help="Description of argument 1")
    parser.add_argument("first_hour", type=int, help="When fetching data from api")
    parser.add_argument("second_hour", type=int, help="When fetching data from api")
    args = parser.parse_args()

    API_KEY = args.API_KEY
    first_hour, second_hour = args.first_hour, args.second_hour
    assert (0 <= first_hour <= 23 and 0 <= second_hour <= 23 and first_hour < second_hour)

    fetch_and_save_bus_stops_coordinates(API_KEY)
    process_bus_stops_coordinates()

    fetch_and_save_buses_at_stops(API_KEY)
    process_buses_at_stops()

    start(first_hour, fetch_and_save_bus_locations, API_KEY)
    start(second_hour, fetch_and_save_bus_locations, API_KEY)
    process_bus_location_files()

    fetch_and_save_timetables(API_KEY)
    process_timetables(first_hour, second_hour)
