
import bcrypt

from datetime import datetime

from .Common_Methods import Common
from .Database import DB_Employee
from .Logging import get_logger, remove_handler


class Employee:
    
    def __init__(self, ID):
        self.ID = ID
        
    @property
    def database(self):
        try: self._database
        except: self._database = DB_Employee.Retrieve()
        return self._database
        
    @staticmethod
    def List(ID = None, Only_Modifiable = False):
        LOGGER_NAME = "Employee.List"
        DATATYPE = "DB_Employee"
        
        Method = Common(LOGGER_NAME, DATATYPE)
        return Method.List(ID = ID, Only_Modifiable = Only_Modifiable)
    
    @staticmethod
    def Search(*keywords):
        LOGGER_NAME = "Employee.Search"
        DATATYPE = "DB_Employee"
        
        Method = Common(LOGGER_NAME, DATATYPE)
        return Method.Search(*keywords)
    
    @staticmethod
    def hash_password(password):
        byte_pass = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(byte_pass, salt)
        return hashed
        
    @property
    def valid_ID(self):
    
        if self.ID not in self.database:
            return False
        
        return True
    
    def Login(self, password):
        logger = get_logger("Employee.Login")
        
        if not self.valid_ID:
            logger.info(f"Invalid {self.ID}, please register")
            logger = remove_handler(logger)
            return False
        
        if "BCrypt-Pass" in self.database[self.ID].keys():
            hashed_pass = self.database[self.ID]["BCrypt-Pass"]
            if bcrypt.checkpw(password.encode('utf-8'), hashed_pass.encode('utf-8')):
                logger.info(f"Login successful as user {self.ID}")
                logger = remove_handler(logger)
                    
                return True
            
        elif "Password" in self.database[self.ID].keys() == False:
            if password == self.database[self.ID]["Password"]:
                logger.info(f"Login successful as user {self.ID}")
                logger = remove_handler(logger)
                    
                return True
        
        logger.info(f"Password incorrect as user {self.ID}")
        
        logger = remove_handler(logger)
        
        return False

    def Register(self, password, hashed = True):
        LOGGER_NAME = "Employee.Register"
        DATATYPE = "DB_Employee"
        
        Method = Common(LOGGER_NAME, DATATYPE)
        
        Base = {}
        Base[self.ID] = {
            "Address": None,
            "Contact-Number": None,
            "Creation-Date": str(datetime.now()),
            "Email": None,
            "Emergency-Contact-Number": None,
            "Full-Name": None
            }
        
        if hashed != False:
            hashed_pass = Employee.hash_password(password)
            Base[self.ID]["BCrypt-Pass"] = hashed_pass.decode()
            
        elif hashed == False:
            Base[self.ID]["Password"] = password
        
        return Method.Register(self.ID, Base)

    def Modify(self, Key, Value):
        LOGGER_NAME = "Employee.Modify"
        DATATYPE = "DB_Employee"
        
        Method = Common(LOGGER_NAME, DATATYPE)
        return Method.Modify(self.ID, Key, Value)

    def Delete(self):
        LOGGER_NAME = "Employee.Delete"
        DATATYPE = "DB_Employee"
        
        Method = Common(LOGGER_NAME, DATATYPE)
        return Method.Delete(self.ID)
