
import sqlite3
conn = sqlite3.connect('vin_cache.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS vin_cache
             (vin TEXT PRIMARY KEY, make TEXT, model TEXT, year TEXT, body_class TEXT)''')
c.close()