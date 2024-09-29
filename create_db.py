import sqlite3

conn = sqlite3.connect('stem_courses.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        surname TEXT NOT NULL,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        address TEXT NOT NULL,
        personal_phone TEXT NOT NULL,
        sponsor_phone TEXT NOT NULL,
        email TEXT NOT NULL,
        course TEXT NOT NULL
    )
''')

conn.commit()
conn.close()
