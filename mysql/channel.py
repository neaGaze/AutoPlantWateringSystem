from mysql_connector import MysqlDriver

class Channel:

    # CHANNEL
    INSERT_CHANNEL = "INSERT INTO Channel (channel_id, plant_id, water_start_trigger, water_end_trigger, delay) VALUES (%d, %d, %f, %f, %d)"
    UPDATE_CHANNEL__WATER_START_TRIGGER = "UPDATE Channel SET water_start_trigger=%f WHERE channel_id=%d"
    UPDATE_CHANNEL__WATER_END_TRIGGER = "UPDATE Channel SET water_end_trigger=%f WHERE channel_id=%d"
    UPDATE_CHANNEL__DELAY = "UPDATE Channel SET delay=%d WHERE channel_id=%d"
    READ_WATER_START_TRIGGER = "SELECT water_start_trigger FROM Channel where channel_id=%d"
    READ_WATER_END_TRIGGER = "SELECT water_end_trigger FROM Channel where channel_id=%d"


    def __init__(self):
        self._driver = MysqlDriver.instance()

    def update_start_trigger(self, channel_id, value):
        if self._driver:
            self._driver.insert(lambda cursor: cursor.execute(Channel.UPDATE_CHANNEL__WATER_START_TRIGGER % (value, channel_id)))
    
    def update_end_trigger(self, channel_id, value):
        if self._driver:
            self._driver.insert(lambda cursor: cursor.execute(Channel.UPDATE_CHANNEL__WATER_END_TRIGGER % (value, channel_id)))

    def update_delay(self, channel_id, delay):
        if self._driver:
            self._driver.insert(lambda cursor: cursor.execute(Channel.UPDATE_CHANNEL__DELAY % (delay, channel_id)))
    
    def read_start_trigger(self, channel_id):
        start_trigger = 0.0
        if self._driver:
            record = self._driver.fetch(lambda cursor: cursor.execute(Channel.READ_WATER_START_TRIGGER % (channel_id)))
            start_trigger = int(record[0]) if len(record) > 0 else 0.0
        return start_trigger

    def read_end_trigger(self, channel_id):
        end_trigger = 0.0
        if self._driver:
            record = self._driver.fetch(lambda cursor: cursor.execute(Channel.READ_WATER_END_TRIGGER % (channel_id)))
            end_trigger = int(record[0]) if len(record) > 0 else 0.0
        return end_trigger