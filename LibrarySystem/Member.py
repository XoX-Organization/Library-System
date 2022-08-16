
from datetime import datetime, timedelta

from .Common_Methods import Common
from .Database import DB_Member
from .Logging import get_logger, remove_handler

class Member:
    
    def __init__(self, ID):
        self.ID = ID
        
    @property
    def database(self):
        try: self._database
        except: self._database = DB_Member.Retrieve()
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
        valid_logger = get_logger("Member.valid_ID")
        
        if self.ID not in self.database:
            valid_logger = remove_handler(valid_logger)
            return False
        
        if self.database[self.ID]["Membership-Status"].upper() in ["BARRED", "DEACTIVATED"]:
            status = self.database[self.ID]["Membership-Status"]
            valid_logger.info(f"Member {self.ID} has been {status}")
            valid_logger = remove_handler(valid_logger)
            return False
        
        valid_logger = remove_handler(valid_logger)
        return True
    
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
            "Membership-Status": "Active",
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
                                                                "Date-Borrowed": str(datetime.now()),
                                                                "Due-Date": str(datetime.now() + timedelta(days = 7))
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
        
        penalty = self._PenaltyLateReturn(StockID)
        if penalty > 0:
            try:
                while True:
                    if input(f'Enter "CONFIRM" after the payment (RM {penalty:.2f}) is made to continue: ') == "CONFIRM":
                        break
            except:
                logger.warning("Payment transaction failed, please try again")
                return False
        
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
    
    @property
    def TotalPenalty(self):
        total = 0
        
        for stock_id in self.database[self.ID]["Stock"]["Borrowing"]:
            total += self._PenaltyLateReturn(stock_id)
        
        return total
    
    def _PenaltyLateReturn(self, StockID):
        logger = get_logger("Member._PenaltyLateReturn")
        
        if not self.valid_ID:
            logger.info(f"Invalid {self.ID}")
            logger = remove_handler(logger)
            return False
        
        if StockID not in self.database[self.ID]["Stock"]["Borrowing"]:
            logger.critical(f"{StockID} is not borrowed by {self.ID}")
            logger = remove_handler(logger)
            return False
        
        due_date = datetime.strptime(self.database[self.ID]["Stock"]["Borrowing"][StockID]["Due-Date"], "%Y-%m-%d %H:%M:%S.%f")
        
        if due_date >= datetime.now():
            logger = remove_handler(logger)
            return 0
        
        time_delta = datetime.now() - due_date
        time_delta_seconds = time_delta.total_seconds() # Convert timedelta class into seconds
        time_delta_days = time_delta_seconds // 86400 # 1 day 86400 seconds
        subtotal = time_delta_days * 0.5 # 1 day RM0.50
        
        logger = remove_handler(logger)
        return subtotal
    
    def ListBorrowing(self):
        logger = get_logger("Member.ListBorrowing")
        
        if not self.valid_ID:
            logger.info(f"Invalid {self.ID}")
            logger = remove_handler(logger)
            return False
        
        if not self.database[self.ID]["Stock"]["Borrowing"]:
            logger.warning("Database is empty")
            logger = remove_handler(logger)
            return False
        
        ### Getting the headers of the table
        List = []
        SList = ["Stock-ID"]
        for y in self.database[self.ID]["Stock"]["Borrowing"].values():
            for yx in y:
                if yx not in SList:
                    SList.append(yx)
            
        SList.append("Subtotal-Penalty")
        List.append(SList)
        
        
        ### Getting the data of the table
        for stock_id in self.database[self.ID]["Stock"]["Borrowing"].keys():
            SList = [stock_id]
            
            for header in List[0]:
                if header in ("Stock-ID", "Subtotal-Penalty"):
                    continue
                
                SList.append(self.database[self.ID]["Stock"]["Borrowing"][stock_id][header])
                
            List.append(SList)
            
        ### Getting the subtotal of the penalty
        for i in range(1, len(List)):
            stock_id = List[i][0]
            penalty = self._PenaltyLateReturn(stock_id)
            List[i].append(penalty)
        
        
        ### Print total of penalty
        SList = []
        for i in range(1, len(List[0])):
            SList.append("")
            
        SList.append("Total-Penalty: RM {:.2f}".format(self.TotalPenalty))
        List.append(SList)
        
        logger = remove_handler(logger)
        return List
        
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
