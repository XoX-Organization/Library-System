# Title : Library System
# Programmer : Xian Yee
# Version : 0.0.0

from functions import Store
from tabulate import tabulate
import os
import time
import platform

class FuncUtils:
    
    def __init__(self):
        self.Platform = platform.uname()[0]
        self.ASCII_ART = "\n\t╭╮╱╱╭━━┳━━╮╭━━━┳━━━┳━━━┳╮╱╱╭╮╱╱╱╱╱╱╱╱╭╮\n\t┃┃╱╱╰┫┣┫╭╮┃┃╭━╮┃╭━╮┃╭━╮┃╰╮╭╯┃╱╱╱╱╱╱╱╭╯╰╮\n\t┃┃╱╱╱┃┃┃╰╯╰┫╰━╯┃┃╱┃┃╰━╯┣╮╰╯╭┻━┳╮╱╭┳━┻╮╭╋━━┳╮╭╮\n\t┃┃╱╭╮┃┃┃╭━╮┃╭╮╭┫╰━╯┃╭╮╭╯╰╮╭┫━━┫┃╱┃┃━━┫┃┃┃━┫╰╯┃\n\t┃╰━╯┣┫┣┫╰━╯┃┃┃╰┫╭━╮┃┃┃╰╮╱┃┃┣━━┃╰━╯┣━━┃╰┫┃━┫┃┃┃\n\t╰━━━┻━━┻━━━┻╯╰━┻╯╱╰┻╯╰━╯╱╰╯╰━━┻━╮╭┻━━┻━┻━━┻┻┻╯\n\t╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╭━╯┃\n\t╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╰━━╯\n\n"

    def Cls(self):
        if self.Platform == 'Windows':
            os.system("cls")
            print(self.ASCII_ART)
        elif self.Platform in ('Darwin', 'Linux'):
            os.system("clear")
            print(self.ASCII_ART)


def main():
    
    while True:
        FuncUtils().Cls()
        print("Free to contribute on https://github.com/victoryy2003/Library-System\n")
        print("\t1. Create entry")
        print("\t2. Delete entry")
        print("\t3. List all entries")
        print("\t4. Search entry")
        
        print("\tQ. Quit program")
        

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
    