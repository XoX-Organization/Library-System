Library System
=================
Install
-------
To install Library System: (Requirement Python Version >= 3.6)
```bash
pip install "git+https://github.com/KimAssignment/Library-System@master"
```

To update Library System:
```bash
pip install "git+https://github.com/KimAssignment/Library-System@master" --upgrade
```
Usage
-----
To use the application, simply run the following command:
```bash
LibrarySystem
```

Usage as a library
-----
```bash

#### About Storing
from LibrarySystem.Storing import Storing

### Following functions requires to be initialized before use
Object = Storing("AB123")
# Initiate module Storing by assigning ID into it, and the result will be assigning to the variable which named "Object"

Object.valid_ID
# This will return True if the ID "AB123" is existing in database
Object.Register()
# This will register ID "AB123" if it is not existing
Object.Delete()
# This will delete ID "AB123" if it is in the database
Object.Modify(Key, Value)
# This will allow user to modify the values of the ID "AB123" by given key in database (The key has to be 70% match to the key in database)



### Those following functions doesn't requires initialization

Storing.Search(*keywords)
# This allow user to search for matching keywords in database
# For example, Storing.Search("AB", "ABB WEE ADW")
# Can provide more keywords as much as you want as long they separate with commas and in string form

Storing.List(ID = None, Only_Modifiable = False) 
# This will list out all items in database
# (if ID has been provided besides None, it will only show item with matching ID)
# (if Only_Modifiable sets to True, only values that cannot be modify will be hidden)




#### About Member
from LibrarySystem.Member import Member

### Following functions requires to be initialized before use
Object = Member("2200153")
# Initiate module Member by assigning ID into it, and the result will be assigning to the variable which named "Object"

Object.valid_ID
# This will return True if the ID "2200153" is existing in database
Object.Register()
# This will register ID "2200153" if it is not existing
Object.Delete()
# This will delete ID "2200153" if it is in the database
Object.Modify(Key, Value)
# This will allow user to modify the values of the ID "2200153" by given key in database (The key has to be 70% match to the key in database)



### Those following functions doesn't requires initialization

Member.Search(*keywords)
# This allow user to search for matching keywords in database
# For example, Member.Search("AB", "ABB WEE ADW")
# Can provide more keywords as much as you want as long they separate with commas and in string form

Member.List(ID = None, Only_Modifiable = False) 
# This will list out all items in database
# (if ID has been provided besides None, it will only show item with matching ID)
# (if Only_Modifiable sets to True, only values that cannot be modify will be hidden)




#### About Employee
from LibrarySystem.Employee import Employee

### Following functions requires to be initialized before use
Object = Employee("001")
# Initiate module Employee by assigning ID into it, and the result will be assigning to the variable which named "Object"

Object.valid_ID
# This will return True if the ID "001" is existing in database

Object.Register(password, hashed = True)
# This will register ID "001" if it is not existing
# (if hashed is True, the password will be BCrypted)
# (if hashed is False, the password will be registered in string form)

Object.Login(password)
# Employee have to login before using the system

Object.Delete()
# This will delete ID "001" if it is in the database

Object.Modify(Key, Value)
# This will allow user to modify the values of the ID "001" by given key in database (The key has to be 70% match to the key in database)



### Those following functions doesn't requires initialization

Employee.Search(*keywords)
# This allow user to search for matching keywords in database
# For example, Employee.Search("AB", "ABB WEE ADW")
# Can provide more keywords as much as you want as long they separate with commas and in string form

Employee.List(ID = None, Only_Modifiable = False) 
# This will list out all items in database
# (if ID has been provided besides None, it will only show item with matching ID)
# (if Only_Modifiable sets to True, only values that cannot be modify will be hidden)




#### About Logging

from LibrarySystem.Logging import get_logger, remove_handler, shutdown

logger = get_logger(LOGGER_NAME)
# Initialize first by getting a logger handler with replacing LOGGER_NAME variable with a name
# For example, logger = get_logger("System")

logger.info("This is a info")
logger.warning("This is a warning")
logger.error("This is a error")
logger.critical("This is a critical")
logger.debug("This is a debug")
# Those are level of logging, by specifying the level, the logger will filter them and write into a log file

logger = remove_handler(logger)
# While in a loop, the logger will keep adding handlers unlimitedly
# To prevent that issue, remove_handler should be call out every time after finish a loop

shutdown()
# This may be call out at the end of the script to shutdown all instances of logging

```