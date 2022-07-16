# Title : Library System
# Programmer : Xian Yee
# Version : 0.0.0

from functions import Store

ASCII_ART = "\n\t██╗░░░░░██╗██████╗░██████╗░░█████╗░██████╗░██╗░░░██╗  ░██████╗██╗░░░██╗░██████╗████████╗███████╗███╗░░░███╗\n\t██║░░░░░██║██╔══██╗██╔══██╗██╔══██╗██╔══██╗╚██╗░██╔╝  ██╔════╝╚██╗░██╔╝██╔════╝╚══██╔══╝██╔════╝████╗░████║\n\t██║░░░░░██║██████╦╝██████╔╝███████║██████╔╝░╚████╔╝░  ╚█████╗░░╚████╔╝░╚█████╗░░░░██║░░░█████╗░░██╔████╔██║\n\t██║░░░░░██║██╔══██╗██╔══██╗██╔══██║██╔══██╗░░╚██╔╝░░  ░╚═══██╗░░╚██╔╝░░░╚═══██╗░░░██║░░░██╔══╝░░██║╚██╔╝██║\n\t███████╗██║██████╦╝██║░░██║██║░░██║██║░░██║░░░██║░░░  ██████╔╝░░░██║░░░██████╔╝░░░██║░░░███████╗██║░╚═╝░██║\n\t╚══════╝╚═╝╚═════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░  ╚═════╝░░░░╚═╝░░░╚═════╝░░░░╚═╝░░░╚══════╝╚═╝░░░░░╚═╝\n\t"

print(ASCII_ART)
print("\t1. Create entry")
print("\t2. Delete entry\n")

Option = input("Choose an option: ")

if Option == "1":
    ID = input("Insert the book ID : ")
    BookTitle = input("Insert the book title : ")
    Author = input("Insert the author name : ")
    Subject = input("Insert the subject name : ")
    
    Store.Insert(ID, BookTitle, Author, Subject)

if Option == "2":
    ID = input("Insert the book ID : ")
    
    Store.Delete(ID)
