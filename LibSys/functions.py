# Title : Library System
# Programmer : Xian Yee
# Version : 0.0.0

import os
import sys
import json
import logging


logging.basicConfig(level = logging.DEBUG,
                    format = '%(asctime)s %(name)s %(levelname)s %(message)s',
                    datefmt = '%Y-%m-%d %H:%M:%S',
                    filename = 'LibSys.log',
                    filemode = 'a')

Console = logging.StreamHandler()
Console.setLevel(logging.INFO)
ConsoleFormat = logging.Formatter('%(message)s')
Console.setFormatter(ConsoleFormat)
logging.getLogger().addHandler(Console)


class Authentication:        
    
    def __init__(self, Username, Password):
        self.Database = SysDB.EmployeeRetrieve()
        self.Username = Username
        self.Password = Password
        
    def CheckExists(Username):
        return bool(Username in SysDB.EmployeeRetrieve().keys())
        
    def Login(self):
        AuthLogin = logging.getLogger("AuthLogin	")
        
        if self.Password == self.Database[self.Username]["Password"]:
            AuthLogin.info(f"Login successful as user {self.Username}")
            return True
        
        elif self.Password != self.Database[self.Username]["Password"]:
            AuthLogin.warning(f"Login failed as user {self.Username}")
            return False
    
    def Register(self):
        AuthRegister = logging.getLogger("AuthRegister	")
        
        self.Database[self.Username] = {"Password": self.Password}
        SysDB.EmployeeDump(self.Database)
        AuthRegister.info(f"Registration successful as user {self.Username}")
        
        return True

class Store:
    
    def __init__(self):
        pass
    
    def Insert(ID, BookTitle, Author, Subject):
        StoreInsertion = logging.getLogger("StoreInsertion	")
        
        Database = SysDB.StoreRetrieve()
        
        if ID not in Database.keys():
            Database[ID] = {
                "BookTitle": BookTitle,
                "Author": Author,
                "Subject": Subject
                            }
            StoreInsertion.info(f"ID: {ID}, BookTitle: {BookTitle}, Author: {Author}, Subject: {Subject} has been added successfully")
        
        elif ID in Database.keys():
            StoreInsertion.warning(f"ID: {ID} is existing, thus will not be added")
            
        SysDB.StoreDump(Database)
        
    def Delete(ID):
        StoreDeletion = logging.getLogger("StoreDeletion	")
        
        Database = SysDB.StoreRetrieve()
        
        if ID in Database.keys():
            Database.pop(ID)
            StoreDeletion.info(f"ID:{ID} has been deleted successfully")
            
        elif ID not in Database.keys():
            StoreDeletion.warning(f"ID:{ID} does not exist")
            
        SysDB.StoreDump(Database)
        
    def ListAll():
        StoreListFunc = logging.getLogger("StoreListFunc	")
        
        Database = SysDB.StoreRetrieve()
        List = [["ID", "Book Title", "Author", "Subject"]]
        
        if Database.keys():
            for ID in Database:
                List.append([ID, Database[ID]["BookTitle"], Database[ID]["Author"], Database[ID]["Subject"]])
                
            StoreListFunc.info("All the items retrieved successfully")
            return List
        
    def Search(ID = None, BookTitle = None, Author = None, Subject = None):
        StoreSearchFunc = logging.getLogger("StoreSearchFunc	")
        
        Database = SysDB.StoreRetrieve()
        List = [["ID", "Book Title", "Author", "Subject"]]
        ListID = []
        
        if (ID != None) or (BookTitle != None) or (Author != None) or (Subject != None):
            StoreSearchFunc.info(f"Given ID: {ID}, BookTitle: {BookTitle}, Author: {Author}, Subject: {Subject}, searching for similar item")
            
            for DBID, DBInfo in Database.items():
                for i in DBInfo:
                    if (ID in DBID) or (BookTitle in DBInfo[i]) or (Author in DBInfo[i]) or (Subject in DBInfo[i]):
                        if DBID not in ListID:
                            ListID.append(DBID)
                        
            for x in ListID:
                List.append([x, Database[x]["BookTitle"], Database[x]["Author"], Database[x]["Subject"]])
                        
            StoreSearchFunc.info(f"Finished searching by given ID: {ID}, BookTitle: {BookTitle}, Author: {Author}, Subject: {Subject}")
                    
        return List
                    
        
     
class SysDB:
    
    def __init__(self):
        pass
    
    def StoreRetrieve():
        SysDBStoreRetrieve = logging.getLogger("SysDBStoreRetrieve	")
        
        try:
            if os.stat("Store-DB.json").st_size != 0:
                with open("Store-DB.json", "r", encoding = "UTF-8") as f:
                    JSON = json.load(f)
                    SysDBStoreRetrieve.debug("Store-DB.json has been successfully loaded")
                    return JSON
            else:
                SysDBStoreRetrieve.debug("Store-DB.json is empty, will return {} value back to the requester to avoid JSONDecodeError")
                return {}
            
        except FileNotFoundError:
            SysDBStoreRetrieve.debug("Store-DB.json is not exists, will create a new Store-DB.json file")
            open("Store-DB.json", "w+", encoding = "UTF-8")
            return {}
        
        except json.decoder.JSONDecodeError:
            SysDBStoreRetrieve.critical("Store-DB.json has corrupted, please contact professional to fix it")
            sys.exit(1)
            
        
    def StoreDump(Database):
        SysDBStoreDump = logging.getLogger("SysDBStoreDump	")
        
        SysDB.StoreRetrieve()
        
        with open("Store-DB.json", "w", encoding = "UTF-8") as f:
            json.dump(Database, f, indent = 4, ensure_ascii = False, sort_keys = False)
            SysDBStoreDump.debug("The data has been successfully saved")
            
            
    #---------------------------------------------------------------------------------------------------#
            
                
    def EmployeeRetrieve():
        SysDBEmployeeRetrieve = logging.getLogger("SysDBEmployeeRetrieve	")
        
        try:
            if os.stat("Employee-DB.json").st_size != 0:
                with open("Employee-DB.json", "r", encoding = "UTF-8") as f:
                    JSON = json.load(f)
                    SysDBEmployeeRetrieve.debug("Employee-DB.json has been successfully loaded")
                    return JSON
            else:
                SysDBEmployeeRetrieve.debug("Employee-DB.json is empty, will return {} value back to the requester to avoid JSONDecodeError")
                return {}
            
        except FileNotFoundError:
            SysDBEmployeeRetrieve.debug("Employee-DB.json is not exists, will create a new Employee-DB.json file")
            open("Employee-DB.json", "w+", encoding = "UTF-8")
            return {}
        
        except json.decoder.JSONDecodeError:
            SysDBEmployeeRetrieve.critical("Employee-DB.json has corrupted, please contact professional to fix it")
            sys.exit(1)
            
        
    def EmployeeDump(Database):
        SysDBEmployeeDump = logging.getLogger("SysDBEmployeeDump	")
        
        SysDB.EmployeeRetrieve()
        
        with open("Employee-DB.json", "w", encoding = "UTF-8") as f:
            json.dump(Database, f, indent = 4, ensure_ascii = False, sort_keys = False)
            SysDBEmployeeDump.debug("The data has been successfully saved")
                
            
    #---------------------------------------------------------------------------------------------------#
            
                
    def MemberRetrieve():
        SysDBMemberRetrieve = logging.getLogger("SysDBMemberRetrieve	")
        
        try:
            if os.stat("Member-DB.json").st_size != 0:
                with open("Member-DB.json", "r", encoding = "UTF-8") as f:
                    JSON = json.load(f)
                    SysDBMemberRetrieve.debug("Member-DB.json has been successfully loaded")
                    return JSON
            else:
                SysDBMemberRetrieve.debug("Member-DB.json is empty, will return {} value back to the requester to avoid JSONDecodeError")
                return {}
            
        except FileNotFoundError:
            SysDBMemberRetrieve.debug("Member-DB.json is not exists, will create a new Member-DB.json file")
            open("Member-DB.json", "w+", encoding = "UTF-8")
            return {}
        
        except json.decoder.JSONDecodeError:
            SysDBMemberRetrieve.critical("Member-DB.json has corrupted, please contact professional to fix it")
            sys.exit(1)
            
        
    def MemberDump(Database):
        SysDBMemberDump = logging.getLogger("SysDBMemberDump	")
        
        SysDB.MemberRetrieve()
        
        with open("Member-DB.json", "w", encoding = "UTF-8") as f:
            json.dump(Database, f, indent = 4, ensure_ascii = False, sort_keys = False)
            SysDBMemberDump.debug("The data has been successfully saved")
                
        