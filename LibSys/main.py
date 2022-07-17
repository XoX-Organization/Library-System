# Title : Library System
# Programmer : Xian Yee
# Version : 0.0.0

from functions import Store, Authentication
from tabulate import tabulate
from getpass import getpass
from distutils.util import strtobool
import os
import time
import platform

class FuncUtils:
    
    def __init__(self):
        self.Platform = platform.system()
        self.ASCII_ART = "\n\t╭╮╱╱╭━━┳━━╮╭━━━┳━━━┳━━━┳╮╱╱╭╮╱╱╱╱╱╱╱╱╭╮\n\t┃┃╱╱╰┫┣┫╭╮┃┃╭━╮┃╭━╮┃╭━╮┃╰╮╭╯┃╱╱╱╱╱╱╱╭╯╰╮\n\t┃┃╱╱╱┃┃┃╰╯╰┫╰━╯┃┃╱┃┃╰━╯┣╮╰╯╭┻━┳╮╱╭┳━┻╮╭╋━━┳╮╭╮\n\t┃┃╱╭╮┃┃┃╭━╮┃╭╮╭┫╰━╯┃╭╮╭╯╰╮╭┫━━┫┃╱┃┃━━┫┃┃┃━┫╰╯┃\n\t┃╰━╯┣┫┣┫╰━╯┃┃┃╰┫╭━╮┃┃┃╰╮╱┃┃┣━━┃╰━╯┣━━┃╰┫┃━┫┃┃┃\n\t╰━━━┻━━┻━━━┻╯╰━┻╯╱╰┻╯╰━╯╱╰╯╰━━┻━╮╭┻━━┻━┻━━┻┻┻╯\n\t╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╭━╯┃\n\t╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╰━━╯\n"

    def Cls(self, PrintUser = True):
        if self.Platform == 'Windows':
            os.system("cls")
            print(self.ASCII_ART)
            if PrintUser:
                print(f"\tLogged in as {Username}\n")
                
        elif self.Platform in ('Darwin', 'Linux'):
            os.system("clear")
            print(self.ASCII_ART)
            if PrintUser:
                print(f"\tLogged in as {Username}\n")


def main():
    
    while True:
        
        '''
        Section Login System:
        The user will be prompted for login credential before using this program.
        '''
        global Username
        
        FuncUtils().Cls(PrintUser = False)
        
        Username = input("Please enter your username: ")
        
        if Authentication.CheckExists(Username):
            print("Tip: If you can't see what password you entered, it's normal not bug :D\n")
            Password = getpass("Please enter your password: ")
            Auth = Authentication(Username, Password).Login()
            if Auth == True:
                pass
            elif Auth == False:
                input("You had entered an incorrect password. Please try again\nPress <Enter> to continue...")
                continue
            
        elif not Authentication.CheckExists(Username):
            
            try:
                RegConf = strtobool(input("The username is not exist, do you want to register?: (Y/N) "))
            except ValueError:
                continue
            
            if RegConf:
                print("Tip: If you can't see what password you entered, it's normal not bug :D\n")
                Password = getpass("Please make a password: ")
                Password2nd = getpass("Please confirm your password: ")
                
                if Password == Password2nd:
                    Authentication(Username, Password).Register()
                    print("You have successfully registered")
                    time.sleep(3)
                    
                elif Password != Password2nd:
                    input("The confirmation password not match the previous password\nPress <Enter> to continue...")
                    continue
                
            elif not RegConf:
                continue
                
                
                
        while True:
            
            '''
            Section Main
            '''
            
        
            FuncUtils().Cls()
            print("\tFree to contribute on https://github.com/victoryy2003/Library-System\n")
            print("\t1. Create entry")
            print("\t2. Delete entry")
            print("\t3. List all entries")
            print("\t4. Search entry")
            
            print("\tQ. Log Out")
            

            Option = input("\nChoose an option: ")

            if Option == "1":
                while True:
                    try:
                        FuncUtils().Cls()
                        print("Tips: Press <CTRL-C> to return to menu\n")
                        ID = input("Insert the book ID : ")
                        BookTitle = input("Insert the book title : ")
                        Author = input("Insert the author name : ")
                        Subject = input("Insert the subject name : ")
                        
                        Store.Insert(ID, BookTitle, Author, Subject)
                        time.sleep(4)
                        continue
                    
                    except KeyboardInterrupt:
                        break

            if Option == "2":
                while True:
                    try:
                        FuncUtils().Cls()
                        print("Tips: Press <CTRL-C> to return to menu\n")
                        ID = input("Insert the book ID : ")
                    
                        Store.Delete(ID)
                        time.sleep(4)
                        continue
                    
                    except KeyboardInterrupt:
                        break

            if Option == "3":
                while True:
                    FuncUtils().Cls()
                    List = Store.ListAll()
                    
                    print(tabulate(List, headers = "firstrow", tablefmt = "grid", showindex = True, missingval = "N/A"))
                    input("Press Enter to continue...")
                    break
                
            if Option == "4":
                while True:
                    FuncUtils().Cls()
                    ID = input("Insert the book ID : ")
                    BookTitle = input("Insert the book title : ")
                    Author = input("Insert the author name : ")
                    Subject = input("Insert the subject name : ")
                    
                    List = Store.Search(ID = ID, BookTitle = BookTitle, Author = Author, Subject = Subject)
                    print(tabulate(List, headers = "firstrow", tablefmt = "grid", showindex = True, missingval = "N/A"))
                    input("Press Enter to continue...")
                    break
                    
            if Option.upper() == "Q":
                break
                    
                
if __name__ == "__main__":
    main()
    