import os
import json
import requests
import logging
from api import gitlabhelper

locations_data = None

FILE_PATH = "./"
FILE_NAME = "locations.json"

def check_location_file_existence():
    return os.path.isfile(FILE_PATH + FILE_NAME)

def parse_file():
    if not check_location_file_existence():
        logging.warn(f"{FILE_NAME} doesn't exist")
        git_type = os.getenv('GIT_MODE', 'GITLAB')
        if git_type == "" or git_type == "GITLAB":
            logging.info("Gitlab type is specified")
            if not download_gitlab_file():
                return
        else:
            logging.info("Github type is specified")
            if not download_github_file():
                return
    with open(FILE_PATH + FILE_NAME) as file:
        try:
            data = json.load(file)
            global locations_data
            locations_data = data
        except Exception as e:
            logging.critical(f"Couldn't parse file due to {str(e)}")

def download_github_file():
    raw_link = os.getenv("GITHUB_RAW_FILE_LOCATION")
    logging.info(f"Downloading file from {raw_link}")
    if len(raw_link) == 0:
        logging.critical(f"Empty raw link {raw_link}")
        return False
    req = requests.get(raw_link)
    if req.status_code != 200:
        logging.critical(f"Something went wrong while downloading file {req.status_code}")
        return False
    logging.info("File Downloaded")
    if len(req.text) == 0:
        logging.warn("Empty Data downloaded")
        return write_to_file("{}", "w")
    print(req.text)
    return write_to_file(req.text, "w")

def download_gitlab_file():
    logging.info(f"Downloading file from gitlab")
    err, content = gitlabhelper.get_file_content()
    if err:
        logging.critical(f"Something went wrong while downloading file {err}")
        return False
    if content is None or len(content) == 0:
        logging.warn("Empty Data downloaded")
        return write_to_file("{}", "w")
    print(content)
    return write_to_file(content, "w")

def write_to_file(data, mode):
    try:
        with open(FILE_PATH + FILE_NAME, mode) as file:
            file.write(data)
        return True
    except Exception as e:
        logging.critical(f"Something went wrong while writing the file {str(e)}")
        return False
