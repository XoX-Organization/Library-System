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

class Store:
    
    def __init__(self):
        pass
    
    def Insert(ID, BookTitle, Author, Subject):
        StoreInsertion = logging.getLogger("StoreInsertion	")
        
        Database = SysDB.Retrieve()
        
        if ID not in Database.keys():
            Database[ID] = {
                "BookTitle": BookTitle,
                "Author": Author,
                "Subject": Subject
                            }
            StoreInsertion.info(f"ID: {ID}, BookTitle: {BookTitle}, Author: {Author}, Subject: {Subject} has been added successfully")
        
        elif ID in Database.keys():
            StoreInsertion.warning(f"ID: {ID} is existing, thus will not be added")
            
        SysDB.Dump(Database)
        
    def Delete(ID):
        StoreDeletion = logging.getLogger("StoreDeletion	")
        
        Database = SysDB.Retrieve()
        
        if ID in Database.keys():
            Database.pop(ID)
            StoreDeletion.info(f"ID:{ID} has been deleted successfully")
            
        elif ID not in Database.keys():
            StoreDeletion.warning(f"ID:{ID} does not exist")
            
        SysDB.Dump(Database)
        
    def ListAll():
        StoreListFunc = logging.getLogger("StoreListFunc	")
        
        Database = SysDB.Retrieve()
        List = [["ID", "Book Title", "Author", "Subject"]]
        
        if Database.keys():
            for ID in Database:
                List.append([ID, Database[ID]["BookTitle"], Database[ID]["Author"], Database[ID]["Subject"]])
                
            StoreListFunc.info("All the items retrieved successfully")
            return List
        
    def Search(ID = None, BookTitle = None, Author = None, Subject = None):
        StoreSearchFunc = logging.getLogger("StoreSearchFunc	")
        
        Database = SysDB.Retrieve()
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
    
    def Retrieve():
        SysDBRetrieve = logging.getLogger("SysDBRetrieve	")
        
        try:
            if os.stat("Database.json").st_size != 0:
                with open("Database.json", "r", encoding = "UTF-8") as f:
                    JSON = json.load(f)
                    SysDBRetrieve.debug("Database.json has been successfully loaded")
                    return JSON
            else:
                SysDBRetrieve.debug("Database.json is empty, will return {} value back to the requester to avoid JSONDecodeError")
                return {}
            
        except FileNotFoundError:
            SysDBRetrieve.debug("Database.json is not exists, will create a new Database.json file")
            open("Database.json", "w+", encoding = "UTF-8")
            return {}
        
        except json.decoder.JSONDecodeError:
            SysDBRetrieve.critical("Database.json has corrupted, please contact professional to fix it")
            sys.exit(1)
            
        
    def Dump(Database):
        SysDBDump = logging.getLogger("SysDBDump	")
        
        SysDB.Retrieve()
        
        with open("Database.json", "w", encoding = "UTF-8") as f:
            json.dump(Database, f, indent = 4, ensure_ascii = False, sort_keys = False)
            SysDBDump.debug("The data has been successfully saved")
                
        