import sqlite3
from typing import Any, List, Tuple

from constants import DATABASE_NAME

class DatabaseHandler:
    def __init__(self, db_name = DATABASE_NAME):
        self.db_name = db_name

    def create_table(self):
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        try:
            
            try:
                cursor.execute('''
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
                cursor.execute('''
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
                cursor.execute('''
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
        
        conn.close()

    def execute_sql_query(self, sql_query: str, params: Tuple[Any] = ()) -> List[Tuple[Any]]:

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        try:
            
            cursor.execute(sql_query, params)
            output = cursor.fetchall()
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            output = None
        
        conn.close()
        
        return output

    def insert_region(self, name, climate) -> None:
        # Create a database connection
        conn = sqlite3.connect(self.db_name)
        
        # Create a cursor object
        cursor = conn.cursor()
        
        # Create a query string
        
        cursor.execute("INSERT INTO regions (name, climate) VALUES (?, ?)", (name, climate))
        
        # Commit the changes
        conn.commit()
        
        # Close the connection
        conn.close()

    def insert_population(self, species: str, population_size: int, region: str) -> None:
        # Create a database connection
        conn = sqlite3.connect(self.db_name)
        
        # Create a cursor object
        cursor = conn.cursor()
        
        # Create a query string
        
        cursor.execute("INSERT INTO populations (species, population_size, region) VALUES (?, ?, ?)", (species, population_size, region))
        
        # Commit the changes
        conn.commit()
        
        # Close the connection
        conn.close()

    def insert_species(self, species_name, trophic_type, heterotroph_level) -> None:
        # Create a database connection
        conn = sqlite3.connect(self.db_name)
        
        # Create a cursor object
        cursor = conn.cursor()
        
        # Create a query string
        
        cursor.execute("INSERT INTO species (name, trophic_type, heterotroph_level) VALUES (?, ?, ?)", (species_name, trophic_type, heterotroph_level))
        
        # Commit the changes
        conn.commit()
        
        # Close the connection
        conn.close()
        
    def remove_all(self):

        try:
            
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            # Loop through the tables and delete all records from each table
            for table in ['populations', 'species', 'regions']:
                cursor.execute(f"DELETE FROM {table};")
            
            # Commit the changes
            conn.commit()
            
        except Exception as e:
            # Rollback changes in case of error
            conn.rollback()
            print(f"An error occurred: {e}") 
        
        conn.close()
