import os
import json
import requests

locations_data = None

FILE_PATH = "./"
FILE_NAME = "locations.json"

def check_location_file_existence():
    return os.path.isfile(FILE_PATH + FILE_NAME)

def parse_file():
    if not check_location_file_existence():
        print(f"{FILE_NAME} doesn't exist")
        if not download_file():
            return
    with open(FILE_PATH + FILE_NAME) as file:
        try:
            data = json.load(file)
            global locations_data
            locations_data = data
        except Exception as e:
            print(f"Couldn't parse file due to {str(e)}")

def download_file():
    raw_link = os.getenv("RAW_FILE_LOCATION")
    print(f"Downloading file from {raw_link}")
    if len(raw_link) == 0:
        print(f"Empty raw link {raw_link}")
        return False
    req = requests.get(raw_link)
    if req.status_code != 200:
        print(f"Something went wrong while downloading file {req.status_code}")
        return False
    print("File Downloaded")
    if len(req.text) == 0:
        print("Empty Data downloaded")
        return write_to_file("{}", "w")
    return write_to_file(req.text, "w")

def write_to_file(data, mode):
    try:
        with open(FILE_PATH + FILE_NAME, mode) as file:
            file.write(data)
        return True
    except Exception as e:
        print(f"Something went wrong while writing the file {str(e)}")
        return False
