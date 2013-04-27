import sqlite3

conn = sqlite3.connect("main.db")
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE feed(feed text, url text, pubdate date)
''')

conn.commit()
conn.close

