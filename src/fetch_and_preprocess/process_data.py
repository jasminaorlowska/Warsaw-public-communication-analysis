from datetime import datetime, timedelta
from src.common.config import *
from file_utils import *
import pandas as pd
import os
import json
from check_format import *

__all__ = [
    "process_bus_stops_coordinates",
    "process_buses_at_stops",
    "process_timetables",
    "process_bus_location_files"
]


def process_bus_stops_coordinates():
    """
   Processes the coordinates of bus stops.
   Reads the raw coordinates data from the specified file, cleans it, and saves the processed data to a new file
   BUS_STOPS_COORDINATES_FILE in data/processed folder.
   """
    data = read_file_from_data_folder(BUS_STOPS_COORDINATES_FILE, True)

    df = pd.DataFrame([{item['key']: item['value'] for item in record['values']} for record in data['result']])

    selected_columns = ['zespol', 'slupek', 'nazwa_zespolu', 'id_ulicy', 'szer_geo', 'dlug_geo']
    df = df[selected_columns]

    dest_path = get_filepath(BUS_STOPS_COORDINATES_FILE, False)
    df.to_json(dest_path, orient='records', indent=4, force_ascii=False)
    print(f"Data saved to {dest_path}")


def process_buses_at_stops():
    """
    Processes the list of buses available at stops.
    Reads the raw buses data from the specified file, filters it, and saves the processed data to a new file
    BUSES_AT_STOPS_FILE in data/processed folder.
    """
    df = pd.read_json(get_filepath(BUSES_AT_STOPS_FILE, RAW))

    # Filter vehicles - remove all trams and all buses starting with a letter.
    def filter_buses(bus_list):
        return [bus for bus in bus_list if not bus[0].isalpha() and len(bus) > 2]

    df['autobusy'] = df['autobusy'].apply(filter_buses)
    df = df[df['autobusy'].apply(bool)]

    dest_path = get_filepath(BUSES_AT_STOPS_FILE, False)
    df.to_json(dest_path, orient='records', indent=4, force_ascii=False)
    print(f"Data saved to {dest_path}")


def process_timetables(first_hour, second_hour):
    """
    Processes the timetables at stops.
    Reads the raw timetable data from the specified file, cleans it, and saves the processed data to a new file
    TIMETABLES in data/processed folder.

    Args:
        first_hour(int): hour of first bus locations fetching
        second_hour(int) hours of second bus locations fetching
    """

    buss_top_id, bus_stop_nr, timetables, bus_line = "busstopId", "busstopNr", "rozklad", "linia"
    with open(get_filepath(TIMETABLES, True), 'r', encoding='utf-8') as file:
        data = json.load(file)

    def check_condition(departure, first_hour, second_hour):
        time_ok = check_time_in_range(departure["czas"], first_hour, second_hour, TIME_FORMAT)
        brigade_ok = departure["brygada"].isdigit()

        return time_ok and brigade_ok

    cleaned_data = []
    for bus_stop_timetables in data:
        if bus_stop_timetables:
            first_bus_stop = bus_stop_timetables[0]
            bus_stop_data = {
                buss_top_id: first_bus_stop[buss_top_id],
                bus_stop_nr: first_bus_stop[bus_stop_nr],
                timetables: {}
            }

            for bus_line_timetable in bus_stop_timetables:
                bus_line_number = bus_line_timetable[bus_line]
                departures = []

                for departure in bus_line_timetable[timetables]:
                    if check_condition(departure, first_hour, second_hour):
                        departure_data = {"czas": departure["czas"], "brygada": departure["brygada"]}
                        departures.append(departure_data)
                if departures:
                    bus_stop_data[timetables][bus_line_number] = departures

        if bus_stop_data[timetables]:
            cleaned_data.append(bus_stop_data)

    save_file_to_data_folder(cleaned_data, TIMETABLES, False)


def process_bus_location_file(filename: str) -> None:
    """
    Processes bus location data from a single file.
    Reads the raw bus location data from the specified file, filters it based on a time window,
    and saves the processed data to a new file in data/processed/buses_live_locations folder.

    Parameters:
        filename (str): The name of the file containing bus location data.
    """

    base_name = filename.rsplit('.', 1)[0]
    file_datetime = datetime.strptime(base_name, DATE_FORMAT)
    filepath = os.path.join(BUSES_LIVE_LOCATIONS, filename)

    with open(get_filepath(filepath, True), 'r', encoding='utf-8') as file:
        data = json.load(file)

    def check_condition(bus_location, file_datetime) -> bool:
        try:
            coordinates_ok = check_coordinates(bus_location['Lat'], bus_location['Lon'])
            line_number_ok = bus_location['Lines'][0].isdigit()
            brigade_ok = bus_location['Brigade'].isdigit()
            time_ok = check_time(bus_location['Time'], DATE_FORMAT) and (abs(
                datetime.strptime(bus_location["Time"], DATE_FORMAT) - file_datetime) <= timedelta(minutes=1))
            return brigade_ok and coordinates_ok and line_number_ok and time_ok
        except (KeyError, IndexError, ValueError):
            return False

    filtered_bus_locations = [
        {
            'Lines': bus_location['Lines'],
            'Lon': bus_location['Lon'],
            'Lat': bus_location['Lat'],
            'Brigade': bus_location['Brigade'],
            'Time': bus_location['Time']
        }
        for bus_location in data.get("result", [])
        if check_condition(bus_location, file_datetime)
    ]
    length = len("YYYY-MM-DD HH")
    path = os.path.join(BUSES_LIVE_LOCATIONS, filename[:length])
    live_buses_location_hour_directory = get_filepath(path, False)
    try:
        os.makedirs(get_filepath(live_buses_location_hour_directory, False), exist_ok=True)
        print(f"Directory '{get_filepath(live_buses_location_hour_directory, False)}' created successfully.")
        new_file_path = os.path.join(live_buses_location_hour_directory, filename)
        save_file_to_data_folder(filtered_bus_locations, new_file_path, False)
    except Exception as e:
        print(f"Error occurred while creating directory "
              f"'{get_filepath(live_buses_location_hour_directory, False)}': {e}")


def process_bus_location_files() -> None:
    """
    Processes bus location data from multiple files.
    For each bus-location file reads raw bus location data, processes it, and saves the processed data to a new file
    in  data/processed/buses_live_locations folder.
    """

    filepath = get_filepath(BUSES_LIVE_LOCATIONS, True)
    for filename in os.listdir(filepath):
        if filename.endswith(".json"):
            process_bus_location_file(filename)
