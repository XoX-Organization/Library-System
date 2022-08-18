
from datetime import datetime
from tabulate import tabulate

from .Common_Methods import Common
from .Database import DB_Storing
from .Logging import get_logger, get_receipt_logger, remove_handler
from .Member import Member

class Storing:

    def __init__(self, ID):
        self.ID = ID

    @property
    def database(self):
        try: self._database
        except AttributeError: self._database = DB_Storing.Retrieve()
        return self._database

    @staticmethod
    def List(ID: bool = None,
            Only_Modifiable: bool = False
            ):

        LOGGER_NAME = 'Storing.List'
        DATATYPE = 'DB_Storing'

        Method = Common(LOGGER_NAME, DATATYPE)
        return Method.List(ID = ID, Only_Modifiable = Only_Modifiable)

    @staticmethod
    def Search(*keywords):
        LOGGER_NAME = 'Storing.Search'
        DATATYPE = 'DB_Storing'

        Method = Common(LOGGER_NAME, DATATYPE)
        return Method.Search(*keywords)

    @property
    def valid_ID(self):

        if self.ID not in self.database:
            return False

        return True

    @property
    def valid_StockID(self):

        BaseID = self.ID[:-5]

        if BaseID not in self.database:
            return False

        if self.ID not in self.database[BaseID]['Stock']:
            return False

        self.base_id = BaseID

        return True

    def Register(self):
        LOGGER_NAME = 'Storing.Register'
        DATATYPE = 'DB_Storing'

        Method = Common(LOGGER_NAME, DATATYPE)

        Base = {}
        Base[self.ID] = {
            'Author': None,
            'BookTitle': None,
            'Catalogue-Type': None,
            'Creation-Date': str(datetime.now()),
            'Internal-Reference': None,
            'ISBN-Number': None,
            'Pricing': None,
            'Stock': {},
            'Subject': None
            }

        return Method.Register(self.ID, Base)

    def AddStock(self):
        logger = get_logger('Storing.AddStock')

        if not self.valid_ID:
            logger.info('Invalid %s', self.ID)
            logger = remove_handler(logger)
            return False

        total_stock = len(self.database[self.ID]['Stock'])

        if total_stock >= 99999:
            logger.critical('Base Item %s has reached the maximum stock amounts (%i)', self.ID, total_stock)
            logger = remove_handler(logger)
            return False

        level = total_stock + 1
        stock_new_id = self.ID + str(level).zfill(5)

        self.database[self.ID]['Stock'][stock_new_id] = {
            'Date-Added': str(datetime.now()),
            'Date-Sold': None,
            'Latest-Date-Lent': None,
            'Latest-Date-Returned': None,
            'Latest-Member-Borrowed': None,
            'Status': 'Available'
        }

        logger.info('New stock (%s) -> Base (%s) , Currently left ({len(self.StockLeft())}) in storage.', stock_new_id, self.ID)
        DB_Storing.Dump(self.database)

        logger = remove_handler(logger)
        return stock_new_id

    def DeleteStock(self):
        logger = get_logger('Storing.DeleteStock')

        if not self.valid_StockID:
            logger.info('Invalid %s', self.ID)
            logger = remove_handler(logger)
            return False

        if self.database[self.base_id]['Stock'][self.ID]['Status'] in ('Lending', 'Sold', 'Deleted'):
            logger.info('Stock %s is not available right now', self.ID)
            logger = remove_handler(logger)
            return False

        initial_status = self.database[self.base_id]['Stock'][self.ID]['Status']
        self.database[self.base_id]['Stock'][self.ID]['Status'] = 'Deleted'
        DB_Storing.Dump(self.database)

        logger.info('Status of stock (%s): (%s) -> (Deleted) , Currently left ({len(self.StockLeft())}) in storage (%s).', self.ID, initial_status, self.base_id)
        logger = remove_handler(logger)

        return True

    @staticmethod
    def SellStock(
        EmployeeID,
        *StockID,
        JustCheckPriceOnly: bool = True
        ):

        logger = get_logger('Storing.SellStock')

        database = DB_Storing.Retrieve()
        subtotal = 0
        stock_available = []
        stock_list = [['STOCK ID', 'BOOK TITLE', 'PRICING']]

        for stock_id in StockID:

            BaseID = stock_id[:-5]

            if BaseID not in database:
                logger.info('Invalid %s', stock_id)
                continue

            if stock_id not in database[BaseID]['Stock']:
                logger.info('Invalid %s', stock_id)
                continue

            if database[BaseID]['Stock'][stock_id]['Status'] in ('Lending', 'Sold', 'Deleted'):
                logger.info('Stock %s is not available right now', stock_id)
                continue

            price = database[BaseID]['Pricing']
            if price is None:
                logger.info("Item %s haven't set a price yet", BaseID)
                continue

            stock_available.append(stock_id)
            subtotal += float(price)
            stock_title = database[BaseID]['BookTitle']
            stock_list.append([stock_id, stock_title, price])

            if JustCheckPriceOnly is False:
                initial_status = database[BaseID]['Stock'][stock_id]['Status']
                database[BaseID]['Stock'][stock_id]['Status'] = 'Sold'
                database[BaseID]['Stock'][stock_id]['Date-Sold'] = str(datetime.now())
                DB_Storing.Dump(database)


                logger.info('Status of stock (%s): (%s) -> (Sold)', stock_id, initial_status)


        if (JustCheckPriceOnly is False) and (len(stock_list) > 1):
            logger_receipt = get_receipt_logger(EmployeeID)
            logger_receipt.info(tabulate(
                                            stock_list,
                                            headers = 'firstrow',
                                            tablefmt = 'grid',
                                            showindex = True,
                                            missingval = 'N/A'
                                        ) +
                                f'\nSUBTOTAL: {subtotal}'
                                )
            logger_receipt = remove_handler(logger_receipt)

        logger = remove_handler(logger)
        return stock_list, stock_available, subtotal

    def LendStock(self,
                MaximumBorrowAllowed,
                MemberID: bool = None
                ):

        logger = get_logger('Storing.LendStock')

        member = Member(MemberID)

        if MemberID is not None:
            if not member.valid_ID:
                logger.info('Invalid Member ID %s', MemberID)
                logger = remove_handler(logger)
                return False

        if not self.valid_StockID:
            logger.info('Invalid %s', self.ID)
            logger = remove_handler(logger)
            return False

        if member.total_borrowing >= MaximumBorrowAllowed:
            logger.info('%s has total of %i books which has reached the maximum', MemberID, member.total_borrowing)
            logger = remove_handler(logger)
            return False

        if self.database[self.base_id]['Stock'][self.ID]['Status'] in ('Lending', 'Sold', 'Deleted'):
            logger.info('Stock %s is not available right now', self.ID)
            logger = remove_handler(logger)
            return False

        if MemberID is not None:
            if not member.BorrowStock(self.ID):
                return False
            self.database[self.base_id]['Stock'][self.ID]['Latest-Member-Borrowed'] = MemberID
        else:
            self.database[self.base_id]['Stock'][self.ID]['Latest-Member-Borrowed'] = None

        initial_status = self.database[self.base_id]['Stock'][self.ID]['Status']
        self.database[self.base_id]['Stock'][self.ID]['Status'] = 'Lending'
        self.database[self.base_id]['Stock'][self.ID]['Latest-Date-Lent'] = str(datetime.now())
        self.database[self.base_id]['Stock'][self.ID]['Latest-Date-Returned'] = None

        DB_Storing.Dump(self.database)

        logger.info('Status of stock (%s): (%s) -> (Lending) -> Member (%s) , Currently left (%i) in storage (%s).', self.ID, initial_status, MemberID, len(self.StockLeft()), self.base_id)
        logger = remove_handler(logger)

        return True

    def ReturnStock(self, PenaltyLateReturn):

        logger = get_logger('Storing.ReturnStock')

        if not self.valid_StockID:
            logger.info('Invalid %s', self.ID)
            logger = remove_handler(logger)
            return False

        if self.database[self.base_id]['Stock'][self.ID]['Status'] in ('Available', 'Sold', 'Deleted'):
            logger.info('Stock %s is currently available right now, perhaps you entered a wrong stock id?', self.ID)
            logger = remove_handler(logger)
            return False

        MemberID = self.database[self.base_id]['Stock'][self.ID]['Latest-Member-Borrowed']
        if MemberID is not None:
            if not Member(MemberID).ReturnStock(self.ID, PenaltyLateReturn):
                return False

        initial_status = self.database[self.base_id]['Stock'][self.ID]['Status']
        self.database[self.base_id]['Stock'][self.ID]['Status'] = 'Available'
        self.database[self.base_id]['Stock'][self.ID]['Latest-Date-Returned'] = str(datetime.now())

        DB_Storing.Dump(self.database)

        logger.info('Status of stock (%s): (%s) -> (Available) , Currently left (%i) in storage (%s).', self.ID, initial_status, len(self.StockLeft()), self.base_id)
        logger = remove_handler(logger)

        return True

    def StockLeft(self):
        logger = get_logger('Storing.StockLeft')

        base_id = self.ID
        if not self.valid_ID:
            if not self.valid_StockID:
                logger.info('Invalid %s', self.ID)
                logger = remove_handler(logger)
                return False

            base_id = self.ID[:-5]

        stock_available_list = []
        for stock in self.database[base_id]['Stock']:
            if self.database[base_id]['Stock'][stock]['Status'] == 'Available':
                stock_available_list.append(stock)

        return stock_available_list

    def Modify(self, Key, Value):
        LOGGER_NAME = 'Storing.Modify'
        DATATYPE = 'DB_Storing'

        Method = Common(LOGGER_NAME, DATATYPE)
        return Method.Modify(self.ID, Key, Value)

    def Delete(self):
        logger = get_logger('Storing.Delete')

        if self.ID == '':
            logger = remove_handler(logger)
            return False

        if not self.valid_ID:
            logger.info('Invalid %s', self.ID)
            logger = remove_handler(logger)
            return False

        for stock_id in self.database[self.ID]['Stock'].keys():
            if self.database[self.ID]['Stock'][stock_id]['Status'] in ('Lending'):
                member_borrowed = self.database[self.ID]['Stock'][stock_id]['Latest-Member-Borrowed']
                logger.info('Stock (%s) of (%s) is currently borrowed by member (%s), please gather all the stocks before next deletion operation', stock_id, self.ID, member_borrowed)
                logger = remove_handler(logger)
                return False

        del self.database[self.ID]
        logger.info('Deletion successful for %s', self.ID)
        DB_Storing.Dump(self.database)

        logger = remove_handler(logger)
        return True
