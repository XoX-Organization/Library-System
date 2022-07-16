# Title : Library System
# Programmer : Xian Yee
# Version : 0.0.0

from functions import Store
from tabulate import tabulate
import platform
import os


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
        print("\t1. Create entry")
        print("\t2. Delete entry")
        print("\t3. List all entries")

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
                    continue
                
                except KeyboardInterrupt:
                    break

        if Option == "3":
            while True:
                FuncUtils().Cls()
                List = Store.ListAll()
                List.insert(0, ["ID", "Book Title", "Author", "Subject"])
                
                print(tabulate(List, headers = "firstrow", tablefmt = "grid", showindex = True, missingval = "N/A"))
                input("Press Enter to continue...")
                break
                
                
if __name__ == "__main__":
    main()
    