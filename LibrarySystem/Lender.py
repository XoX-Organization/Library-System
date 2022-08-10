
from datetime import datetime

from .Database import DB_Storing, DB_Member
from .Logging import get_logger, remove_handler

class Lender:

    def __init__(self, MemberID):
        self.db_storing = DB_Storing.Retrieve()
        self.db_member = DB_Member.Retrieve()
        self.member_id = MemberID
            
    @property
    def valid_ID(self):
        return bool(self.member_id in self.db_member.keys())

    def Borrow(self, BookID):
        logger = get_logger("Lender.Borrow")
        
        if self.valid_ID is False:
            logger.info(f"Member {self.member_id} is not valid")
            logger = remove_handler(logger)
            return False
        
        if BookID not in self.db_storing.keys():
            logger.info(f"Book {BookID} is not valid")
            logger = remove_handler(logger)
            return False
        
        if self.db_storing[BookID]["Stock-Level"] in (None, 0):
            logger.warning(f"Book {BookID} out of stock")
            logger = remove_handler(logger)
            return False
        
        total_number = 0
        for x in self.db_member[self.member_id]["Borrowing-Book"].keys():
            total_number += len(self.db_member[self.member_id]["Borrowing-Book"][x].keys())
        
        if total_number >= 5:
            logger.info(f"Member {self.member_id} already owns 5 books which are the max number of a member can hold at a time")
            logger = remove_handler(logger)
            return False
        
        if BookID in self.db_member[self.member_id]["Borrowing-Book"]:
            length = len(self.db_member[self.member_id]["Borrowing-Book"][BookID])
            self.db_member[self.member_id]["Borrowing-Book"][BookID][length + 1] = str(datetime.now())
        else:
            self.db_member[self.member_id]["Borrowing-Book"][BookID] = {1: str(datetime.now())}
        
        self.db_storing[BookID]["Stock-Level"] -= 1
        
        DB_Storing.Dump(self.db_storing)
        DB_Member.Dump(self.db_member)
        
        logger.info(f"Book {BookID} successfully lend to Member {self.member_id}")
        logger = remove_handler(logger)
        return True
        
    def Return(self, BookID):
        logger = get_logger("Lender.Return")
        
        if self.valid_ID is False:
            logger.info(f"Member {self.member_id} is not valid")
            logger = remove_handler(logger)
            return False
        
        if BookID not in self.db_storing.keys():
            logger.info(f"Book {BookID} is not valid")
            logger = remove_handler(logger)
            return False
        
        if BookID not in self.db_member[self.member_id]["Borrowing-Book"].keys():
            logger.info(f"Member {self.member_id} is not borrowing Book {BookID}")
            logger = remove_handler(logger)
            return False
        
        if len(self.db_member[self.member_id]["Borrowing-Book"][BookID]) > 1:
            length = len(self.db_member[self.member_id]["Borrowing-Book"][BookID])
            del self.db_member[self.member_id]["Borrowing-Book"][BookID][str(length)]
        else:
            del self.db_member[self.member_id]["Borrowing-Book"][BookID]
            
        self.db_member[self.member_id]["History-Returned-Book"].append([BookID, str(datetime.now())])
        
        self.db_storing[BookID]["Stock-Level"] += 1
        
        DB_Storing.Dump(self.db_storing)
        DB_Member.Dump(self.db_member)
        
        logger.info(f"Member {self.member_id} successfully returned back Book {BookID}")
        logger = remove_handler(logger)
        return True
        
