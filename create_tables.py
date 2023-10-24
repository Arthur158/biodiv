
import sqlite3

from constants import DATABASE_NAME


try:
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    
    try:
        c.execute('''
            CREATE TABLE IF NOT EXISTS regions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                climate TEXT NOT NULL
            );
        ''')
        print("Successfully created 'regions' table.")
    except sqlite3.OperationalError as e:
        print("Could not create 'regions' table:", e)

    try:
        c.execute('''
            CREATE TABLE IF NOT EXISTS species (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                trophic_type TEXT NOT NULL,
                heterotroph_level INTEGER
            );
        ''')
        print("Successfully created 'species' table.")
    except sqlite3.OperationalError as e:
        print("Could not create 'species' table:", e)

    try:
        c.execute('''
            CREATE TABLE IF NOT EXISTS populations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                species TEXT NOT NULL,
                population_size INTEGER NOT NULL,
                region TEXT NOT NULL                
            );
        ''')
        print("Successfully created 'populations' table.")
    except sqlite3.OperationalError as e:
        print("Could not create 'populations' table:", e)

    conn.commit()
    
except sqlite3.Error as e:
    print("Database connection error:", e)

finally:
    if conn:
        conn.close()
