
import time

from difflib import SequenceMatcher
from typing import Optional
from jsonmerge import merge

from .Constants import UNMODIFIABLE_LIST, UNPUBLICITY_LIST
from .Database import DB_Storing, DB_Member, DB_Employee
from .Logging import get_logger, remove_handler

class Common:

    def __init__(self, LOGGER_NAME, DATATYPE):
        self.logger_name = LOGGER_NAME
        self.datatype = DATATYPE

        if DATATYPE not in ('DB_Storing', 'DB_Employee', 'DB_Member'):
            raise Exception(f'Invalid parameter DATATYPE: {DATATYPE}')
        elif DATATYPE == 'DB_Storing':
            self.db = DB_Storing
            self.database = DB_Storing.Retrieve()
        elif DATATYPE == 'DB_Employee':
            self.db = DB_Employee
            self.database = DB_Employee.Retrieve()
        elif DATATYPE == 'DB_Member':
            self.db = DB_Member
            self.database = DB_Member.Retrieve()

    def List(self,
            ID: Optional[str] = None,
            Only_Modifiable: bool = False,
            Include_Title: bool = True,
            Title_Only: bool = False
            ):

        logger = get_logger(self.logger_name)

        if not self.database.keys():
            logger.warning('Database is empty.')
            logger = remove_handler(logger)
            return False

        List = []
        if Include_Title or Title_Only: SList = ['ID']
        else: SList = []

        if Include_Title or Title_Only:
            for y in self.database.values():
                for yx in y:

                    if yx in UNPUBLICITY_LIST:
                        continue

                    if Only_Modifiable is True:
                        if yx in UNMODIFIABLE_LIST:
                            continue

                    SList.append(yx)
                break
            List.append(SList)

        if Title_Only:
            logger = remove_handler(logger)
            return List

        if ID is None:
            for x, y in self.database.items():
                SList = [x]
                for yx in y:

                    if yx in UNPUBLICITY_LIST:
                        continue

                    if Only_Modifiable is True:
                        if yx in UNMODIFIABLE_LIST:
                            continue

                    SList.append(self.database[x][yx])
                List.append(SList)

        elif ID is not None:
            SList = [ID]
            for x in self.database[ID].keys():

                if x in UNPUBLICITY_LIST:
                    continue

                if Only_Modifiable is True:
                    if x in UNMODIFIABLE_LIST:
                        continue

                SList.append(self.database[ID][x])
            List.append(SList)

        logger = remove_handler(logger)
        if Include_Title is False and Title_Only is False and ID != None: return SList
        else: return List

    def Search(self, *keywords):
        logger = get_logger(self.logger_name)

        if keywords == ('',):
            logger = remove_handler(logger)
            return False

        if not self.database.keys():
            logger.warning('Database is empty.')
            logger = remove_handler(logger)
            return False

        start_time = time.time() * 1000

        ListID = []
        for x, y in self.database.items():
            for yx in y:
                for z in keywords:
                    if (SequenceMatcher(None, str(z), str(x)).ratio() >= 0.7) or (SequenceMatcher(None, str(z), str(self.database[x][yx])).ratio() >= 0.7):
                        if x not in ListID:
                            ListID.append(x)

        List = self.List(Title_Only = True)
        for x in ListID:
            List.append(
                self.List(ID = x, Include_Title = False)
            )

        logger = get_logger(self.logger_name)
        logger.info('Finished searching by given keywords: %s (Execution time: %.2f ms)', keywords, (time.time() * 1000 - start_time))
        logger = remove_handler(logger)
        return List

    def valid_ID(self, ID):
        if ID == '': return False
        return bool(ID in self.database.keys())

    def Register(self, ID, DATADUMP):
        logger = get_logger(self.logger_name)

        if self.valid_ID(ID):
            logger.info('%s is existing, thus will not be added', ID)
            logger = remove_handler(logger)
            return False

        if ID == '':
            logger = remove_handler(logger)
            return False

        Final = merge(DATADUMP, self.database)

        self.db.Dump(Final)
        logger.info('{ID} has been added successfully')

        logger = remove_handler(logger)
        return True

    def Modify(self, ID, Key, Value):
        logger = get_logger(self.logger_name)

        if Key == '':
            logger = remove_handler(logger)
            return False

        if Value == '':
            Value = None

        if not self.valid_ID(ID):
            logger.info('Invalid %s, please register', ID)
            logger = remove_handler(logger)
            return False

        for x in self.database[ID].keys():
            if x in UNMODIFIABLE_LIST:
                continue

            if SequenceMatcher(None, Key, x).ratio() >= 0.7:
                old_value = self.database[ID][x]
                self.database[ID][x] = Value
                logger.info('(%s) of (%s) has been changed from (%s) -> (%s)', x, ID, old_value, Value)
                break
        else:
            logger.info('Invalid Key: %s', Key)
            logger = remove_handler(logger)
            return False

        self.db.Dump(self.database)

        logger = remove_handler(logger)
        return True

    def Delete(self, ID):
        logger = get_logger(self.logger_name)

        if ID == '':
            logger = remove_handler(logger)
            return False

        if not self.valid_ID(ID):
            logger.info('Invalid %s', ID)
            logger = remove_handler(logger)
            return False

        del self.database[ID]
        logger.info('Deletion successful for %s', ID)
        self.db.Dump(self.database)

        logger = remove_handler(logger)
        return True
