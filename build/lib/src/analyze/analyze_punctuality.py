from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import numpy as np
from geopy.distance import geodesic

def analyze_punctuality_thread_executor(row, timetables, lat, lon):
    with ThreadPoolExecutor() as executor:
        result = executor.submit(analyze_punctuality_for_a_bus_stop, df_locations, row, timetables, lat, lon)
        return result.result()


def analyze_punctuality_for_a_bus_stop(df_locations, row, timetables, lat, lon):
    arrivals_number = 0
    delay_sum = 0
    timetables = row[timetables]
    lat = row[lat]
    lon = row[lon]
    now = datetime.now().date()

    for line in timetables:
        timetable_for_line = timetables[line]
        # if line[0].isdigit():
        line = np.int64(line)

        for expected_arrival_for_a_line in timetable_for_line:
            best_delay_in_minutes = -1
            expected_arrival_time = datetime.strptime(expected_arrival_for_a_line['czas'], "%H:%M:%S").time()
            expected_arrival_brigade = np.int64(expected_arrival_for_a_line['brygada'])

            # Find right row
            bus_locations = df_locations.loc[
                (df_locations['Lines'] == line) & (df_locations['Brigade'] == expected_arrival_brigade)]
            if not bus_locations.empty:
                # bus_locations['Data']) its a list of lists of dicts with keys:  Lat Lon Time
                locations_of_expected_bus = list(bus_locations['Data'])[0]
                for element in locations_of_expected_bus:
                    if geodesic((lat, lon), (element['Lat'], element['Lon'])).meters < 100:
                        arrival_time = datetime.strptime(element['Time'], "%Y-%m-%d %H:%M:%S").time()
                        diff = datetime.combine(now, expected_arrival_time) - datetime.combine(now, arrival_time)
                        diff = diff.total_seconds() / 60
                        # We don't count Delays > 3h and < 0h (wrong data)
                        if diff > 180 or diff < 0:
                            continue
                        # Update best delay - we probably found correct bus.
                        # The nearest one at that time with the same line and brigade.
                        if best_delay_in_minutes == -1 or best_delay_in_minutes > diff:
                            best_delay_in_minutes = diff
                            if best_delay_in_minutes < 5:
                                break
            # If we have result - update it.
            if best_delay_in_minutes != -1:
                arrivals_number = arrivals_number + 1
                delay_sum += best_delay_in_minutes

    if arrivals_number != 0:
        return delay_sum / arrivals_number
    else:
        return -1