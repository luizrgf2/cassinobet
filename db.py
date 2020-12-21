import sqlite3

cone = sqlite3.connect('roletas.db')


cursor = cone.cursor()

cursor.execute('SELECT * FROM Table1')


