
import os

from jsonmerge import merge
from difflib import SequenceMatcher

from LibrarySystem.Logging import get_logger, remove_handler
from LibrarySystem.Database import DB_Storing, DB_Member, DB_Employee
from LibrarySystem.Constants import *

class Common:
    
    def __init__(self, LOGGER_NAME, DATATYPE):
        self.logger_name = LOGGER_NAME
        self.datatype = DATATYPE
        
        if DATATYPE not in ("DB_Storing", "DB_Employee", "DB_Member"):
            raise Exception(f"Invalid parameter DATATYPE: {DATATYPE}")
        elif DATATYPE == "DB_Storing":
            self.db = DB_Storing
            self.database = DB_Storing.Retrieve()
        elif DATATYPE == "DB_Employee":
            self.db = DB_Employee
            self.database = DB_Employee.Retrieve()
        elif DATATYPE == "DB_Member":
            self.db = DB_Member
            self.database = DB_Member.Retrieve()
            
    def List(self, ID = None, Only_Modifiable = False):
        logger = get_logger(self.logger_name)
        
        if not self.database.keys():
            logger.warning("Database is empty.")

        List = []
        SList = ["ID"]
        
        for y in self.database.values():
            for yx in y:
                
                if Only_Modifiable == True:
                    if yx in UNMODIFIABLE_LIST:
                        continue
                    
                SList.append(yx)
            break
        List.append(SList)
        
        if ID == None:
            for x, y in self.database.items():
                SList = [x]
                for yx in y:
                    
                    if Only_Modifiable == True:
                        if yx in UNMODIFIABLE_LIST:
                            continue
                    
                    SList.append(self.database[x][yx])
                List.append(SList)
            
        elif ID != None:
            SList = [ID]
            for x in self.database[ID].keys():
                    
                if Only_Modifiable == True:
                    if x in UNMODIFIABLE_LIST:
                        continue
                
                SList.append(self.database[ID][x])
            List.append(SList)
            
        logger = remove_handler(logger)
                
        return List
        
    def Search(self, *keywords):
        logger = get_logger(self.logger_name)
        
        if not self.database.keys():
            logger.warning("Database is empty.")
            logger = remove_handler(logger)
            return False
        
        ListID = []
        for x, y in self.database.items():
            for yx in y:
                for z in keywords:
                    if (SequenceMatcher(None, str(z), str(x)).ratio() >= 0.7) or (SequenceMatcher(None, str(z), str(self.database[x][yx])).ratio() >= 0.7):
                        if x not in ListID:
                            ListID.append(x)
                            
        SList = ["ID"]
        for x, y in self.database.items():
            for yx in y:
                SList.append(yx)
            break
        List = []
        List.append(SList)
        
        for x in ListID:
            SList = [x]
            for y in self.database[x]:
                SList.append(self.database[x][y])
            List.append(SList)
                    
        logger.info(f"Finished searching by given keywords: {keywords}")
        
        logger = remove_handler(logger)
        
        return List
    
    def valid_ID(self, ID):
        return bool(ID in self.database.keys())
    
    def Register(self, ID, DATADUMP):
        logger = get_logger(self.logger_name)
        
        if self.valid_ID(ID):
            logger.info(f"{ID} is existing, thus will not be added")
            logger = remove_handler(logger)
            return False
        
        Final = merge(DATADUMP, self.database)
        
        self.db.Dump(Final)
        logger.info(f"{ID} has been added successfully")
        
        logger = remove_handler(logger)
        
        return True
        
    def Modify(self, ID, Key, Value):
        logger = get_logger(self.logger_name)
        if Value == "":
            Value = None
        
        if not self.valid_ID(ID):
            logger.info(f"Invalid {ID}, please register")
            logger = remove_handler(logger)
            return False
        
        for x in self.database[ID].keys():
            if x in UNMODIFIABLE_LIST:
                continue
            
            if SequenceMatcher(None, Key, x).ratio() >= 0.7:
                old_value = self.database[ID][x]
                self.database[ID][x] = Value
                logger.info(f"({x}) of ({ID}) has been changed from ({old_value}) -> ({Value})")
                break
        else:
            logger.info(f"Invalid Key: {Key}")
            logger = remove_handler(logger)
            return False
        
        self.db.Dump(self.database)
        
        logger = remove_handler(logger)
        
        return True
        
    def Delete(self, ID):
        logger = get_logger(self.logger_name)
        
        if not self.valid_ID(ID):
            logger.info(f"Invalid {ID}")
            logger = remove_handler(logger)
            return False
        
        del self.database[ID]
        logger.info(f"Deletion successful for {ID}")
        self.db.Dump(self.database)
        
        logger = remove_handler(logger)
        
        return True
