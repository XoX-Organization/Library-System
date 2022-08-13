
from datetime import datetime
from tabulate import tabulate

from .Common_Methods import Common
from .Database import DB_Storing
from .Logging import get_logger, get_receipt_logger, remove_handler
from .Member import Member
from .Path import Path

class Storing:
    
    def __init__(self, ID):
        self.ID = ID
    
    @property
    def database(self):
        try: self._database
        except: self._database = DB_Storing.Retrieve()
        return self._database
    
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

        if self.ID not in self.database:
            return False
        
        return True
        
    @property
    def valid_StockID(self):
        
        try: BaseID = self.ID[:-5]
        except: return False
        
        if BaseID not in self.database:
            return False
        
        StockString = self.ID[-5:]
        
        if self.ID not in self.database[BaseID]["Stock"]:
            return False
        
        self.base_id = BaseID
        
        return True

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
            "Stock": {}
            }
        
        return Method.Register(self.ID, Base)
    
    def AddStock(self):
        logger = get_logger("Storing.AddStock")
        
        if not self.valid_ID:
            logger.info(f"Invalid {self.ID}")
            logger = remove_handler(logger)
            return False
        
        total_stock = len(self.database[self.ID]["Stock"])
        
        if total_stock >= 99999:
            logger.critical(f"Base Item {self.ID} has reached the maximum stock amounts ({total_stock})")
            logger = remove_handler(logger)
            return False
        
        level = total_stock + 1
        stock_new_id = self.ID + str(level).zfill(5)
        
        self.database[self.ID]["Stock"][stock_new_id] = {
            "Date-Added": str(datetime.now()),
            "Date-Sold": None,
            "Latest-Date-Lent": None,
            "Latest-Date-Returned": None,
            "Latest-Member-Borrowed": None,
            "Status": "Available"
        }
        
        logger.info(f'New stock ({stock_new_id}) -> Base ({self.ID}) , Currently left ({len(self.StockLeft())}) in storage.')
        DB_Storing.Dump(self.database)
        
        logger = remove_handler(logger)
        return stock_new_id
        
    def DeleteStock(self):
        logger = get_logger("Storing.DeleteStock")
        
        if not self.valid_StockID:
            logger.info(f"Invalid {self.ID}")
            logger = remove_handler(logger)
            return False
        
        if self.database[self.base_id]["Stock"][self.ID]["Status"] in ("Lending", "Sold", "Deleted"):
            logger.info(f"Stock {self.ID} is not available right now")
            logger = remove_handler(logger)
            return False
        
        initial_status = self.database[self.base_id]["Stock"][self.ID]["Status"]
        self.database[self.base_id]["Stock"][self.ID]["Status"] = "Deleted"
        DB_Storing.Dump(self.database)
        
        logger.info(f'Status of stock ({self.ID}): ({initial_status}) -> (Deleted) , Currently left ({len(self.StockLeft())}) in storage ({self.base_id}).')
        logger = remove_handler(logger)
        
        return True
        
    @staticmethod
    def SellStock(EmployeeID, *StockID, JustCheckPriceOnly = True):
        logger = get_logger("Storing.SellStock")
        
        database = DB_Storing.Retrieve()
        subtotal = 0
        stock_available = []
        stock_list = [["STOCK ID", "BOOK TITLE", "PRICING"]]
        
        for stock_id in StockID:
            
            try: BaseID = stock_id[:-5]
            except:
                logger.info(f"Invalid {stock_id}")
                continue
            
            if BaseID not in database:
                logger.info(f"Invalid {stock_id}")
                continue
            
            if stock_id not in database[BaseID]["Stock"]:
                logger.info(f"Invalid {stock_id}")
                continue
        
            if database[BaseID]["Stock"][stock_id]["Status"] in ("Lending", "Sold", "Deleted"):
                logger.info(f"Stock {stock_id} is not available right now")
                continue
            
            price = database[BaseID]["Pricing"]
            if price == None:
                logger.info(f"Item {BaseID} haven't set a price yet")
                continue
                
            stock_available.append(stock_id)
            subtotal += float(price)
            stock_title = database[BaseID]["BookTitle"]
            stock_list.append([stock_id, stock_title, price])

            if JustCheckPriceOnly == False:
                initial_status = database[BaseID]["Stock"][stock_id]["Status"]
                database[BaseID]["Stock"][stock_id]["Status"] = "Sold"
                database[BaseID]["Stock"][stock_id]["Date-Sold"] = str(datetime.now())
                DB_Storing.Dump(database)
                
                
                logger.info(f"Status of stock ({stock_id}): ({initial_status}) -> (Sold)")
            
        
        else:
            if (JustCheckPriceOnly == False) and (len(stock_list) > 1):
                logger_receipt = get_receipt_logger(EmployeeID)
                logger_receipt.info(tabulate(
                                                stock_list,
                                                headers = "firstrow",
                                                tablefmt = "grid",
                                                showindex = True,
                                                missingval = "N/A"
                                            ) +
                                    f"\nSUBTOTAL: {subtotal}"
                                    )
                logger_receipt = remove_handler(logger_receipt)
                
            logger = remove_handler(logger)
            return stock_list, stock_available, subtotal
        
    def LendStock(self, MemberID = None):
        logger = get_logger("Storing.LendStock")
        
        member = Member(MemberID)
        
        if MemberID != None:
            if not member.valid_ID:
                logger.info(f"Invalid Member ID {MemberID}")
                logger = remove_handler(logger)
                return False
        
        if not self.valid_StockID:
            logger.info(f"Invalid {self.ID}")
            logger = remove_handler(logger)
            return False
        
        if member.total_borrowing >= 5:
            logger.info(f"{MemberID} has total of {member.total_borrowing} books which has reached the maximum")
            logger = remove_handler(logger)
            return False
        
        if self.database[self.base_id]["Stock"][self.ID]["Status"] in ("Lending", "Sold", "Deleted"):
            logger.info(f"Stock {self.ID} is not available right now")
            logger = remove_handler(logger)
            return False
        
        initial_status = self.database[self.base_id]["Stock"][self.ID]["Status"]
        self.database[self.base_id]["Stock"][self.ID]["Status"] = "Lending"
        self.database[self.base_id]["Stock"][self.ID]["Latest-Date-Lent"] = str(datetime.now())
        self.database[self.base_id]["Stock"][self.ID]["Latest-Date-Returned"] = None
        self.database[self.base_id]["Stock"][self.ID]["Latest-Member-Borrowed"] = None
        
        if MemberID != None:
            self.database[self.base_id]["Stock"][self.ID]["Latest-Member-Borrowed"] = MemberID
            member._BorrowStock(self.ID)
        
        DB_Storing.Dump(self.database)
        
        logger.info(f'Status of stock ({self.ID}): ({initial_status}) -> (Lending) -> Member ({MemberID}) , Currently left ({len(self.StockLeft())}) in storage ({self.base_id}).')
        logger = remove_handler(logger)
        
        return True
    
    def ReturnStock(self):
        logger = get_logger("Storing.ReturnStock")
        
        if not self.valid_StockID:
            logger.info(f"Invalid {self.ID}")
            logger = remove_handler(logger)
            return False
        
        if self.database[self.base_id]["Stock"][self.ID]["Status"] in ("Available", "Sold", "Deleted"):
            logger.info(f"Stock {self.ID} is currently available right now, perhaps you entered a wrong stock id?")
            logger = remove_handler(logger)
            return False
        
        initial_status = self.database[self.base_id]["Stock"][self.ID]["Status"]
        self.database[self.base_id]["Stock"][self.ID]["Status"] = "Available"
        self.database[self.base_id]["Stock"][self.ID]["Latest-Date-Returned"] = str(datetime.now())
        
        MemberID = self.database[self.base_id]["Stock"][self.ID]["Latest-Member-Borrowed"]
        if MemberID != None:
            Member(MemberID)._ReturnStock(self.ID)
        
        DB_Storing.Dump(self.database)
        
        logger.info(f'Status of stock ({self.ID}): ({initial_status}) -> (Available) , Currently left ({len(self.StockLeft())}) in storage ({self.base_id}).')
        logger = remove_handler(logger)
        
        return True
    
    def StockLeft(self):
        logger = get_logger("Storing.StockLeft")
        
        base_id = self.ID
        if not self.valid_ID:
            if not self.valid_StockID:
                logger.info(f"Invalid {self.ID}")
                logger = remove_handler(logger)
                return False
            
            base_id = self.ID[:-5]
        
        stock_available_list = []
        for stock in self.database[base_id]["Stock"]:
            if self.database[base_id]["Stock"][stock]["Status"] == "Available":
                stock_available_list.append(stock)
                    
        return stock_available_list
        
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
