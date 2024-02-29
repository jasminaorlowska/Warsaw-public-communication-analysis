from typing import Dict, Optional, Callable, List, Any
import requests
from requests import Response
import json
from src.common.config import *
from api_data import *
from file_utils import save_file_to_data_folder, get_filepath
from check_format import *
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
from datetime import datetime

MAX_WORKERS = 40

__all__ = ["fetch_and_save_bus_stops_coordinates",
           "fetch_and_save_buses_at_stops",
           "fetch_and_save_timetables",
           "fetch_and_save_bus_locations"]


def fetch_data(request_data: Dict) -> Optional[Response]:
    """
    Fetches data based on the provided API data.

    Args:
        request_data (Dict): Dictionary containing the API request details with keys: 'url', 'params', and 'headers'.

    Returns:
        Optional[Response]: The response object from the API request if the fetch is successful, None otherwise.
    """

    try:
        url, params, headers = request_data.get('url'), request_data.get('params'), request_data.get('headers')

        response = requests.get(url, params=params, headers=headers)

        if check_format_basic(response):
            return response
        else:
            print(f"Failed to fetch data from {url}. Response: {response.text}")
            return None

    except requests.RequestException as e:
        print(f"Request Exception occurred: {e}")
        return None


def fetch_and_save_bus_stops_coordinates(api_key: str) -> None:
    """
    Fetches bus stops coordinates data from an API using the provided API key,
    checks its format, and saves it to a file in the RAW folder.

    Args:
        api_key (str): The API key required to access the bus stops coordinates data.
    """
    response = fetch_data(get_request_data_bus_stops_coordinates(api_key))
    if check_format_basic(response) and check_format_buses_coordinates(response.json()):
        save_file_to_data_folder(response.json(), BUS_STOPS_COORDINATES_FILE, True)
    else:
        print(f"An error occurred while fetching and saving data: bus_stops_coordinates.")


def fetch_and_save_multiple(input_file: str, output_file: str, helper_function: Callable, api_key: str) -> None:
    """
    Reads data from a JSON file, invokes a data-fetching function for each object in the file,
    and saves the results to an output file. Function is multithreading, allowing for faster data retrieval.

    Args:
        input_file (str): The path to the input JSON file.
        output_file (str): The path to the output file where the results will be saved.
        helper_function (Callable): A function responsible for fetching data for each object in the input file.
        api_key (str): The API key required to access the data.
    """
    with open(get_filepath(input_file, False), 'r', encoding='utf-8') as file:
        loaded_data = json.load(file)

    result_data = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_item = {executor.submit(helper_function, item, api_key): item for item in loaded_data}
        for future in as_completed(future_to_item):
            result = future.result()
            if result:
                result_data.append(result)

    save_file_to_data_folder(result_data, output_file, True)


def fetch_buses_at_stop(stop: Any, api_key: str) -> Optional[Dict[str, Any]]:
    """
    Fetches the list of buses available at a given bus stop.

    Args:
        stop (Dict): A dictionary containing the bus stop information including 'zespol' (busstopId)
        and 'slupek (busstopNr).
        api_key (str): The user's API key.

    Returns:
        Optional[Dict]: A dictionary containing bus stop ID, number, and a list of buses if successful,
        otherwise None.
    """
    api_data = get_request_data_buses_at_stop(stop['zespol'], stop['slupek'], api_key)

    response = fetch_data(api_data)
    if check_format_basic(response):
        result = response.json()
        if check_format_buses_at_stop(result):
            buses = []
            values = result.get("result", [])
            for value in values:
                for bus_line in value.get("values", []):
                    buses.append(bus_line.get("value"))
            return {
                'busstopId': stop['zespol'],
                'busstopNr': stop['slupek'],
                'autobusy': buses
            }
    return None


def fetch_timetable_at_stop(stop: Dict[str, Any], api_key: str) -> List[Dict[str, Any]]:
    """Fetches the timetable at a given bus stop.

    Args:
        stop (Dict): A dictionary containing the bus stop information including 'busstopId', 'busstopNr', and
        list of buses at this bus stop.
        api_key (str): The API key required to access the data.

    Returns:
        List[Dict]: A list of dictionaries containing bus stop ID, number, bus line, and timetable data for this line.
    """
    bus_stop_id, bus_stop_nr, buses = stop['busstopId'], stop['busstopNr'], stop['autobusy']
    session = requests.Session()
    all_timetables = []

    def fetch_timetable_at_stop_for_a_line(bus_line):
        api_data = get_request_data_timetable_at_stop_for_line(bus_line, bus_stop_id, bus_stop_nr, api_key)
        response = session.get(api_data['url'], params=api_data['params'])
        if check_format_basic(response):
            result = response.json()
            if check_format_timetables_at_stop(result):
                timetable_data = result.get('result', [])
                timetable_data = [{
                    value["key"]: value["value"]
                    for value in item["values"]
                } for item in timetable_data]
                return {
                    'busstopId': bus_stop_id,
                    'busstopNr': bus_stop_nr,
                    'linia': bus_line,
                    'rozklad': timetable_data
                }
        return None

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(fetch_timetable_at_stop_for_a_line, bus_line) for bus_line in buses]
        for future in futures:
            future_result = future.result()
            if future_result:
                all_timetables.append(future_result)
    session.close()
    return all_timetables


def fetch_and_save_buses_at_stops(api_key: str) -> None:
    """
    Fetches and saves the list of buses at stops using the provided API key.

    Args:
        api_key (str): The API key required to access the data.
    """
    fetch_and_save_multiple(BUS_STOPS_COORDINATES_FILE, BUSES_AT_STOPS_FILE, fetch_buses_at_stop, api_key)


def fetch_and_save_timetables(api_key: str) -> None:
    """
    Fetches and saves the timetables at stops using the provided API key.

    Args:
        api_key (str): The API key required to access the data.
    """
    fetch_and_save_multiple(BUSES_AT_STOPS_FILE, TIMETABLES, fetch_timetable_at_stop, api_key)


def fetch_and_save_bus_locations(api_key: str) -> None:
    """
    Fetches and saves the live locations of buses using the provided API key.

    Args:
        api_key (str): The API key required to access the data.
    """
    curr_time = datetime.now().strftime(DATE_FORMAT)

    filename = str(curr_time) + '.json'
    filepath = os.path.join(BUSES_LIVE_LOCATIONS, filename)
    response = fetch_data(get_request_data_buses_location(api_key))
    if check_format_basic(response):
        result = response.json()
        if check_format_buses_location(result):
            save_file_to_data_folder(result, filepath, True)
            return
