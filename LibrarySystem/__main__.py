
# Title : Library System
# Programmer : Xian Yee
# Version : 0.1.3-a2


import os
import platform
import traceback

from datetime import datetime
from distutils.util import strtobool
from getpass import getpass
from tabulate import tabulate

from .Constants import *
from .Employee import Employee
from .Logging import get_logger, shutdown
from .Member import Member
from .Path import Path
from .Pick import pick
from .Storing import Storing


def cls(print_ctrl_c = False):
    os_name = platform.system()
    try:
        if os_name == 'Windows':
            os.system('cls')
            
        elif os_name in ('Darwin', 'Linux'):
            os.system('clear')
            
    finally:
        print(ASCII_ART)
        
        if print_ctrl_c == True:
            print('\tPress >CTRL+C< back to menu\n')
        


def _main():
    global LOGIN_USER
    
    while True:
        
        
        # ////////////////////////////////////////////////////////////
        #                       LOGIN SCREEN
        # ////////////////////////////////////////////////////////////
        
        
        cls()
        print(
            '\tPress >CTRL+C< to quit the program\n',
            f'\t{"-" * 50}',
            '\tThis Login screen will automatically bring you',
            '\tto register if you are first-time user',
            f'\t{"-" * 50}\n',
            sep = '\n'
        )
        
        LOGIN_USER = input('Login ID: ').upper()
        employee = Employee(LOGIN_USER)
        
        if employee.valid_ID:
            password = getpass('Password: ')
            
            if employee.Login(password) == False:
                input('Press >ENTER< to continue')
                continue
            
            
        elif not employee.valid_ID:
            cls()
            print(
                f'\t{"-" * 50}',
                f'\tWelcome to Library System, {LOGIN_USER}',
                f'\tSince you are first-time user, you will be prompted to register',
                f'\t{"-" * 50}',
                sep = '\n'
            )
            
            password = getpass('Password: ')
            password_again = getpass('Password (again): ')
            
            if password != password_again:
                print('\nBoth passwords unmatching, back to login screen')
                input('Press >ENTER< to continue')
                continue
                
            employee.Register(password, hashed = True)
        
        
        # ////////////////////////////////////////////////////////////
        #                       MAIN MENU
        # ////////////////////////////////////////////////////////////
        
        
        while True:
            cls()
            title = f'\t{"-" * 50}\n\tWelcome to Library System, {LOGIN_USER}\n\t{"-" * 50}'
            
            options = [
                '\tStorage managing',
                '\tMembership managing',
                '\tEmployee managing',
            ]
            
            try: option, index = pick(options, title, indicator = ' > ', print_ctrl_c = True)
            except KeyboardInterrupt: break
            
            
            # ////////////////////////////////////////////////////////////
            #                       COMMON FUNCTIONS
            # ////////////////////////////////////////////////////////////
            
            
            class Function:
                
                def __init__(self, System):
                    if System == 'Storing':
                        self.system = Storing
                    if System == 'Member':
                        self.system = Member
                    if System == 'Employee':
                        self.system = Employee
            
                def list(self):
                    cls(print_ctrl_c = True)
                    print('List all section')
                    list = self.system.List()
                    if list != False: print(tabulate(list, headers = 'firstrow', tablefmt = 'grid', showindex = True, missingval = 'N/A'))
                    input('Press >ENTER< to continue')
                    return False
                    
                def search(self):
                    cls(print_ctrl_c = True)
                    print('Search section')
                    keywords = input('Provide any keywords or phrases (separate with commas): ').upper().split(',')
                    list = self.system.Search(*keywords)
                    if list != False: print(tabulate(list, headers = 'firstrow', tablefmt = 'grid', showindex = True, missingval = 'N/A'))
                    input('Press >ENTER< to continue')
                    return False
                    
                def register(self):
                    cls(print_ctrl_c = True)
                    print('Register section')
                    id = input('ID: ').upper()
                    success = self.system(id).Register()
                    
                    if success != True:
                        input('Press >ENTER< to continue')
                        return True
                        
                    # After register success, now can be able to modify the values
                    while True:
                        try:
                            self.modify_main(id)
                        except KeyboardInterrupt:
                            break
                    
                    return True
                        
                def modify_main(self, id):
                    cls(print_ctrl_c = True)
                    print('Modify section')
                    list = self.system.List(ID = id, Only_Modifiable = True)
                    if list != False: print(tabulate(list, headers = 'firstrow', tablefmt = 'grid', missingval = 'N/A'))
                    key = input('Variable you wish to modify: ')
                    value = input('New value: ').upper()
                    self.system(id).Modify(key, value)
                    input('Press >ENTER< to continue')
                    
                def modify_head(self):
                    cls(print_ctrl_c = True)
                    print('Modify section')
                    id = input('ID: ').upper()
                    object = self.system(id)
                    
                    if object.valid_ID != True:
                        print('Invalid ID')
                        input('Press >ENTER< to continue')
                        return True
                        
                    while True:
                        try:
                            self.modify_main(id)
                        except KeyboardInterrupt:
                            break
                        
                    return False
                    
                def delete(self):
                    cls(print_ctrl_c = True)
                    print('Deletion section')
                    id = input('ID: ').upper()
                    object = self.system(id)
                    
                    if object.valid_ID != True:
                        print('Invalid ID')
                        input('Press >ENTER< to continue')
                        return True
                    
                    try: confirmation = strtobool(input(f'Are you sure you want to delete {id}? (y/N): '))
                    except ValueError: return True
                    
                    if confirmation == True:
                        object.Delete()
                        input('Press >ENTER< to continue')
                        return True
                    
                    else: return True
                
                
            # ////////////////////////////////////////////////////////////
            #                       STORING SYSTEM
            # ////////////////////////////////////////////////////////////
            
            
            if index == 0:
                
                def add_stock():
                    cls(print_ctrl_c = True)
                    print('Add Stock section')
                    print('The Stock ID will auto generate, just input the Book ID instead')
                    book_id = input('Book ID: ').upper()
                    print('Stock ID:', Storing(book_id).AddStock())
                    input('Press >Enter< to continue')
                    return True
                
                def delete_stock():
                    cls(print_ctrl_c = True)
                    print('Delete Stock section')
                    stock_id = input('Stock ID: ').upper()
                    Storing(stock_id).DeleteStock()
                    input('Press >Enter< to continue')
                    return True
                
                def sell_stock():
                    result = Storing.SellStock(LOGIN_USER, JustCheckPriceOnly = True)
                    while True:
                        cls(print_ctrl_c = True)
                        print('Sell Stock section')
                        print(tabulate(
                                result[0],
                                headers = 'firstrow',
                                tablefmt = 'grid',
                                missingval = 'N/A'
                                ),
                            f'SUBTOTAL: {result[2]}',
                            sep = '\n'
                            )
                        stock_id = input('\nType "CONFIRM" to confirm the purchase\nStock ID: ').upper()
                        
                        if stock_id != 'CONFIRM':
                            result[1].append(stock_id)
                            result = Storing.SellStock(LOGIN_USER, *result[1], JustCheckPriceOnly = True)
                            input('Press >Enter< to continue')
                            continue
                        
                        cls()
                        result = Storing.SellStock(LOGIN_USER, *result[1], JustCheckPriceOnly = False)
                        print(
                            '-----RECEIPT OF PURCHASE-----',
                            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            tabulate(
                                result[0],
                                headers = 'firstrow',
                                tablefmt = 'grid',
                                missingval = 'N/A'
                                ),
                            f'SUBTOTAL: {result[2]}',
                            '\nHave a nice day :)\n\n',
                            sep = '\n'
                            )
                            
                        input('Press >Enter< to continue')
                        return False
                
                
                while True:
                    
                    title = f'\t{"-" * 50}\n\tWelcome to Storing System, {LOGIN_USER}\n\t{"-" * 50}\n'
                    
                    options = [
                        '\tList',
                        '\tSearch',
                        '\tRegister',
                        '\tModify',
                        '\tDelete',
                        '\tAdd Stock',
                        '\tDelete Stock',
                        '\tSell Stock'
                    ]
                    
                    try: option, index = pick(options, title, indicator = ' > ', print_ctrl_c = True)
                    except KeyboardInterrupt: break
                    
                    list_functions = {
                        0: Function('Storing').list,
                        1: Function('Storing').search,
                        2: Function('Storing').register,
                        3: Function('Storing').modify_head,
                        4: Function('Storing').delete,
                        5: add_stock,
                        6: delete_stock,
                        7: sell_stock
                    }
                    
                    loop = True
                    while loop == True:
                        try:
                            loop = list_functions.get(index)()
                        except KeyboardInterrupt:
                            break
                    
                    
            # ////////////////////////////////////////////////////////////
            #                       MEMBER SYSTEM
            # ////////////////////////////////////////////////////////////
            
            
            if index == 1:
                
                def Borrow():
                    cls(print_ctrl_c = True)
                    print('Borrow section')
                    member_id = input('Member ID: ').upper()
                    
                    if Member(member_id).valid_ID != True:
                        print('Invalid Member ID')
                        input('Press >ENTER< to continue')
                        return True
                    
                    while True:
                        try:
                            cls(print_ctrl_c = True)
                            print(f'Member: {member_id}')
                            book_id = input('Book ID wish to borrow: ').upper()
                            Storing(book_id).LendStock(MemberID = member_id)
                            input('Press >Enter< to continue')
                        except KeyboardInterrupt: break
                    
                    return True
                
                def Return():
                    cls(print_ctrl_c = True)
                    print('Return section')
                    book_id = input('Book ID: ').upper()
                    
                    Storing(book_id).ReturnStock()
                    input('Press >ENTER< to continue')
                    return True
                
                def ListBorrowing():
                    cls(print_ctrl_c = True)
                    print('List member borrowing section')
                    member_id = input('Member ID: ').upper()
                    
                    member = Member(member_id)
                    if member.valid_ID != True:
                        print('Invalid Member ID')
                        input('Press >ENTER< to continue')
                        return True
                    
                    table = member.ListBorrowing()
                    print(tabulate(
                        table,
                        headers = 'firstrow',
                        tablefmt = 'grid',
                        missingval = 'N/A'
                    ))
                    input('Press >Enter< to continue')
                    return True
                
                while True:
                    
                    title = f'\t{"-" * 50}\n\tWelcome to Member System, {LOGIN_USER}\n\t{"-" * 50}\n'
                    
                    options = [
                        '\tList',
                        '\tSearch',
                        '\tRegister',
                        '\tModify',
                        '\tDelete',
                        '\tBorrow book',
                        '\tReturn book',
                        '\tList Borrowing (Include subtotal penalty)'
                    ]
                    
                    try: option, index = pick(options, title, indicator = ' > ', print_ctrl_c = True)
                    except KeyboardInterrupt: break
            
                    
                    list_functions = {
                        0: Function('Member').list,
                        1: Function('Member').search,
                        2: Function('Member').register,
                        3: Function('Member').modify_head,
                        4: Function('Member').delete,
                        5: Borrow,
                        6: Return,
                        7: ListBorrowing
                    }
                    
                    loop = True
                    while loop == True:
                        try:
                            loop = list_functions.get(index)()
                        except KeyboardInterrupt:
                            break
                    
                    
            # ////////////////////////////////////////////////////////////
            #                       EMPLOYEE SYSTEM
            # ////////////////////////////////////////////////////////////
            
            
            if index == 2:
                
                while True:
                    
                    title = f'\t{"-" * 50}\n\tWelcome to Employee System, {LOGIN_USER}\n\t{"-" * 50}\n'
                    
                    options = [
                        '\tList',
                        '\tSearch',
                        '\tModify',
                        '\tDelete'
                    ]
                    
                    try: option, index = pick(options, title, indicator = ' > ', print_ctrl_c = True)
                    except KeyboardInterrupt: break
                    
                    list_functions = {
                        0: Function('Employee').list,
                        1: Function('Employee').search,
                        2: Function('Employee').modify_head,
                        3: Function('Employee').delete
                    }
                    
                    loop = True
                    while loop == True:
                        try:
                            loop = list_functions.get(index)()
                        except KeyboardInterrupt:
                            break
        
        
    # ////////////////////////////////////////////////////////////
    #                       END OF PROGRAM
    # ////////////////////////////////////////////////////////////
    
    
    
    
def main():
    
    try:
    
        _main()
            
    except KeyboardInterrupt: cls()
    
    except Exception as e:
        cls()
        logger = get_logger('SystemError')
        logger.error(traceback.format_exc())
        print(
            '\n\nCheck the log file and fix the bugs before',
            'next launch to prevent any loss of data\n\n',
            sep = '\n'
        )
        
    finally:
        
        def get_version():
            import re
            
            SRC = os.path.abspath(os.path.dirname(__file__))
            PATH = os.path.join(SRC, '__init__.py')
            
            with open(PATH) as f:
                for line in f:
                    m = re.match("__version__ = '(.*)'", line)
                    if m:
                        return m.group(1)
        
        
        shutdown()
        try: print(f'\t\tVersion: {get_version()}')
        except: print(f'\t\tVersion: FAILED TO GET VERSION')
        print(
            '\n\n\tData has been saved in the following path:',
            f'\t{Path().user_data_roaming_dir}\n',
            '\n\tSources:',
            '\thttps://github.com/KimAssignment/Library-System/\n',
            '\n\tBugs and Feature Suggestions:',
            '\thttps://github.com/KimAssignment/Library-System/issues\n\n',
            sep = '\n'
        )
        
        input('\tPress >Enter< to exit\n\n')
    

if __name__ == '__main__':
    main()
    
