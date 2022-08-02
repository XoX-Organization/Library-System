
from datetime import datetime

from LibrarySystem.Common_Methods import Common

class Storing:
    
    def __init__(self, ID):
        self.ID = ID
    
    @staticmethod
    def List(ID = None, Only_Modifiable = False):
        LOGGER_NAME = "Storing.List"
        DATATYPE = "DB_Storing"
        
        Method = Common(LOGGER_NAME, DATATYPE)
        return Method.List(ID = ID, Only_Modifiable = Only_Modifiable)
        
    @staticmethod
    def Search(*keywords):
        LOGGER_NAME = "Storing.Search"
        DATATYPE = "DB_Storing"
        
        Method = Common(LOGGER_NAME, DATATYPE)
        return Method.Search(*keywords)
    
    @property
    def valid_ID(self):
        LOGGER_NAME = None
        DATATYPE = "DB_Storing"
        
        Method = Common(LOGGER_NAME, DATATYPE)
        return Method.valid_ID(self.ID)

    def Register(self):
        LOGGER_NAME = "Storing.Register"
        DATATYPE = "DB_Storing"
        
        Method = Common(LOGGER_NAME, DATATYPE)
        
        Base = {}
        Base[self.ID] = {
            "Author": None,
            "BookTitle": None,
            "Creation-Date": str(datetime.now()),
            "Pricing": None,
            "Subject": None,
            "Stock-Level": None
            }
        
        return Method.Register(self.ID, Base)

    def Modify(self, Key, Value):
        LOGGER_NAME = "Storing.Modify"
        DATATYPE = "DB_Storing"
        
        Method = Common(LOGGER_NAME, DATATYPE)
        return Method.Modify(self.ID, Key, Value)
        
    def Delete(self):
        LOGGER_NAME = "Storing.Delete"
        DATATYPE = "DB_Storing"
        
        Method = Common(LOGGER_NAME, DATATYPE)
        return Method.Delete(self.ID)
