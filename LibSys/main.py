# Title : Library System
# Programmer : Xian Yee
# Version : 0.0.0

from LibSys.functions import Store, Authentication, Member
from tabulate import tabulate
from getpass import getpass
from distutils.util import strtobool
import os
import time
import platform


def cls(print_login = True):
    os_name = platform.system()
    ascii_art = "\n\t╭╮╱╱╭━━┳━━╮╭━━━┳━━━┳━━━┳╮╱╱╭╮╱╱╱╱╱╱╱╱╭╮\n\t┃┃╱╱╰┫┣┫╭╮┃┃╭━╮┃╭━╮┃╭━╮┃╰╮╭╯┃╱╱╱╱╱╱╱╭╯╰╮\n\t┃┃╱╱╱┃┃┃╰╯╰┫╰━╯┃┃╱┃┃╰━╯┣╮╰╯╭┻━┳╮╱╭┳━┻╮╭╋━━┳╮╭╮\n\t┃┃╱╭╮┃┃┃╭━╮┃╭╮╭┫╰━╯┃╭╮╭╯╰╮╭┫━━┫┃╱┃┃━━┫┃┃┃━┫╰╯┃\n\t┃╰━╯┣┫┣┫╰━╯┃┃┃╰┫╭━╮┃┃┃╰╮╱┃┃┣━━┃╰━╯┣━━┃╰┫┃━┫┃┃┃\n\t╰━━━┻━━┻━━━┻╯╰━┻╯╱╰┻╯╰━╯╱╰╯╰━━┻━╮╭┻━━┻━┻━━┻┻┻╯\n\t╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╭━╯┃\n\t╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╰━━╯\n"
    if os_name == 'Windows':
        os.system("cls")
        print(ascii_art)
        if print_login:
            print(f"\tLogged in as {username}\n")
            
    elif os_name in ('Darwin', 'Linux'):
        os.system("clear")
        print(ascii_art)
        if print_login:
            print(f"\tLogged in as {username}\n")


def main():
    
    while True:
        
        global username
        
        cls(print_login = False)
        
        username = input("Please enter your username: ")
        
        if Authentication.check_user(username):
            print("Tip: If you can't see what password you entered, it's normal not bug :D\n")
            password = getpass("Please enter your password: ")
            auth_pass = Authentication(username, password).Login()
            if auth_pass == True:
                pass
            elif auth_pass == False:
                input("You had entered an incorrect password. Please try again\nPress <Enter> to continue...")
                continue
            
        elif not Authentication.check_user(username):
            
            try:
                register_confirmation = strtobool(input("The username is not exist, do you want to register?: (Y/N) "))
            except ValueError:
                continue
            
            if register_confirmation:
                print("Tip: If you can't see what password you entered, it's normal not bug :D\n")
                password = getpass("Please make a password: ")
                password2nd = getpass("Please confirm your password: ")
                
                if password == password_confirmation:
                    Authentication(username, password).Register()
                    print("You have successfully registered")
                    time.sleep(3)
                    
                elif password != password_confirmation:
                    input("The confirmation password not match the previous password\nPress <Enter> to continue...")
                    continue
                
            elif not register_confirmation:
                continue
                
                
                
        while True:
            
            cls()
            print("\tFree to contribute on https://github.com/KimAssignment/Library-System\n")
            
            print("\t1. Store System")
            print("\t2. Member System")
            
            print("\n\tQ. Log Out")
            option = input("\nChoose an option: ")

            if option == "1":
                while True:
                    
                    cls()
                    print("\t1. Create entry")
                    print("\t2. Delete entry")
                    print("\t3. List all entries")
                    print("\t4. Search entry")
                    
                    print("\n\tQ. Back to Main Menu")
                    

                    option = input("\nChoose an option: ")

                    if option == "1":
                        while True:
                            try:
                                cls()
                                print("Tip: Press <CTRL-C> to return to menu\n")
                                id = input("Insert the book ID : ")
                                book_title = input("Insert the book title : ")
                                author_name = input("Insert the author name : ")
                                subject_title = input("Insert the subject name : ")
                                
                                Store(id).Insert(book_title, author_name, subject_title)
                                input("Press <Enter> to continue...")
                                continue
                            
                            except KeyboardInterrupt:
                                break

                    if option == "2":
                        while True:
                            try:
                                cls()
                                print("Tip: Press <CTRL-C> to return to menu\n")
                                id = input("Insert the book ID : ")
                            
                                Store(id).Delete()
                                input("Press <Enter> to continue...")
                                continue
                            
                            except KeyboardInterrupt:
                                break

                    if option == "3":
                        while True:
                            cls()
                            list = Store.ListAll()
                            
                            print(tabulate(list, headers = "firstrow", tablefmt = "grid", showindex = True, missingval = "N/A"))
                            input("Press <Enter> to continue...")
                            break
                        
                    if option == "4":
                        while True:
                            cls()
                            keywords = input("Provide any keyword: (Can be separated by commas) ").split(",")
                            
                            list = Store.Search(*keywords)
                            print(tabulate(list, headers = "firstrow", tablefmt = "grid", showindex = True, missingval = "N/A"))
                            input("Press <Enter> to continue...")
                            break
                            
                    if option.upper() == "Q":
                        break
                    
            if option == "2":
                while True:
                    cls()
                    print("\t1. Create Member entry")
                    print("\t2. Modify Member entry")
                    print("\t3. Read Member info")
            
                    print("\n\tQ. Back to Main Menu")
                    option = input("\nChoose an option: ")
                    
                    if option == "1":
                        cls()
                        id = input("Insert the member ID: ")
                        Member(id).Create()
                        input('\nThe member has been created, Please goto "Modify Member" section for further adjustment.\nPress <Enter> to continue...')
                        
                    if option == "2":
                        try:
                            cls()
                            print("Tip: Press <CTRL-C> to return to menu\n")
                            id = input("Insert the member ID: ")
                            InitMember = Member(id)
                            while True:
                                cls()
                                list = InitMember.Read()
                                
                                p = 0
                                for i in range(len(list)):
                                    i = i - p
                                    if list[i][0] in ("Creation-Date", "Entitlement"):
                                        list.pop(i)
                                        p = p + 1
                                
                                print(tabulate(list, headers = "firstrow", tablefmt = "grid", showindex = True, missingval = "N/A"))
                                key = input("Enter the variable you wish to edit: ")
                                value = input("Enter the new value: ")
                                InitMember.Modify(key, value)
                                
                        except KeyboardInterrupt:
                            break
                        
                    if option == "3":
                        cls()
                        id = input("Insert the member ID: ")
                        list = Member(id).Read()
                        print(tabulate(list, headers = "firstrow", tablefmt = "grid", showindex = True, missingval = "N/A"))
                        input("Press <Enter> to continue...")
                    
            if option.upper() == "Q":
                break
                        
                
if __name__ == "__main__":
    main()
    