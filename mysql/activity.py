from mysql_connector import MysqlDriver
from time import time
from datetime import datetime

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
WATER_START_TYPE = "WATER START"
WATER_END_TYPE = "WATER END"

class Activity:

    # ACTIVITY
    INSERT_ACTIVITY = "INSERT INTO Activity (transaction_id, created_at, channel_id, activity_type, is_open) VALUES (%d, %s, %d, %s, %i)"
    READ_IS_OPEN = "SELECT channel_id from Activity where is_open=%i"

    def __init__(self):
        self._driver = MysqlDriver.instance()

    def insert_water_start_txn(self, channel_id):
        if self._driver:
            uniq_id = time()
            cur_time = datetime.now()
            self._driver.insert(lambda cursor: cursor.execute(Activity.INSERT_ACTIVITY % (uniq_id, cur_time, channel_id, WATER_START_TYPE, True)))

    def insert_water_end_txn(self, channel_id, txn_id):
        if self._driver:
            cur_time = datetime.now()
            self._driver.insert(lambda cursor: cursor.execute(Activity.INSERT_ACTIVITY % (txn_id, cur_time, channel_id, WATER_END_TYPE, False)))

    def read_are_open(self):
        if self._driver:
            return list(self._driver.fetchall(lambda cursor: cursor.execute(Activity.READ_IS_OPEN % True)))
        return []