
from datetime import datetime
from LibrarySystem.Common_Methods import Common

class Member:
    
    def __init__(self, ID):
        self.ID = ID
    
    @staticmethod
    def List(ID = None, Only_Modifiable = False):
        LOGGER_NAME = "Member.List"
        DATATYPE = "DB_Member"
        
        Method = Common(LOGGER_NAME, DATATYPE)
        return Method.List(ID = ID, Only_Modifiable = Only_Modifiable)
        
    @staticmethod
    def Search(*keywords):
        LOGGER_NAME = "Member.Search"
        DATATYPE = "DB_Member"
        
        Method = Common(LOGGER_NAME, DATATYPE)
        return Method.Search(*keywords)
    
    @property
    def valid_ID(self):
        LOGGER_NAME = None
        DATATYPE = "DB_Member"
        
        Method = Common(LOGGER_NAME, DATATYPE)
        return Method.valid_ID(self.ID)
    
    def Register(self):
        LOGGER_NAME = "Member.Register"
        DATATYPE = "DB_Member"
        
        Method = Common(LOGGER_NAME, DATATYPE)
        
        Base = {}
        Base[self.ID] = {
            "Annual-Fee": None,
            "Borrowing-Book": {},
            "History-Returned-Book": [],
            "Class": None,
            "Creation-Date": str(datetime.now()),
            "Entitlement": {
            },
            "Membership-Status": None,
            "Membership-Type": None,
            "Name": None,
            "One-Time-Deposit": None,
            "Penalty": None,
            "Renewal-Date": None
        }
        
        return Method.Register(self.ID, Base)
        
    def Modify(self, Key, Value):
        LOGGER_NAME = "Member.Modify"
        DATATYPE = "DB_Member"
        
        Method = Common(LOGGER_NAME, DATATYPE)
        return Method.Modify(self.ID, Key, Value)
        
    def Delete(self):
        LOGGER_NAME = "Member.Delete"
        DATATYPE = "DB_Member"
        
        Method = Common(LOGGER_NAME, DATATYPE)
        return Method.Delete(self.ID)
