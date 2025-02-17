""" database > db_connection.py """
import sqlite3

DB_NAME = 'database.db'


def get_connection():
    """ Returns a database connection """
    return sqlite3.connect(DB_NAME)
