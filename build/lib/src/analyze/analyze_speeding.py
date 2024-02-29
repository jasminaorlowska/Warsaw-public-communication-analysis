from datetime import datetime
from src.analyze.analyze_avg_speed import *
from src.common.config import *

def analyze_speeding_points_single(items: List):
    coordinates = []
    if len(items) < 2:
        return []
    try:
        prev_loc = (items[0][lat], items[0][lon])
        prev_time = datetime.strptime(items[0][time], DATE_FORMAT)

        for item in items[1:]:
            curr_loc = (item[lat], item[lon])
            curr_time = datetime.strptime(item[time], DATE_FORMAT)
            dist = GD(prev_loc, curr_loc).km
            time_delta = (curr_time - prev_time).total_seconds() / 3600
            speed = dist/time_delta if time_delta > 0 else 0
            if 50 < speed < 85:
                coordinates.append(((curr_loc[0] + prev_loc[0])/2, (curr_loc[1] + prev_loc[1])/2))
            prev_loc = curr_loc
            prev_time = curr_time
        return coordinates
    except Exception as e:
        print(f"Error occurred while counting speeding points single: {e}")
        return coordinates

def analyze_speeding_points(df: DataFrame) -> DataFrame:
    try:
        df[speeding_points] = df[data].apply(analyze_speeding_points_single)
    except Exception as e:
        print(f"Error occurred while counting  speeding points: {e}")
    return df

def collect_speeding_points(df: DataFrame) -> List:
    all_speeding_points = []
    for values_list in df[speeding_points]:
        all_speeding_points.extend(values_list)
    return all_speeding_points
