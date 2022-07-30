# Title : Library System
# Programmer : Xian Yee
# Version : 0.0.0

import json
import logging
import os
import sys
from datetime import datetime

logging.basicConfig(level = logging.DEBUG,
                    format = '%(asctime)s %(name)s %(levelname)s %(message)s',
                    datefmt = '%Y-%m-%d %H:%M:%S',
                    filename = 'LibSys.log',
                    filemode = 'a')

Console = logging.StreamHandler()
Console.setLevel(logging.INFO)
console_format = logging.Formatter('%(message)s')
Console.setFormatter(console_format)
logging.getLogger().addHandler(Console)


class Authentication:        
    
    def __init__(self, Username, Password):
        self.database = SysDB.EmployeeRetrieve()
        self.username = Username
        self.password = Password
        
    def check_user(Username):
        return bool(Username in SysDB.EmployeeRetrieve().keys())
        
    def Login(self):
        AuthLogin = logging.getLogger("AuthLogin	")
        
        if self.password == self.database[self.username]["Password"]:
            AuthLogin.info(f"Login successful as user {self.username}")
            return True
        
        elif self.password != self.database[self.username]["Password"]:
            AuthLogin.warning(f"Login failed as user {self.username}")
            return False
    
    def Register(self):
        AuthRegister = logging.getLogger("AuthRegister	")
        
        self.database[self.username] = {"Password": self.password}
        SysDB.EmployeeDump(self.database)
        AuthRegister.info(f"Registration successful and logged in as user {self.username}")
        
        return True

class Store:
    
    def __init__(self, ID):
        self.id = ID
        self.database = SysDB.StoreRetrieve()
    
    def Insert(self, BookTitle, Author, Subject):
        StoreInsertion = logging.getLogger("StoreInsertion	")
        
        if self.id not in self.database.keys():
            Database[self.id] = {
                "BookTitle": BookTitle,
                "Author": Author,
                "Subject": Subject
                            }
            StoreInsertion.info(f"ID: {self.id}, BookTitle: {BookTitle}, Author: {Author}, Subject: {Subject} has been added successfully")
        
        elif self.id in self.database.keys():
            StoreInsertion.warning(f"ID: {self.id} is existing, thus will not be added")
            
        SysDB.StoreDump(self.database)
        
    def Modify(self, BookTitle, Author, Subject):
        pass
        
    def Delete(self):
        StoreDeletion = logging.getLogger("StoreDeletion	")
        
        if self.id in self.database.keys():
            self.database.pop(self.id)
            StoreDeletion.info(f"ID:{ID} has been deleted successfully")
            
        elif self.id not in self.database.keys():
            StoreDeletion.warning(f"ID:{ID} does not exist")
            
        SysDB.StoreDump(self.database)
        
    def ListAll():
        StoreListFunc = logging.getLogger("StoreListFunc	")
        
        Database = SysDB.StoreRetrieve()

        List = [["ID", "Book Title", "Author", "Subject"]]
        
        if Database.keys():
            for ID in Database:
                List.append([ID, Database[ID]["BookTitle"], Database[ID]["Author"], Database[ID]["Subject"]])
                
            StoreListFunc.info("All the items retrieved successfully")
            return List
        
    def Search(*keywords):
        
        StoreSearchFunc = logging.getLogger("StoreSearchFunc	")
        
        Database = SysDB.StoreRetrieve()

        List = [["ID", "Book Title", "Author", "Subject"]]
        ListID = []
        
        StoreSearchFunc.info(f"Given keywords: {keywords}, searching for similar item")
        
        for DBID, DBInfo in Database.items():
            for i in DBInfo:
                for y in keywords:
                    if (y in DBID) or (y in DBInfo[i]):
                        if DBID not in ListID:
                            ListID.append(DBID)
                    
        for x in ListID:
            List.append([x, Database[x]["BookTitle"], Database[x]["Author"], Database[x]["Subject"]])
                    
        StoreSearchFunc.info(f"Finished searching by given keywords: {keywords}")
                    
        return List
                    
        
class Member:
    
    def __init__(self, id):
        self.database = SysDB.MemberRetrieve()
        self.id = id
    
    def Modify(self, Key, Value):
        if self.id in self.database.keys():

            if Key.upper() in ("ANNUAL-FEE", "ANNUALFEE", "0"):
                self.database[self.id]["Annual-Fee"] = Value
                
            if Key.upper() in ("CLASS", "1"):
                self.database[self.id]["Class"] = Value
                
            if Key.upper() in ("MEMBERSHIP-STATUS","MEMBERSHIPSTATUS", "2"):
                self.database[self.id]["MembershipStatus"] = Value
                
            if Key.upper() in ("MEMBERSHIP-TYPE, ""MEMBERSHIPTYPE", "3"):
                self.database[self.id]["MembershipType"] = Value
                
            if Key.upper() in ("NAME", "4"):
                self.database[self.id]["Name"] = Value
                
            if Key.upper() in ("ONE-TIME-DEPOSIT", "ONETIMEDEPOSIT", "5"):
                self.database[self.id]["OneTimeDeposit"] = Value
                
            if Key.upper() in ("PENALTY", "6"):
                self.database[self.id]["Penalty"] = Value
                
            if Key.upper() in ("RENEWAL-DATE", "RENEWALDATE", "7"):
                self.database[self.id]["RenewalDate"] = Value
                
        elif self.id not in self.database.keys():
            pass
        
        SysDB.MemberDump(self.database)
    
    def Create(self):
        self.database[self.id] = {
            "Annual-Fee": None,
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
        
        SysDB.MemberDump(self.database)
        
    def Read(self):
        List = [["Key", "Value"]]
        
        for key, value in self.database[self.id].items():
            List.append([key, value])
        
        return List
    
    def Delete(self):
        self.database.pop(self.id)
        
        SysDB.MemberDump(self.database)
    
    
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
                
        