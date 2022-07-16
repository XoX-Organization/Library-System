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
        
        elif ID in Database.keys():
            raise Exception("The item exists already")
            
        SysDB.Dump(Database)
        
    def Delete(ID):
        
        Database = SysDB.Retrieve()
        
        if ID in Database.keys():
            Database.pop(ID)
            
        elif ID not in Database.keys():
            raise Exception("The item does not exist")
            
        SysDB.Dump(Database)
        
    def ListAll():
        
        Database = SysDB.Retrieve()
        List = [["ID", "Book Title", "Author", "Subject"]]
        
        if Database.keys():
            for ID in Database:
                List.append([ID, Database[ID]["BookTitle"], Database[ID]["Author"], Database[ID]["Subject"]])
                
            return List
        
    def Search(ID = None, BookTitle = None, Author = None, Subject = None):
        
        Database = SysDB.Retrieve()
        List = [["ID", "Book Title", "Author", "Subject"]]
        
        if ID != None:
            for DBID in Database.keys():
                if ID == DBID:
                    List.append([DBID, Database[DBID]["BookTitle"], Database[DBID]["Author"], Database[DBID]["Subject"]])
                    
        if (BookTitle != None) or (Author != None) or (Subject != None):
            for DBID in Database.keys():
                if BookTitle == Database[DBID]["BookTitle"]:
                    List.append([DBID, Database[DBID]["BookTitle"], Database[DBID]["Author"], Database[DBID]["Subject"]])
                    
                if Author == Database[DBID]["Author"]:
                    List.append([DBID, Database[DBID]["BookTitle"], Database[DBID]["Author"], Database[DBID]["Subject"]])
                    
                if Subject == Database[DBID]["Subject"]:
                    List.append([DBID, Database[DBID]["BookTitle"], Database[DBID]["Author"], Database[DBID]["Subject"]])
                    
        return List
                    
        
     
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
        