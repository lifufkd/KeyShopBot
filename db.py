#####################################
#            Created by             #
#                SBR                #
#####################################
import os
import sqlite3
#####################################


class DB:
    def __init__(self, path, lock):
        super(DB, self).__init__()
        self.__lock = lock
        self.__db_path = path
        self.__cursor = None
        self.__db = None
        self.init()

    def init(self):
        if not os.path.exists(self.__db_path):
            self.__db = sqlite3.connect(self.__db_path, check_same_thread=False)
            self.__cursor = self.__db.cursor()
            self.__cursor.execute('''
            CREATE TABLE users(
            row_id INTEGER primary key autoincrement not null,
            user_id INTEGER,
            first_name TEXT,
            last_name TEXT,
            nick_name TEXT,
            sales INTEGER,
            is_admin BOOL,
            pay_amount INTEGER,
            UNIQUE(user_id)
            )
            ''')
            self.__cursor.execute('''
            CREATE TABLE products(
            row_id TEXT,
            photo BLOB,
            price INTEGER,
            key TEXT,
            category TEXT,
            preview TEXT,
            description TEXT,
            distro_url TEXT,
            instruction_url TEXT
            )
            ''')
            self.__cursor.execute('''
            CREATE TABLE sales(
            row_id INTEGER primary key autoincrement not null,
            time INTEGER,
            name TEXT,
            price INTEGER,
            payment_status BOOL,  
            nick_tg TEXT,
            user_id INTEGER,
            key TEXT,
            product INTEGER
            )
            ''')
            self.__cursor.execute('''
            CREATE TABLE categories(
            id TEXT,
            name TEXT
            )
            ''')
            self.__cursor.execute('''
            CREATE TABLE subcategories(
            id TEXT,
            id_categories TEXT,
            name TEXT
            )
            ''')
            self.__db.commit()
            self.__db.close()
        else:
            self.__db = sqlite3.connect(self.__db_path, check_same_thread=False)
            self.__cursor = self.__db.cursor()

    def db_write(self, queri, args):
        with self.__lock:
            self.__cursor.execute(queri, args)
            self.__db.commit()

    def db_read(self, queri, args):
        with self.__lock:
            self.__cursor.execute(queri, args)
            data = self.__cursor.fetchall()
        return data
