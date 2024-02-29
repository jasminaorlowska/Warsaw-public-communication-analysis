import unittest
from ..check_format import *

invalid_data = {
    "result": [
        {
            "invalid data"
        }
    ]
}

bus_stops_coordinates_expected_format = {
    "result": [
        {
            "values": [
                {
                    "value": "1001",
                    "key": "zespol"
                },
                {
                    "value": "01",
                    "key": "slupek"
                },
                {
                    "value": "Kijowska",
                    "key": "nazwa_zespolu"
                },
                {
                    "value": "2201",
                    "key": "id_ulicy"
                },
                {
                    "value": "52.248455",
                    "key": "szer_geo"
                },
                {
                    "value": "21.044827",
                    "key": "dlug_geo"
                },
                {
                    "value": "al.Zieleniecka",
                    "key": "kierunek"
                },
                {
                    "value": "2023-10-21 00:00:00.0",
                    "key": "obowiazuje_od"
                }
            ]
        }
    ]
}
buses_at_bus_stop_expected_format = {
    "result": [
        {
            "values": [
                {
                    "value": "138",
                    "key": "linia"
                }
            ]
        },
        {
            "values": [
                {
                    "value": "411",
                    "key": "linia"
                }
            ]
        },
        {
            "values": [
                {
                    "value": "502",
                    "key": "linia"
                }
            ]
        }
    ]
}
timetables_at_bus_stop_expected_format = {
    "result":	[
        {
            "values":	[
                {
                    "value":	"05:04:00",
                    "key":	"czas"
                },
                {
                    "value":	"TO-OLS",
                    "key":	"trasa"
                },
                {
                    "value":	"PKP	Olszynka	Grochowska",
                    "key":	"kierunek"
                },
                {
                    "value":	"1",
                    "key":	"brygada"
                },
                {
                    "value":	"null",
                    "key":	"symbol_1"
                },
                {
                    "value":	"null",
                    "key":	"symbol_2"
                }
            ]
        }
    ]
}
buses_locations_expected_format = {
    "result": [
        {
            "Lines": "213",
            "Lon": 21.102785,
            "VehicleNumber": "1000",
            "Time": "2024-02-26 07:59:19",
            "Lat": 52.222749,
            "Brigade": "3"
        },
        {
            "Lines": "213",
            "Lon": 21.1420323,
            "VehicleNumber": "1001",
            "Time": "2024-02-26 07:59:33",
            "Lat": 52.2141913,
            "Brigade": "4"
        }
    ]
}

class TestResultFormat(unittest.TestCase):

    def test_valid_format_bus_stops_coordinates(self):
        self.assertTrue(check_format_buses_coordinates(bus_stops_coordinates_expected_format))

    def test_invalid_format_bus_stops_coordinates(self):
        self.assertFalse(check_format_buses_coordinates(invalid_data))

    def test_valid_format_buses_at_bus_stop(self):
        self.assertTrue(check_format_buses_at_stop(buses_at_bus_stop_expected_format))

    def test_invalid_format_buses_at_bus_stop(self):
        self.assertFalse(check_format_buses_at_stop(invalid_data))

    def test_valid_format_timetables_at_bus_stop(self):
        self.assertTrue(check_format_timetables_at_stop(timetables_at_bus_stop_expected_format))

    def test_invalid_format_timetables_at_bus_stop(self):
        self.assertFalse(check_format_timetables_at_stop(invalid_data))

    def test_valid_format_buses_location(self):
        self.assertTrue(check_format_buses_location(buses_locations_expected_format))

if __name__ == '__main__':
    unittest.main()
