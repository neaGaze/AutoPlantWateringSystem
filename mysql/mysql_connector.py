import mysql.connector
from mysql.connector import Error

class MysqlDriver:
    _instance = None

    CHANNEL = "Channel"
    PLANT = "Plant"
    Activity = "Activity"

    def __init__(self, host, db, user, pwd):
        # instance()
        self.connection = None
        self.host = host
        self.db = db
        self.user = user
        self.pwd = pwd

    @classmethod
    def instance(self, host=None, db=None, user=None, pwd=None):
        if _instance == None:
            print("Creating a new MySQL Instance")
            _instance = MysqlDriver(host, db, user, pwd) #__new__(cls)
        else:
            print("Reusing old instance")
        return _instance

    def connect(self):
        try:
            self.connection = mysql.connector.connect(host=self.host,
                                                database=self.db,
                                                user=self.user,
                                                password=self.pwd)           
            if self.connection.is_connected():
                db_Info = self.connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)              
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.connection.is_connected()

    def disconnect(self):
        if self.connection.is_connected():
            self.connection.close()

    def fetch(self):
        if self.connection.is_connected():
            cursor = self.connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("Fetched from the database.")
            cursor.close()

    def insert(self, stmt):
        if self.connection.is_connected():
            cursor = self.connection.cursor()
            # cursor.execute("insert into table ")
            stmt(cursor)
            record = cursor.commit()
            print("Inserted into the database.")
            cursor.close()

    def delete(self):
        pass

    def update(self):
        pass
