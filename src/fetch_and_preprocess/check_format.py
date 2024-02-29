import json
from datetime import datetime
from typing import Any
import requests
from requests import Response
from src.common.config import WARSAW_LAT_MIN, WARSAW_LAT_MAX, WARSAW_LON_MIN, WARSAW_LON_MAX

__all__ = [
    'check_format_basic',
    'check_format_buses_coordinates',
    'check_format_buses_at_stop',
    'check_format_timetables_at_stop',
    'check_format_buses_location',
    'check_coordinates',
    'check_time',
    'check_time_in_range'
]

def check_format_basic(response: Response) -> bool:
    """
    Checks if the API response adheres to the expected format according to the documentation.
    According to the API documentation, every successful response should contain a 'result' key
    with a non-empty list of data, represented as {'result': [DATA]}.
    An empty response ({'result': []}) is considered unsuccessful.

    Args:
        response (Response): The response object received from the API request.

    Returns:
        bool: True if the response is correct according to the documentation, False otherwise.
    """
    if not response:
        return False

    try:
        response.raise_for_status()

        data = response.json()

        if isinstance(data, dict) and 'result' in data and isinstance(data['result'], list) and data['result']:
            return True
        else:
            print("Invalid API response: missing data or incorrect format." + response.text)
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except json.JSONDecodeError as json_err:
        print(f"JSON decoding error occurred: {json_err}")
    return False

def check_format_buses_coordinates(result: Any) -> bool:
    """
    Checks if the format of result data is as expected for bus coordinates.

    Args:
        result (dict): The result data. Provided in JSON format

    Returns:
        bool: True if the format is correct, False otherwise.
    """
    required_keys = {'zespol', 'slupek', 'nazwa_zespolu', 'id_ulicy', 'szer_geo', 'dlug_geo', 'kierunek',
                     'obowiazuje_od'}

    # Check if 'result' is a dictionary
    if not isinstance(result, dict):
        return False

    # Check if 'result' contains the key 'result'
    if 'result' not in result or not isinstance(result['result'], list):
        return False

    # Check if each item in the list has the key 'values' and if it's a list
    for item in result['result']:
        if not isinstance(item, dict) or 'values' not in item or not isinstance(item['values'], list):
            return False

        # Check if first item in the 'values' list is a dictionary with keys 'value' and 'key'
        for value_item in item['values']:
            if not isinstance(value_item, dict) or 'key' not in value_item or 'value' not in value_item:
                return False

            # Check if each dictionary item in 'values' has correct key 'key'
            if value_item['key'] not in required_keys:
                return False

    return True


def check_format_buses_at_stop(result: Any) -> bool:
    """
    Checks if the format of result data is as expected for bus buses at stop.

    Args:
        result (dict): The result data. Provided in JSON format

    Returns:
        bool: True if the format is correct, False otherwise.
    """
    if not isinstance(result, dict):
        return False

    if "result" not in result or not isinstance(result["result"], list):
        return False

    for item in result["result"]:
        if not isinstance(item, dict) or "values" not in item or not isinstance(item["values"], list):
            return False

        for value_item in item["values"]:
            if not isinstance(value_item, dict) or "value" not in value_item or "key" not in value_item:
                return False

    return True


def check_format_timetables_at_stop(result: Any) -> bool:
    """
    Checks if the format of result data is as expected for timetables of a bus at a stop.

    Args:
        result (dict): The result data. Provided in JSON format

    Returns:
        bool: True if the format is correct, False otherwise.
    """
    required_keys = {"czas", "trasa", "kierunek", "brygada", "symbol_1", "symbol_2"}
    if "result" not in result:
        return False

    if not isinstance(result["result"], list):
        return False

    for item in result["result"]:
        if not isinstance(item, dict) and "values" not in item:
            return False

        if not isinstance(item["values"], list):
            return False

        for value_item in item["values"]:
            if "value" not in value_item or "key" not in value_item:
                return False

            if value_item["key"] not in required_keys:
                return False

    return True


def check_format_buses_location(result: Any) -> bool:
    required_keys = ["Lines", "Lon", "VehicleNumber", "Time", "Lat", "Brigade"]
    if "result" not in result:
        return False

    if not isinstance(result["result"], list):
        return False

    for item in result["result"]:
        if not all(key in item for key in required_keys):
            return False

    return True

def check_coordinates(lat: float, lon: float) -> bool:
    """
    Checks if the given coordinates are within the geographical boundaries of Warsaw.

    Args:
        lat (float): The latitude coordinate.
        lon (float): The longitude coordinate.

    Returns:
        bool: True if the coordinates are within Poland, False otherwise.
    """
    if not isinstance(lat, (int, float)) or not isinstance(lon, (int, float)):
        return False

    return WARSAW_LAT_MIN <= lat <= WARSAW_LAT_MAX and WARSAW_LON_MIN <= lon <= WARSAW_LON_MAX

def check_time(time_str: str, time_format: str) -> bool:
    try:
        datetime.strptime(time_str, time_format)
        return True
    except ValueError:
        return False

def check_time_in_range(time_str: str, h1: int, h2: int, time_format: str) -> bool:
    """
    Checks if the time specified in the given time format falls within the specified range of hours.
    The data of bus location was fetched within the specified range of hours, so we have to filter the hours
    that will be useless when it comes to analyzing bus locations.

    Parameters:
    time_str (str): A string representing time.
    h1 (int): Lower bound of the range of hours.
    h2 (int): Upper bound of the range of hours.
    format (str): The format string used to parse the time.

    Returns:
    bool: True if the time falls within the specified range; otherwise, False.
    """
    try:
        hour = datetime.strptime(time_str, time_format).hour
        if (h1 <= hour < h1 + 1) or (h2 <= hour < h2 + 1):
            return True
    except ValueError:
        return False

