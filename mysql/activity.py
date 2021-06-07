from mysql_connector import MysqlDriver
from time import time
from datetime import datetime

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
WATER_START_TYPE = "WATER START"
WATER_END_TYPE = "WATER END"

class Activity:

    # ACTIVITY
    INSERT_ACTIVITY = "INSERT INTO Activity (created_at, channel_id, activity_type, is_open) VALUES ('%s', %d, '%s', %i)"
    UPDATE_ACTIVITY = "UPDATE Activity SET activity_type='%s', is_open=%i WHERE channel_id=%d and transaction_id=%d"
    READ_IS_OPEN = "SELECT channel_id, transaction_id from Activity where is_open=%i"

    def __init__(self):
        self._driver = MysqlDriver.instance()

    def insert_water_start_txn(self, channel_id):
        if self._driver:
            cur_time = datetime.now()
            print("QUERY into: "+Activity.INSERT_ACTIVITY % (cur_time.strftime(DATETIME_FORMAT), channel_id, WATER_START_TYPE, True))
            self._driver.insert(lambda cursor: cursor.execute(Activity.INSERT_ACTIVITY % (cur_time.strftime(DATETIME_FORMAT), channel_id, WATER_START_TYPE, True)))

    def insert_water_end_txn(self, channel_id, txn_id):
        if self._driver:
            cur_time = datetime.now()
            #self._driver.insert(lambda cursor: cursor.execute(Activity.INSERT_ACTIVITY % (txn_id, cur_time.strftime(DATETIME_FORMAT), channel_id, WATER_END_TYPE, False)))
            self._driver.insert(lambda cursor: cursor.execute(Activity.UPDATE_ACTIVITY % (WATER_END_TYPE, False, channel_id, txn_id)))

    def read_are_open(self):
        if self._driver:
            res = list(map(lambda x: x[0], list(self._driver.fetchall(lambda cursor: cursor.execute(Activity.READ_IS_OPEN % True)))))
            return res
        return []

    def read_are_open_with_txnid(self):
        if self._driver:
            res = list(map(lambda x: (x[0], x[1]), list(self._driver.fetchall(lambda cursor: cursor.execute(Activity.READ_IS_OPEN % True)))))
            return res
        return []