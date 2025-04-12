import os 
import json

from pathlib import Path
from dotenv import load_dotenv
from helper import file_helper


# Get the path to the parent directory (where .env is located)
parent_dir = Path(__file__).resolve().parent.parent
env_path = parent_dir / ".env"
load_dotenv(dotenv_path=env_path)  

USER_API_KEY_PATH = Path(os.getenv( 'USER_API_KEY_PATH'))

    
def get_name_by_api_key ( INPUT_API_KEY ): 
    
    API_DATA_FROM_JSON = file_helper.read_json( USER_API_KEY_PATH )
    
    get_name = lambda k: next((item.get("name") for item in API_DATA_FROM_JSON if item.get("key") == k),  '-unknown-' )
    name = get_name ( INPUT_API_KEY )
    return name

def check_exist_api_key( api_key):
   
    API_DATA_FROM_JSON = file_helper.read_json( USER_API_KEY_PATH )
    
    if not isinstance(API_DATA_FROM_JSON, list):
        raise TypeError("Data must be a list.")

    if not isinstance(api_key, str):
        raise TypeError("API key must be a string.")

    for item in API_DATA_FROM_JSON:
        if not isinstance(item, dict):
            raise TypeError("Items in data must be dictionaries.")

        if "key" not in item:
            raise ValueError("Each item in data must contain a 'key'.")

        if item["key"] == api_key:
            return True

    return False