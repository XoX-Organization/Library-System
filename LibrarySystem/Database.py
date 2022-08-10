
import os
import json
import traceback

from .Logging import get_logger, remove_handler, shutdown
from .Path import Path


def valid_JSON(FILE_NAME):
    logger = get_logger("DB_Validation")
    
    FILE_PATH = Path().user_data_roaming_dir
    FILE = os.path.join(FILE_PATH, FILE_NAME)
    
    while True:
        try:
            if os.stat(FILE).st_size == 0:
                open(FILE, "w").write("{}")
                
            with open(FILE, "r", encoding = "UTF-8") as f:
                json.load(f)
                
                logger = remove_handler(logger)
                
                return True
            
        except json.decoder.JSONDecodeError:
            logger.error(traceback.format_exc())
            shutdown()
            raise SystemExit(1)
        
        except FileNotFoundError:
            open(FILE, "w+", encoding = "UTF-8")
            logger.debug(f"{FILE_NAME} is created as it doesn't exist")

def pull_data(LOGGER_NAME, FILE_NAME):
    logger = get_logger(LOGGER_NAME)
    
    FILE_PATH = Path().user_data_roaming_dir
    FILE = os.path.join(FILE_PATH, FILE_NAME)
    
    valid_JSON(FILE_NAME)
    
    with open(FILE, "r", encoding = "UTF-8") as f:
        JSON = json.load(f)
        logger.debug(f"{FILE_NAME} has been successfully loaded")
        
        logger = remove_handler(logger)
        
        return JSON
            
def push_data(LOGGER_NAME, FILE_NAME, DUMP_DATA):
    logger = get_logger(LOGGER_NAME)
    
    FILE_PATH = Path().user_data_roaming_dir
    FILE = os.path.join(FILE_PATH, FILE_NAME)
        
    valid_JSON(FILE_NAME)
    
    with open(FILE, "w", encoding = "UTF-8") as f:
        json.dump(DUMP_DATA, f, indent = 4, ensure_ascii = False, sort_keys = False)
        logger.debug(f"Data has been dumped successfully into {FILE_NAME}")
        
        logger = remove_handler(logger)
        
        return True


class DB_Employee:
    
    def Retrieve():
        return pull_data("DB_Employee.Retrieve", "DB_Employee.json")
        
    def Dump(Database):
        push_data("DB_Employee.Dump", "DB_Employee.json", Database)
        
class DB_Member:
    
    def Retrieve():
        return pull_data("DB_Member.Retrieve", "DB_Member.json")
        
    def Dump(Database):
        push_data("DB_Member.Dump", "DB_Member.json", Database)

class DB_Storing:
    
    def Retrieve():
        return pull_data("DB_Storing.Retrieve", "DB_Storing.json")
        
    def Dump(Database):
        push_data("DB_Storing.Dump", "DB_Storing.json", Database)
        