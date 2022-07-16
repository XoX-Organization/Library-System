# Title : Library System
# Programmer : Xian Yee
# Version : 0.0.0

import json


class Store:
    
    def __init__(self):
        pass
    
    def Insert(ID, BookTitle, Author, Subject):
        
        Database = SysDB.Retrieve()
        
        if ID not in Database.keys():
            Database[ID] = {
                "BookTitle": BookTitle,
                "Author": Author,
                "Subject": Subject
                            }
        
        if ID in Database.keys():
            raise Exception("The item exists already")
            
        SysDB.Dump(Database)
        
    def Delete(ID):
        
        Database = SysDB.Retrieve()
        
        if ID in Database.keys():
            Database.pop(ID)
            
        if ID not in Database.keys():
            raise Exception("The item does not exist")
            
        SysDB.Dump(Database)
        
class SysDB:
    
    def __init__(self):
        pass
    
    def Retrieve():
        
        try:
            with open("Database.json", "r", encoding = "UTF-8") as f :
                return json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            open("Database.json", "w+", encoding = "UTF-8")
            return {}
        
    def Dump(Database):
        
        try:
            with open("Database.json", "w", encoding = "UTF-8") as f:
                json.dump(Database, f, indent = 4, ensure_ascii = False, sort_keys = False)
        except FileNotFoundError:
            with open("Database.json", "w+", encoding = "UTF-8") as f:
                json.dump(Database, f, indent = 4, ensure_ascii = False, sort_keys = False)
        