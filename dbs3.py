import sqlite3
import json


class Db:

    schema_file = "schema.sql"

    def __init__(self, databaseName="files.db"):
        self.databaseName = databaseName
        self.conn = None
        self.cur = None


    def connect(self):
        with sqlite3.connect(self.databaseName) as self.conn:
            self.cur = self.conn.cursor()


    def checkTableExists(self, tableName):
        if not self.conn:
            self.connect()

        self.cur.execute("""
            SELECT count(*) as cnt
            FROM sqlite_master
            WHERE type='table' AND name='files'
        """)
        return self.cur.fetchone()[0]



    def read_schema(self):
        with open(self.schema_file) as sf:
            lines = sf.readlines()

        copy_started = False
        par = 0
        tables = []
        collect = []
        for line in lines:
            row = line.strip()        
            if row.startswith("CREATE TABLE"):
                if par != 0:
                    collect = []
                copy_started = True
                collect.append(row)
                par = row.count("(") - row.count(")")
                continue

            if copy_started: 
                if par != 0:
                    collect.append(row)
                    par += row.count("(") - row.count(")")
                else:
                    copy_started = False
                    tables.append("".join(collect))
                    collect = []

        # flush collect if has lines and parantesis = 0
        if copy_started and par == 0:
            copy_started = False
            tables.append("".join(collect))

        return tables


    def createFilesTable(self):
        tables = self.read_schema()

        for table in tables:
            try:
                self.cur.execute(table)
            except sqlite3.OperationalError as err:
                print("Table cannot be created:\n{}".format(table))
                print("Error: {}".format(err))
                continue


    def checkConnection(self):
        if not self.checkTableExists("files"):
            self.createFilesTable()


    def saveFiles(self, files):

        self.checkConnection()

        for fileName, md5 in files.items():
            # Insert a row of data
            self.cur.execute(
                """
                INSERT OR REPLACE
                INTO files (fileName, md5)
                VALUES (?, ?)
                """, (fileName, md5)
            )

            print("{} = {}".format(fileName, md5))

        # Save (commit) the changes
        self.conn.commit()


    def test_file(self, fileName, testValue) -> int:
        self.checkConnection()
        self.cur.execute(
            """
            SELECT filename, md5
            FROM files
            WHERE fileName = ?
            """, (fileName,)
        )
        record = self.cur.fetchone()
        if record is None:
            return -1

        return 1 if record[1] == testValue else 0


if __name__ == "__main__":
    db = Db()

    db.checkConnection()