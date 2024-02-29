import os
from typing import List
import pandas as pd
from geopy.distance import geodesic as GD
from pandas import DataFrame
from src.analyze.dictionary_data import *

def combine_bus_locations_within_hour(folder: str) -> DataFrame:
    """
    Combine bus locations within an hour from JSON files in the given folder.

    Args:
    - folder (str): The path to the folder containing JSON files.

    Returns:
    DataFrame: A DataFrame containing combined bus location data.
    """
    combined_data = []

    try:
        for filename in os.listdir(folder):
            if filename.endswith('.json'):
                file_path = os.path.join(folder, filename)
                df = pd.read_json(file_path)
                combined_data.append(df)

        result = pd.concat(combined_data, ignore_index=True)
        return result
    except Exception as e:
        print(f"Error occurred while combining bus locations files: {e}")


def group_by_bus(df: DataFrame) -> DataFrame:
    """
    Group bus location DataFrame by lines and brigade.

    Args:
    - df (DataFrame): DataFrame containing bus location data.

    Returns:
    DataFrame: Grouped DataFrame with a new column "Data" containing grouped records.
    """
    try:
        return df.groupby([lines, brigade]).apply(
            lambda x: x[[time, lon, lat]].sort_values(by=time).to_dict("records"),
            include_groups=False).reset_index(name=data)
    except Exception as e:
        print(f"Error occurred while grouping by bus: {e}")


def count_trip_duration(items: List):
    """
    Count trip duration for a group of bus locations.

    Args:
    - items: A list of dictionaries containing bus location data.

    Returns:
    float: Trip duration in hours.
    """
    try:
        min_time = max_time = items[0][time]
        for item in items[1:]:
            if item[time] < min_time:
                min_time = item[time]
            if item[time] > max_time:
                max_time = item[time]
        trip_dur = pd.to_datetime(max_time) - pd.to_datetime(min_time)
        return trip_dur.total_seconds() / 3600
    except Exception as e:
        print(f"Error occurred while counting trip duration: {e}")


def count_durations(df: DataFrame) -> DataFrame:
    """
    Count trip durations for each group in DataFrame.

    Args:
    - df (DataFrame): DataFrame containing bus location data.

    Returns:
    DataFrame: DataFrame with added "Trip_Dur" column.
    """
    try:
        df[trip_duration] = df[data].apply(count_trip_duration)
        return df
    except Exception as e:
        print(f"Error occurred while counting durations: {e}")


def count_distance(items):
    """
    Count total distance covered by the bus.

    Args:
    - items: A list of dictionaries containing bus location data.

    Returns:
    float: Total distance covered in kilometers.
    """
    if len(items) < 2:
        return 0
    try:
        bus_total_distance = 0
        prev_loc = (items[0][lat], items[0][lon])
        for item in items[1:]:
            curr_loc = (item[lat], item[lon])
            bus_total_distance += GD(prev_loc, curr_loc).km
            prev_loc = curr_loc
        return bus_total_distance
    except Exception as e:
        print(f"Error occurred while counting distance: {e}")


def count_avg_speed(df: DataFrame) -> DataFrame:
    """
    Count average speed for each group in DataFrame.

    Args:
    - df (DataFrame): DataFrame containing bus location data.

    Returns:
    DataFrame: DataFrame with added total_distance and avg_speed columns.
    """
    try:
        df[total_distance] = df[data].apply(count_distance)
        df[avg_speed] = df[total_distance] / df[trip_duration]
        df.dropna(inplace=True)
        return df
    except Exception as e:
        print(f"Error occurred while counting average speed: {e}")

def clean_df(df: DataFrame) -> DataFrame:
    rows_to_remove = df.loc[(df[avg_speed] < 30) | (df[avg_speed] > 80)]
    df.drop(rows_to_remove.index, inplace=True)
    df.dropna(inplace=True)
    return df
