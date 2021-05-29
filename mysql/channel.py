from mysql_connector import MysqlDriver

class Channel:

    # CHANNEL
    INSERT_CHANNEL = "INSERT INTO Channel (channel_id, plant_id, water_start_trigger, water_end_trigger) VALUES (%d, %d, %f, %f)"
    UPDATE_CHANNEL__WATER_START_TRIGGER = "UPDATE Channel SET water_start_trigger=%f WHERE channel_id=%d"
    UPDATE_CHANNEL__WATER_END_TRIGGER = "UPDATE Channel SET water_end_trigger=%f WHERE channel_id=%d"


    def __init__(self):
        self._driver = MysqlDriver.instance()

    def update_start_trigger(self, channel_id, value):
        if self._driver:
            self._driver.insert(lambda cursor: cursor.execute(Channel.UPDATE_CHANNEL__WATER_START_TRIGGER % (channel_id, value)))
    
    def update_end_trigger(self, channel_id, value):
        if self._driver:
            self._driver.insert(lambda cursor: cursor.execute(Channel.UPDATE_CHANNEL__WATER_END_TRIGGER % (channel_id, value)))
