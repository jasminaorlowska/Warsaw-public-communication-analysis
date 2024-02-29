"""
This module constructs API request data for Warsaw public transport services,
covering dictionaries, bus stop coordinates, schedules, and live bus locations.
Functions return dictionaries for API requests, specifying URLs, necessary API keys, and query parameters.
API documentation can be found here: https://api.um.warszawa.pl/#
"""


def get_request_data_bus_stops_coordinates(apikey):
    return {
        'url': 'https://api.um.warszawa.pl/api/action/dbstore_get',
        'params': {
            'id': '1c08a38c-ae09-46d2-8926-4f9d25cb0630',
            'apikey': apikey
        },
        'headers': {}
    }


def get_request_data_buses_at_stop(bus_stop_id, bus_stop_nr, apikey):
    return {
        'url': "https://api.um.warszawa.pl/api/action/dbtimetable_get",
        'params': {
            'id': '88cd555f-6f31-43ca-9de4-66c479ad5942',
            'busstopId': bus_stop_id,
            'busstopNr': bus_stop_nr,
            'apikey': apikey
        },
        'headers': {}
    }


def get_request_data_timetable_at_stop_for_line(line, bus_stop_id, bus_stop_nr, apikey):
    return {
        'url': "https://api.um.warszawa.pl/api/action/dbtimetable_get",
        'params': {
            'id': 'e923fa0e-d96c-43f9-ae6e-60518c9f3238',
            'line': line,
            'busstopId': bus_stop_id,
            'busstopNr': bus_stop_nr,
            'apikey': apikey
        },
        'headers': {}
    }


def get_request_data_buses_location(apikey):
    return {
        'url': "https://api.um.warszawa.pl/api/action/busestrams_get/",
        'params': {
            "resource_id": "f2e5503e927d-4ad3-9500-4ab9e55deb59",
            "type": "1",
            "apikey": apikey
        },
        'headers': {"Cache-Control": "no-cache"}
    }
