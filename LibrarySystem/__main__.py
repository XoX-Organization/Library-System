
# Title : Library System
# Programmer : Xian Yee
# Version : 0.1.0-a2


import os
import platform
import traceback

from tabulate import tabulate
from getpass import getpass
from distutils.util import strtobool

from LibrarySystem.Storing import Storing
from LibrarySystem.Member import Member
from LibrarySystem.Employee import Employee
from LibrarySystem.Lender import Lender
from LibrarySystem.Logging import get_logger, shutdown
from LibrarySystem.Path import Path


def cls(Print_CTRL_C = False):
    os_name = platform.system()
    ascii_art = "\n\t╭╮╱╱╭━━┳━━╮╭━━━┳━━━┳━━━┳╮╱╱╭╮╱╱╱╱╱╱╱╱╭╮\n\t┃┃╱╱╰┫┣┫╭╮┃┃╭━╮┃╭━╮┃╭━╮┃╰╮╭╯┃╱╱╱╱╱╱╱╭╯╰╮\n\t┃┃╱╱╱┃┃┃╰╯╰┫╰━╯┃┃╱┃┃╰━╯┣╮╰╯╭┻━┳╮╱╭┳━┻╮╭╋━━┳╮╭╮\n\t┃┃╱╭╮┃┃┃╭━╮┃╭╮╭┫╰━╯┃╭╮╭╯╰╮╭┫━━┫┃╱┃┃━━┫┃┃┃━┫╰╯┃\n\t┃╰━╯┣┫┣┫╰━╯┃┃┃╰┫╭━╮┃┃┃╰╮╱┃┃┣━━┃╰━╯┣━━┃╰┫┃━┫┃┃┃\n\t╰━━━┻━━┻━━━┻╯╰━┻╯╱╰┻╯╰━╯╱╰╯╰━━┻━╮╭┻━━┻━┻━━┻┻┻╯\n\t╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╭━╯┃\n\t╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╰━━╯\n"
    try:
        if os_name == 'Windows':
            os.system("cls")
            
        elif os_name in ('Darwin', 'Linux'):
            os.system("clear")
            
    finally:
        print(ascii_art)
        
        if Print_CTRL_C == True:
            print("\tPress >CTRL+C< back to menu\n")
        


def main():
    try:
        global LOGIN_USER
        
        while True:
            
            
            # ////////////////////////////////////////////////////////////
            #                       LOGIN SCREEN
            # ////////////////////////////////////////////////////////////
            
            cls()
            print("\tPress >CTRL+C< to quit the program\n")
            print("\t---------------------------------------------------")
            print("\tThis Login screen will automatically bring you")
            print("\tto register if you are first-time user")
            print("\t---------------------------------------------------\n")
            LOGIN_USER = input("Login ID: ")
            employee = Employee(LOGIN_USER)
            
            if employee.valid_ID:
                password = getpass("Password: ")
                
                if employee.Login(password) == False:
                    input("Press >ENTER< to continue")
                    continue
                
                
            elif not employee.valid_ID:
                print("\n///////////////////////////////////////////////////")
                print("BRINGING YOU TO REGISTER AS YOU ARE FIRST TIME USER")
                print("///////////////////////////////////////////////////\n")
                password = getpass("Password: ")
                password_again = getpass("Password (again): ")
                
                if password != password_again:
                    print("\nBoth passwords unmatching, back to login screen")
                    input("Press >ENTER< to continue")
                    continue
                    
                employee.Register(password, hashed = True)
            
            
            
            # ////////////////////////////////////////////////////////////
            #                       MAIN MENU
            # ////////////////////////////////////////////////////////////
            
            while True:
                cls()
                print("\t---------------------------------------------------")
                print(f"\tWelcome to Library System, {LOGIN_USER}")
                print("\tPress >Q< to log out")
                print("\t---------------------------------------------------")
                
                print("\t1. Storing Library Books? (Storage managing)")
                print("\t2. Or managing Library Members? (Membership managing)")
                print("\t3. Here to editing employee details (Employee editing)")
                option = input("\n\nChoose an option: ").upper()
                
                if option == "Q":
                    break
                
                
                # ////////////////////////////////////////////////////////////
                #                       COMMON FUNCTIONS
                # ////////////////////////////////////////////////////////////
                
                
                class Function:
                    
                    def __init__(self, System):
                        if System == "Storing":
                            self.system = Storing
                        if System == "Member":
                            self.system = Member
                        if System == "Employee":
                            self.system = Employee
                
                    def list(self):
                        cls(Print_CTRL_C = True)
                        print("List all section")
                        list = self.system.List()
                        if list != False: print(tabulate(list, headers = "firstrow", tablefmt = "grid", showindex = True, missingval = "N/A"))
                        input("Press >ENTER< to continue")
                        return False
                        
                    def search(self):
                        cls(Print_CTRL_C = True)
                        print("Search section")
                        keywords = input("Provide any keywords or phrases (separate with commas): ").split(",")
                        list = self.system.Search(*keywords)
                        if list != False: print(tabulate(list, headers = "firstrow", tablefmt = "grid", showindex = True, missingval = "N/A"))
                        input("Press >ENTER< to continue")
                        return False
                        
                    def register(self):
                        cls(Print_CTRL_C = True)
                        print("Register section")
                        id = input("ID: ")
                        success = self.system(id).Register()
                        
                        if success != True:
                            input("Press >ENTER< to continue")
                            return True
                            
                        # After register success, now can be able to modify the values
                        while True:
                            try:
                                self.modify_main(id)
                            except KeyboardInterrupt:
                                break
                        
                        return True
                            
                    def modify_main(self, id):
                        cls(Print_CTRL_C = True)
                        print("Modify section")
                        list = self.system.List(ID = id, Only_Modifiable = True)
                        if list != False: print(tabulate(list, headers = "firstrow", tablefmt = "grid", missingval = "N/A"))
                        key = input("Variable you wish to modify: ")
                        value = input("New value: ")
                        self.system(id).Modify(key, value)
                        input("Press >ENTER< to continue")
                        
                    def modify_head(self):
                        cls(Print_CTRL_C = True)
                        print("Modify section")
                        id = input("ID: ")
                        object = self.system(id)
                        
                        if object.valid_ID != True:
                            print("Invalid ID")
                            input("Press >ENTER< to continue")
                            return True
                            
                        while True:
                            try:
                                self.modify_main(id)
                            except KeyboardInterrupt:
                                break
                            
                        return False
                        
                    def delete(self):
                        cls(Print_CTRL_C = True)
                        print("Deletion section")
                        id = input("ID: ")
                        object = self.system(id)
                        
                        if object.valid_ID != True:
                            print("Invalid ID")
                            input("Press >ENTER< to continue")
                            return True
                        
                        try: confirmation = strtobool(input(f"Are you sure you want to delete {id}? (y/N): "))
                        except ValueError: return True
                        
                        if confirmation == True:
                            object.Delete()
                            input("Press >ENTER< to continue")
                            return True
                        
                        else: return True
                    
                    
                # ////////////////////////////////////////////////////////////
                #                       STORING SYSTEM
                # ////////////////////////////////////////////////////////////
                
                
                if option == "1":
                    
                    while True:
                        cls()
                        print("\t---------------------------------------------------")
                        print(f"\tWelcome to Storing System, {LOGIN_USER}")
                        print("\tPress >Q< back to main menu")
                        print("\t---------------------------------------------------\n")
                        
                        print("\t1. List")
                        print("\t2. Search")
                        print("\t3. Register")
                        print("\t4. Modify")
                        print("\t5. Delete")
                        option_storing = input("\n\nChoose an option: ").upper()
                        if option_storing == "Q": break
                        
                        storing_options = {
                            "1": Function("Storing").list,
                            "2": Function("Storing").search,
                            "3": Function("Storing").register,
                            "4": Function("Storing").modify_head,
                            "5": Function("Storing").delete
                        }
                        
                        loop = True
                        while loop == True:
                            try:
                                loop = storing_options.get(option_storing, lambda: input("Please select a valid option\nPress >Enter< to continue"))()
                            except KeyboardInterrupt:
                                break
                        
                        
                # ////////////////////////////////////////////////////////////
                #                       MEMBER SYSTEM
                # ////////////////////////////////////////////////////////////
                
                if option == "2":
                    
                    def Borrow():
                        cls(Print_CTRL_C = True)
                        print("Borrow section")
                        id = input("ID: ")
                        object = Lender(id)
                        
                        if object.valid_ID != True:
                            print("Invalid ID")
                            input("Press >ENTER< to continue")
                            return True
                        
                        while True:
                            try:
                                cls(Print_CTRL_C = True)
                                print(f"Member: {id}")
                                book_id = input("Book ID wish to borrow: ")
                                object.Borrow(book_id)
                                input("Press >Enter< to continue")
                            except KeyboardInterrupt: break
                        
                        return True
                    
                    def Return():
                        cls(Print_CTRL_C = True)
                        print("Return section")
                        id = input("ID: ")
                        object = Lender(id)
                        
                        if object.valid_ID != True:
                            print("Invalid ID")
                            input("Press >ENTER< to continue")
                            return True
                        
                        while True:
                            try:
                                cls(Print_CTRL_C = True)
                                print(f"Member: {id}")
                                book_id = input("Book ID wish to return: ")
                                object.Return(book_id)
                                input("Press >Enter< to continue")
                            except KeyboardInterrupt: break
                        
                        return True
                    
                    while True:
                        cls()
                        print("\t---------------------------------------------------")
                        print(f"\tWelcome to Member System, {LOGIN_USER}")
                        print("\tPress >Q< back to main menu")
                        print("\t---------------------------------------------------\n")
                        
                        print("\t1. List")
                        print("\t2. Search")
                        print("\t3. Register")
                        print("\t4. Modify")
                        print("\t5. Delete")
                        print("\t6. Borrow book")
                        print("\t7. Return book")
                        option_member = input("\n\nChoose an option: ").upper()
                        if option_member == "Q": break
                        
                        member_options = {
                            "1": Function("Member").list,
                            "2": Function("Member").search,
                            "3": Function("Member").register,
                            "4": Function("Member").modify_head,
                            "5": Function("Member").delete,
                            "6": Borrow,
                            "7": Return
                        }
                        
                        loop = True
                        while loop == True:
                            try:
                                loop = member_options.get(option_member, lambda: input("Please select a valid option\nPress >Enter< to continue"))()
                            except KeyboardInterrupt:
                                break
                        
                        
                        
                # ////////////////////////////////////////////////////////////
                #                       EMPLOYEE SYSTEM
                # ////////////////////////////////////////////////////////////
                
                if option == "3":
                    
                    while True:
                        cls()
                        print("\t---------------------------------------------------")
                        print(f"\tWelcome to Employee System, {LOGIN_USER}")
                        print("\tPress >Q< back to main menu")
                        print("\t---------------------------------------------------\n")
                        
                        print("\t1. List")
                        print("\t2. Search")
                        print("\t3. Modify")
                        print("\t4. Delete")
                        option_employee = input("\n\nChoose an option: ").upper()
                        if option_employee == "Q": break
                        
                        employee_options = {
                            "1": Function("Employee").list,
                            "2": Function("Employee").search,
                            "3": Function("Employee").modify_head,
                            "4": Function("Employee").delete
                        }
                        
                        loop = True
                        while loop == True:
                            try:
                                loop = employee_options.get(option_employee, lambda: input("Please select a valid option\nPress >Enter< to continue"))()
                            except KeyboardInterrupt:
                                break
        
        
    # ////////////////////////////////////////////////////////////
    #                       END OF PROGRAM
    # ////////////////////////////////////////////////////////////
        
    except Exception as e:
        cls()
        logger = get_logger("SystemError")
        logger.error(traceback.format_exc())
        
    except KeyboardInterrupt: cls()
        
    finally:
        
        import re
        SRC = os.path.abspath(os.path.dirname(__file__))
        if os.path.exists(os.path.join(SRC, 'LibrarySystem/__init__.py')):
            path = os.path.join(SRC, 'LibrarySystem/__init__.py')
        else: path = os.path.join(SRC, '__init__.py')
        def get_version():
            with open(path) as f:
                for line in f:
                    m = re.match("__version__ = '(.*)'", line)
                    if m:
                        return m.group(1)
        
        
        shutdown()
        print(f"\t\tVersion: {get_version()}")
        print("\n\n\tData has been saved in the following path:")
        print(f"\t{Path().user_data_roaming_dir}\n")
        print("\n\tSources:")
        print("\thttps://github.com/KimAssignment/Library-System/\n")
        print("\n\tBugs and Feature Suggestions:")
        print("\thttps://github.com/KimAssignment/Library-System/issues\n\n")
        input("\tPress >Enter< to continue")
        
        
        
        
        
        
        
if __name__ == "__main__":
    main()
    
