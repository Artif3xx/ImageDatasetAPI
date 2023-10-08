import json
import sqlite3
from pathlib import Path

# define the production database here. This is the database that will be used as default
produktionDatabase: str = 'data/Database.db'


def execute_sql_query(sql_query, data=None, databaseName: str = produktionDatabase):
    """
    Execute a SQL query and return the result.

    :param sql_query: the sql query to execute
    :param data: the data to insert into the sql query, this is optional
    :param databaseName: der Name der Datenbank, auf der der Befehl ausgeführt werden soll
    :return: the fetched rows as a list of json objects
    """
    # Verbindung zur Datenbank herstellen
    conn = sqlite3.connect(databaseName)
    cursor = conn.cursor()

    try:
        if data:
            # SQL-Befehl mit Daten ausführen
            cursor.execute(sql_query, data)
        else:
            # SQL-Befehl ausführen
            cursor.execute(sql_query)

        # Änderungen in der Datenbank speichern
        conn.commit()

        # print("SQL query executed successfully.")
    except sqlite3.Error as e:
        print(f"[Error] --> Error executing SQL query: {e}")
    finally:
        # Ergebnis des SQL-Befehls abrufen
        rows = cursor.fetchall()
        # Ergebniszeilen in JSON-Objekte konvertieren
        json_rows = []
        for row in rows:
            row_dict = {}
            for idx, col in enumerate(cursor.description):
                row_dict[col[0]] = row[idx]
            json_rows.append(row_dict)

    # Verbindung zur Datenbank trennen
    conn.close()
    # Ergebnis des SQL-Befehls zurückgeben
    return json.loads(json.dumps(json_rows))


class Database:
    """
    This class handles the database. It creates a new database if it does not exist and creates the tables. It is used
    as init function. To just execute a query use the execute_sql_query function.
    """
    databaseName = ""

    def __init__(self, databaseName: str = produktionDatabase):
        """
        Simple constructor to initialize the database with a database or the production database
        """
        self.databaseName = databaseName
        self.initDatabase()

    def executeSql(self, query, data=None):
        """
        Execute a SQL query and return the result.
        :param query: the sql query to execute
        :param data: the data to insert into the sql query, this is optional
        :return: the fetched rows as a list of json objects
        """
        return execute_sql_query(query, data, self.databaseName)

    def initDatabase(self):
        """
        creates a new database in the folder "databases" and creates the tables
        """
        self.createDatabase()

        # create a table for the balance of the front cash register
        Images = """
                    CREATE TABLE IF NOT EXISTS Images (
                        id INTEGER PRIMARY KEY,
                        path TEXT UNIQUE,
                        metadata TEXT,
                        labels TEXT
                    ); 
                """
        self.executeSql(query=Images)

    def createDatabase(self):
        """
        creates a new database in the folder "databases"
        """
        # check if the database already exists
        if Path(self.databaseName).is_file():
            print(f'[Info] --> Database "{self.databaseName}" already exists.')
            return

        # create a connection to the database
        conn = sqlite3.connect(self.databaseName)
        conn.close()

        print(f'[Info] --> Database "{self.databaseName}" created successfully.')
