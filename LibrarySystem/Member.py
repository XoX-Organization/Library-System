
from datetime import datetime

from .Common_Methods import Common
from .Database import DB_Member
from .Logging import get_logger, remove_handler

class Member:
    
    def __init__(self, ID):
        self.ID = ID
        self._database = None
        
    @property
    def database(self):
        if self._database == None:
            self._database = DB_Member.Retrieve()
        return self._database
    
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
            "Class": None,
            "Creation-Date": str(datetime.now()),
            "Entitlement": None,
            "Membership-Status": None,
            "Membership-Type": None,
            "Name": None,
            "One-Time-Deposit": None,
            "Penalty": None,
            "Renewal-Date": None,
            "Stock": {
                "Borrowing": {},
                "Returned": {}
            }
        }
        
        return Method.Register(self.ID, Base)
    
    @property
    def total_borrowing(self):
        total = len(self.database[self.ID]["Stock"]["Borrowing"].keys())
        return total
    
    def _BorrowStock(self, StockID):
        logger = get_logger("Member.BorrowStock")
        
        if not self.valid_ID:
            logger.info(f"Invalid {self.ID}")
            logger = remove_handler(logger)
            return False
        
        if StockID in self.database[self.ID]["Stock"]["Borrowing"]:
            logger.error("Serious ERROR had occured, please solve the bugs before next run to prevent Database CORRUPTED")
            raise Exception("Serious ERROR had occured, please solve the bugs before next run to prevent Database CORRUPTED")
        
        self.database[self.ID]["Stock"]["Borrowing"][StockID] = {
                                                                "Date-Borrowed": str(datetime.now())
                                                                }
        DB_Member.Dump(self.database)
        
        logger.info(f"Member {self.ID} had successfully borrowed stock {StockID}")
        logger = remove_handler(logger)
        
        return True
        
    def _ReturnStock(self, StockID):
        logger = get_logger("Member.ReturnStock")
        
        if not self.valid_ID:
            logger.info(f"Invalid {self.ID}")
            logger = remove_handler(logger)
            return False
        
        if StockID not in self.database[self.ID]["Stock"]["Borrowing"]:
            logger.error("Serious ERROR had occured, please solve the bugs before next run to prevent Database CORRUPTED")
            raise Exception("Serious ERROR had occured, please solve the bugs before next run to prevent Database CORRUPTED")
        
        date_borrowed = self.database[self.ID]["Stock"]["Borrowing"][StockID]["Date-Borrowed"]
        del self.database[self.ID]["Stock"]["Borrowing"][StockID]

        try: count = len(self.database[self.ID]["Stock"]["Returned"][StockID])
        except:
            count = 0
            self.database[self.ID]["Stock"]["Returned"][StockID] = {}
        
        self.database[self.ID]["Stock"]["Returned"][StockID][str(count + 1)] = {
                                                                                "Date-Borrowed": date_borrowed,
                                                                                "Date-Returned": str(datetime.now())
                                                                                }
            
        DB_Member.Dump(self.database)
        
        logger.info(f"Member {self.ID} had successfully returned back stock {StockID}")
        logger = remove_handler(logger)
        
        return True
        
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
