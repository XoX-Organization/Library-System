
# Title : Library System
# Programmer : Xian Yee
# Version : 0.1.4-a1


import functools
import os
import platform
import traceback

from datetime import datetime
from distutils.util import strtobool
from getpass import getpass
from tabulate import tabulate

from .Constants import ASCII_ART
from .Employee import Employee
from .Logging import get_logger, shutdown
from .Member import Member
from .Path import Path
from .Pick import pick
from .Storing import Storing



def cls(
    print_ctrl_c: bool = False,
    print_ascii_art: bool = True
    ):
    os_name = platform.system()
    try:
        if os_name == 'Windows':
            os.system('cls')

        elif os_name in ('Darwin', 'Linux'):
            os.system('clear')

    finally:
        if print_ascii_art is True:
            print('\n', ASCII_ART)

        if print_ctrl_c is True:
            print('\tPress >CTRL+C< back to menu\n')



def _main(
    Flush,
    HashedPassword,
    MaximumBorrowAllowed,
    PenaltyLateReturn,
    PrintASCIIArt
):

    if Flush is True:
        global print
        print = functools.partial(print, flush = True)

    if PrintASCIIArt is False:
        global cls, pick
        cls = functools.partial(cls, print_ascii_art = PrintASCIIArt)
        pick = functools.partial(pick, print_ascii_art = PrintASCIIArt)


    # ////////////////////////////////////////////////////////////
    #                       LOGIN SCREEN
    # ////////////////////////////////////////////////////////////


    while True:

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
        if LOGIN_USER == "":
            input('Please enter a valid ID\nPress >ENTER< to continue')
            continue

        employee = Employee(LOGIN_USER)

        if employee.valid_ID:
            password = getpass('Password: ')

            if employee.Login(password) is False:
                input('Press >ENTER< to continue')
                continue


        elif not employee.valid_ID:
            cls()
            print(
                '\tPress >CTRL+C< to quit the program\n',
                f'\t{"-" * 50}',
                f'\tWelcome to Library System, {LOGIN_USER}',
                '\tSince you are first-time user, you will be prompted to register',
                f'\t{"-" * 50}',
                sep = '\n'
            )

            password = getpass('Password: ')
            password_again = getpass('Password (again): ')

            if password != password_again:
                print('\nBoth passwords unmatching, back to login screen')
                input('Press >ENTER< to continue')
                continue

            if HashedPassword is True:
                employee.Register(password, hashed = True)
            else:
                employee.Register(password)


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

            try:
                index = pick(
                    options,
                    title,
                    indicator = ' > ',
                    print_ctrl_c = True
                )[1]

            except KeyboardInterrupt: break


            # ////////////////////////////////////////////////////////////
            #                       COMMON FUNCTIONS
            # ////////////////////////////////////////////////////////////


            class Function:

                def __init__(self, SystemType):
                    if SystemType == 'Storing':
                        self.system = Storing
                    if SystemType == 'Member':
                        self.system = Member
                    if SystemType == 'Employee':
                        self.system = Employee

                def ListAll(self):

                    cls(print_ctrl_c = True)
                    print('List all section')

                    response = self.system.List()

                    if response is not False:
                        print(tabulate(
                            response,
                            headers = 'firstrow',
                            tablefmt = 'grid',
                            showindex = True,
                            missingval = 'N/A'
                            ))

                    input('Press >ENTER< to continue')
                    return False # Return to main menu

                def Search(self):

                    cls(print_ctrl_c = True)
                    print('Search section')

                    keywords = input('Provide any keywords or phrases (separate with commas): ').upper().split(',')
                    response = self.system.Search(*keywords)

                    if response is not False:
                        print(tabulate(
                            response,
                            headers = 'firstrow',
                            tablefmt = 'grid',
                            showindex = True,
                            missingval = 'N/A'
                            ))

                    input('Press >ENTER< to continue')
                    return False # Return to main menu

                def _ModifyMain(self, ItemID):

                    cls(print_ctrl_c = True)
                    print('Modify section')

                    response = self.system.List(ID = ItemID, Only_Modifiable = True)

                    if response is not False:
                        print(tabulate(
                            response,
                            headers = 'firstrow',
                            tablefmt = 'grid',
                            showindex = True,
                            missingval = 'N/A'
                            ))

                    key = input('Variable you wish to modify: ')
                    value = input('New value: ').upper()
                    self.system(ItemID).Modify(key, value)

                    input('Press >ENTER< to continue')

                def Register(self):

                    cls(print_ctrl_c = True)
                    print('Register section')

                    item_id = input('Item ID: ').upper()
                    success = self.system(item_id).Register()

                    if success is not True:
                        input('Press >ENTER< to continue')
                        return True # Keep looping

                    # After register success, now can be able to modify the values
                    while True:
                        try:
                            self._ModifyMain(item_id)
                        except KeyboardInterrupt:
                            return True # Keep looping


                def Modify(self):

                    cls(print_ctrl_c = True)
                    print('Modify section')

                    item_id = input('Item ID: ').upper()
                    item = self.system(item_id)

                    if item.valid_ID is not True:
                        print('Invalid ID')
                        input('Press >ENTER< to continue')
                        return True # Keep looping

                    while True:
                        try:
                            self._ModifyMain(item_id)
                        except KeyboardInterrupt:
                            break

                    return False # Return to main menu

                def Delete(self):

                    cls(print_ctrl_c = True)
                    print('Deletion section')

                    item_id = input('Item ID: ').upper()
                    item = self.system(item_id)

                    if item.valid_ID is not True:
                        print('Invalid ID')
                        input('Press >ENTER< to continue')
                        return True # Keep looping

                    try:
                        confirmation = strtobool(
                            input(f'Are you sure you want to delete {item_id}? (y/N): ')
                            )
                    except ValueError:
                        return True # Keep looping

                    if bool(confirmation) is True:
                        item.Delete()
                        input('Press >ENTER< to continue')
                        return True # Keep looping

                    else: return True # Keep looping


            # ////////////////////////////////////////////////////////////
            #                       STORING SYSTEM
            # ////////////////////////////////////////////////////////////


            if index == 0:
                index = 0

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
                                showindex = True,
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
                                showindex = True,
                                missingval = 'N/A'
                                ),
                            f'SUBTOTAL: {result[2]}',
                            '\nHave a nice day :)\n\n',
                            sep = '\n'
                            )

                        input('Press >Enter< to continue')
                        return False


                while True:

                    title = f'\t{"-" * 50}\n\tWelcome to Storing System, {LOGIN_USER}\n\t{"-" * 50}'

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

                    try:
                        index = pick(
                                options,
                                title,
                                indicator = ' > ',
                                default_index = index,
                                print_ctrl_c = True
                                )[1]

                    except KeyboardInterrupt: break

                    list_functions = {
                        0: Function('Storing').ListAll,
                        1: Function('Storing').Search,
                        2: Function('Storing').Register,
                        3: Function('Storing').Modify,
                        4: Function('Storing').Delete,
                        5: add_stock,
                        6: delete_stock,
                        7: sell_stock
                    }

                    loop = True
                    while loop is True:
                        try:
                            loop = list_functions.get(index)()
                        except KeyboardInterrupt:
                            break


            # ////////////////////////////////////////////////////////////
            #                       MEMBER SYSTEM
            # ////////////////////////////////////////////////////////////


            if index == 1:
                index = 0

                def Borrow():
                    cls(print_ctrl_c = True)
                    print('Borrow section')
                    member_id = input('Member ID: ').upper()

                    if Member(member_id).valid_ID is not True:
                        print('Invalid Member ID')
                        input('Press >ENTER< to continue')
                        return True

                    while True:
                        try:
                            cls(print_ctrl_c = True)
                            print(f'Member: {member_id}')
                            book_id = input('Book ID wish to borrow: ').upper()
                            Storing(book_id).LendStock(MaximumBorrowAllowed, MemberID = member_id)
                            input('Press >Enter< to continue')
                        except KeyboardInterrupt: break

                    return True

                def Return():
                    cls(print_ctrl_c = True)
                    print('Return section')
                    book_id = input('Book ID: ').upper()

                    Storing(book_id).ReturnStock(PenaltyLateReturn = PenaltyLateReturn)
                    input('Press >ENTER< to continue')
                    return True

                def ListBorrowing():
                    cls(print_ctrl_c = True)
                    print('List member borrowing section')
                    member_id = input('Member ID: ').upper()

                    member = Member(member_id)
                    if member.valid_ID is not True:
                        print('Invalid Member ID')
                        input('Press >ENTER< to continue')
                        return True

                    table = member.ListBorrowing(PenaltyLateReturn = PenaltyLateReturn)
                    print(tabulate(
                        table,
                        headers = 'firstrow',
                        tablefmt = 'grid',
                        showindex = True,
                        missingval = 'N/A'
                        ))
                    input('Press >Enter< to continue')
                    return True

                while True:

                    title = f'\t{"-" * 50}\n\tWelcome to Member System, {LOGIN_USER}\n\t{"-" * 50}'

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

                    try:
                        index = pick(
                                options,
                                title,
                                indicator = ' > ',
                                default_index = index,
                                print_ctrl_c = True
                                )[1]

                    except KeyboardInterrupt: break


                    list_functions = {
                        0: Function('Member').ListAll,
                        1: Function('Member').Search,
                        2: Function('Member').Register,
                        3: Function('Member').Modify,
                        4: Function('Member').Delete,
                        5: Borrow,
                        6: Return,
                        7: ListBorrowing
                    }

                    loop = True
                    while loop is True:
                        try:
                            loop = list_functions.get(index)()
                        except KeyboardInterrupt:
                            break


            # ////////////////////////////////////////////////////////////
            #                       EMPLOYEE SYSTEM
            # ////////////////////////////////////////////////////////////


            if index == 2:
                index = 0

                while True:

                    title = f'\t{"-" * 50}\n\tWelcome to Employee System, {LOGIN_USER}\n\t{"-" * 50}'

                    options = [
                        '\tList',
                        '\tSearch',
                        '\tModify',
                        '\tDelete'
                    ]

                    try:
                        index = pick(
                                options,
                                title,
                                indicator = ' > ',
                                default_index = index,
                                print_ctrl_c = True,
                                )[1]

                    except KeyboardInterrupt: break

                    list_functions = {
                        0: Function('Employee').ListAll,
                        1: Function('Employee').Search,
                        2: Function('Employee').Modify,
                        3: Function('Employee').Delete
                    }

                    loop = True
                    while loop is True:
                        try:
                            loop = list_functions.get(index)()
                        except KeyboardInterrupt:
                            break


    # ////////////////////////////////////////////////////////////
    #                       END OF PROGRAM
    # ////////////////////////////////////////////////////////////




def main(
    Flush: bool = True,
    HashedPassword: bool = True,
    MaximumBorrowAllowed: int = 5,
    PenaltyLateReturn: float = 0.5,
    PrintASCIIArt: bool = True
):

    try:

        return _main(
            Flush,
            HashedPassword,
            MaximumBorrowAllowed,
            PenaltyLateReturn,
            PrintASCIIArt
        )

    except KeyboardInterrupt: cls()

    except Exception:
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

            with open(PATH, encoding = 'UTF-8') as f:
                for line in f:
                    m = re.match("__version__ = '(.*)'", line)
                    if m:
                        return m.group(1)


        shutdown()
        try: print(f'\t\tVersion: {get_version()}')
        except: print('\t\tVersion: FAILED TO GET VERSION')
        print(
            '\n\n\tData has been saved in the following path:',
            f'\t{Path().user_data_roaming_dir}\n',
            '\n\tSources:',
            '\thttps://github.com/KimAssignment/Library-System/\n',
            '\n\tBugs and Feature Suggestions:',
            '\thttps://github.com/KimAssignment/Library-System/issues\n\n',
            sep = '\n'
        )

        try: input('\tPress >Enter< to exit\n\n')
        except KeyboardInterrupt: pass


if __name__ == '__main__':
    main()

