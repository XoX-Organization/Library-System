
from datetime import datetime, timedelta
from typing import Optional

from .Common_Methods import Common
from .Database import DB_Member
from .Logging import get_logger, remove_handler

class Member:

    def __init__(self, ID):
        self.ID = ID

    @property
    def database(self):
        try: self._database
        except AttributeError: self._database = DB_Member.Retrieve()
        return self._database

    @staticmethod
    def List(
        ID: Optional[str] = None,
        Only_Modifiable: bool = False
        ):

        LOGGER_NAME = 'Member.List'
        DATATYPE = 'DB_Member'

        Method = Common(LOGGER_NAME, DATATYPE)
        return Method.List(ID = ID, Only_Modifiable = Only_Modifiable)

    @staticmethod
    def Search(*keywords):
        LOGGER_NAME = 'Member.Search'
        DATATYPE = 'DB_Member'

        Method = Common(LOGGER_NAME, DATATYPE)
        return Method.Search(*keywords)

    @property
    def valid_ID(self):
        valid_logger = get_logger('Member.valid_ID')

        if self.ID not in self.database:
            valid_logger = remove_handler(valid_logger)
            return False

        if self.database[self.ID]['Membership-Status'].upper() in ['BARRED', 'DEACTIVATED']:
            status = self.database[self.ID]['Membership-Status']
            valid_logger.info('Member %s has been %s', self.ID, status)
            valid_logger = remove_handler(valid_logger)
            return False

        valid_logger = remove_handler(valid_logger)
        return True

    def Register(self):
        LOGGER_NAME = 'Member.Register'
        DATATYPE = 'DB_Member'

        Method = Common(LOGGER_NAME, DATATYPE)

        Base = {}
        Base[self.ID] = {
            'Annual-Fee': None,
            'Class': None,
            'Creation-Date': str(datetime.now()),
            'Entitlement': None,
            'Membership-Status': 'Active',
            'Membership-Type': None,
            'Name': None,
            'One-Time-Deposit': None,
            'Penalty': None,
            'Renewal-Date': None,
            'Stock': {
                'Borrowing': {},
                'Returned': {}
            }
        }

        return Method.Register(self.ID, Base)

    @property
    def total_borrowing(self):
        total = len(self.database[self.ID]['Stock']['Borrowing'].keys())
        return total

    def BorrowStock(self, StockID):

        logger = get_logger('Member.BorrowStock')

        if not self.valid_ID:
            logger.info('Invalid %s', self.ID)
            logger = remove_handler(logger)
            return False

        if StockID in self.database[self.ID]['Stock']['Borrowing']:
            logger.error('Serious ERROR had occured, please solve the bugs before next run to prevent Database CORRUPTED')
            raise Exception('Serious ERROR had occured, please solve the bugs before next run to prevent Database CORRUPTED')

        self.database[self.ID]['Stock']['Borrowing'][StockID] = {
                                                                'Date-Borrowed': str(datetime.now()),
                                                                'Due-Date': str(datetime.now() + timedelta(days = 7))
                                                                }
        DB_Member.Dump(self.database)

        logger.info('Member %s had successfully borrowed stock %s', self.ID, StockID)
        logger = remove_handler(logger)

        return True

    def ReturnStock(self, StockID, PenaltyLateReturn):

        logger = get_logger('Member.ReturnStock')

        if not self.valid_ID:
            logger.info('Invalid %s', self.ID)
            logger = remove_handler(logger)
            return False

        if StockID not in self.database[self.ID]['Stock']['Borrowing']:
            raise Exception('Serious ERROR had occured, please solve the bugs before next run to prevent Database CORRUPTED')

        penalty = self._PenaltyLateReturn(StockID, PenaltyLateReturn)
        if penalty > 0:
            try:
                while True:
                    if input(f'Enter "CONFIRM" after the payment (RM {penalty:.2f}) is made by member ({self.ID}) to continue: ') == 'CONFIRM':
                        break
            except KeyboardInterrupt:
                logger.warning('Payment transaction failed, please try again')
                return False

        date_borrowed = self.database[self.ID]['Stock']['Borrowing'][StockID]['Date-Borrowed']
        del self.database[self.ID]['Stock']['Borrowing'][StockID]

        try: count = len(self.database[self.ID]['Stock']['Returned'][StockID])
        except KeyError:
            count = 0
            self.database[self.ID]['Stock']['Returned'][StockID] = {}

        self.database[self.ID]['Stock']['Returned'][StockID][str(count + 1)] = {
                                                                                'Date-Borrowed': date_borrowed,
                                                                                'Date-Returned': str(datetime.now())
                                                                                }

        DB_Member.Dump(self.database)

        logger.info('Member %s had successfully returned back stock %s', self.ID, StockID)
        logger = remove_handler(logger)

        return True

    def TotalPenalty(self, PenaltyLateReturn):

        total = 0

        for stock_id in self.database[self.ID]['Stock']['Borrowing']:
            total += self._PenaltyLateReturn(stock_id, PenaltyLateReturn)

        return total

    def _PenaltyLateReturn(self, StockID, PenaltyLateReturn):

        logger = get_logger('Member._PenaltyLateReturn')

        if not self.valid_ID:
            logger.info('Invalid %s', self.ID)
            logger = remove_handler(logger)
            return False

        if StockID not in self.database[self.ID]['Stock']['Borrowing']:
            logger.critical('%s is not borrowed by %s', StockID, self.ID)
            logger = remove_handler(logger)
            return False

        due_date = datetime.strptime(self.database[self.ID]['Stock']['Borrowing'][StockID]['Due-Date'], '%Y-%m-%d %H:%M:%S.%f')

        if due_date >= datetime.now():
            logger = remove_handler(logger)
            return 0

        time_delta = datetime.now() - due_date
        time_delta_seconds = time_delta.total_seconds() # Convert timedelta class into seconds
        time_delta_days = time_delta_seconds // 86400 # 1 day 86400 seconds
        subtotal = time_delta_days * PenaltyLateReturn # Default 1 day RM0.50

        logger = remove_handler(logger)
        return subtotal

    def ListBorrowing(self, PenaltyLateReturn):

        logger = get_logger('Member.ListBorrowing')

        if not self.valid_ID:
            logger.info('Invalid %s', self.ID)
            logger = remove_handler(logger)
            return False

        if not self.database[self.ID]['Stock']['Borrowing']:
            logger.warning('Database is empty')
            logger = remove_handler(logger)
            return False

        ### Getting the headers of the table
        List = []
        SList = ['Stock-ID']
        for y in self.database[self.ID]['Stock']['Borrowing'].values():
            for yx in y:
                if yx not in SList:
                    SList.append(yx)

        SList.append('Subtotal-Penalty')
        List.append(SList)


        ### Getting the data of the table
        for stock_id in self.database[self.ID]['Stock']['Borrowing'].keys():
            SList = [stock_id]

            for header in List[0]:
                if header in ('Stock-ID', 'Subtotal-Penalty'):
                    continue

                SList.append(self.database[self.ID]['Stock']['Borrowing'][stock_id][header])

            List.append(SList)

        ### Getting the subtotal of the penalty
        for i in range(1, len(List)):
            stock_id = List[i][0]
            penalty = self._PenaltyLateReturn(stock_id, PenaltyLateReturn)
            List[i].append(penalty)


        ### Print total of penalty
        SList = []
        for i in range(1, len(List[0])):
            SList.append('')

        SList.append(f'Total-Penalty: RM {self.TotalPenalty(PenaltyLateReturn):.2f}')
        List.append(SList)

        logger = remove_handler(logger)
        return List

    def Modify(self, Key, Value):
        LOGGER_NAME = 'Member.Modify'
        DATATYPE = 'DB_Member'

        Method = Common(LOGGER_NAME, DATATYPE)
        return Method.Modify(self.ID, Key, Value)

    def Delete(self):
        logger = get_logger('Member.Delete')

        if self.ID == '':
            logger = remove_handler(logger)
            return False

        if not self.valid_ID:
            logger.info('Invalid %s', self.ID)
            logger = remove_handler(logger)
            return False

        length = len(self.database[self.ID]['Stock']['Borrowing'])

        if length >= 1:
            logger.info('Member (%s) still borrowing %i stocks, please return all the stocks before next deletion operation', self.ID, length)
            logger = remove_handler(logger)
            return False

        del self.database[self.ID]
        logger.info('Deletion successful for %s', self.ID)
        DB_Member.Dump(self.database)

        logger = remove_handler(logger)
        return True
