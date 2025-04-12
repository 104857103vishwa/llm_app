import json
import os
from pathlib import Path


from dotenv import load_dotenv
from fastapi import HTTPException

# LOGGER

import logging_config
import logging

logger = logging.getLogger(__name__)


# ENV
load_dotenv()
USER_API_KEY_PATH = os.getenv('USER_API_KEY_PATH')


def create_json ( payload ) -> bool: 
    try:
        with open(USER_API_KEY_PATH, 'w') as file:
             json.dump(payload, file, indent=4)
       
    except Exception as e:
        
        logger.warning("A warning")
        raise HTTPException(status_code=500, detail=f"Error storing API key: {e}")
    
def write_json(payload):
   
    USER_API_KEY_PATH = Path( os.getenv('USER_API_KEY_PATH') ) 

    try:
        if USER_API_KEY_PATH.exists():
            with USER_API_KEY_PATH.open("r") as file:
                try:
                    existing_data = json.load(file)
                    if not isinstance(existing_data, list): #Added check to make sure the data is a list.
                        existing_data = [] #If it is not a list, then start with an empty list.
                except json.JSONDecodeError:
                    existing_data = []
        else:
            existing_data = []

        existing_data.append(payload)

        with USER_API_KEY_PATH.open("w") as file:
            json.dump(existing_data, file, indent=4)

        return {"message": "Data appended successfully"}
        
        # raise ValueError("This is a test exception")

    except Exception as e:
        logger.warning(f" {e} ")
        raise HTTPException(status_code=500, detail=f"Error appending data: {e}")


def read_json( path: str): 
    try:
        with open(path, 'r') as file:
             data = json.load(file)
             return data 
    except Exception as e:
        logger.error(f" {e} ")
        raise HTTPException(status_code=500, detail=f"Error reading API key: {e}")
 
 
def read_txt(PATH):
    try:
        with open(PATH, "r", encoding="utf-8") as file:
           
            data = file.read()
            return data 
    except Exception as e:
        logger.error(f" {e} ")
        raise HTTPException(status_code=500, detail=f"Error reading API key: {e}")