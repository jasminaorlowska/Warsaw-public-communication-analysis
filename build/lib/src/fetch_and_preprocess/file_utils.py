import os

from src.common.config import *
from typing import Any
import json

__all__ = [
    "get_filepath",
    "save_file_to_data_folder",
    "read_file_from_data_folder"
]


def get_filepath(filename: str, data_is_raw: bool) -> str:
    """
    Returns the full file path based on the file name and whether the data is in raw or processed form.

    Args:
        filename (str): The name of the file for which the path is retrieved.
        data_is_raw (bool): A flag indicating whether the data is in raw (True) or processed (False) form.

    Returns:
        str: The full file path based on the provided filename and data form.
    """
    src_path = os.path.abspath(os.path.dirname(__file__))

    if data_is_raw:
        data_path = os.path.abspath(os.path.join(src_path, '..', '..', DATA_FOLDER, RAW, filename))
    else:
        data_path = os.path.abspath(os.path.join(src_path, '..', '..', DATA_FOLDER, PROCESSED, filename))

    return data_path


def save_file_to_data_folder(json_result: Any, output_file: str, data_is_raw: bool) -> None:
    """
    Saves json_result data to a specified output file within the data folder.

    Args:
        json_result (Any): The data to be saved. Should be provided in json format.
        output_file (str): The name of the output file.
        data_is_raw (bool): If true, the data is saved to "data/raw" folder (folder containing unprocessed data)
        otherwise the data is saved to "data/processed"
    """
    # Check if result is provided in json format.
    try:
        json.dumps(json_result)
    except TypeError:
        raise TypeError("The 'result' data is not in JSON format.")

    # Save result into the data/raw or data/processed folder
    dest_path = get_filepath(output_file, data_is_raw)
    with open(dest_path, 'w', encoding='utf-8') as f:
        json.dump(json_result, f, indent=4, ensure_ascii=False)
        print(f"Data saved to {dest_path}")


def read_file_from_data_folder(filename: str, data_is_raw: bool) -> Any:
    """
   Reads data from a file in data folder.

   Args:
       filename (str): The name of the file to read.
       data_is_raw (bool): Indicates whether the data is stored in the raw folder.
   """
    data_path = get_filepath(filename, data_is_raw)

    if not os.path.exists(data_path):
        print("No such file or directory: " + data_path)
        return None
    else:
        with open(data_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
