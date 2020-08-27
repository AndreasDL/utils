import json
import pyodbc

class SQLConnection():
    def __init__(self, server_name, database, uid, pwd):
        self.server_name = server_name
        self.database = database
        self.uid = uid
        self.pwd = pwd

        self.conn_str = f"""
            Driver={{ODBC driver 17 for SQL Server}};
            SERVER={self.server_name};
            DATABASE={self.database};
            UID={self.uid};
            PWD={self.pwd};
        """

    @staticmethod
    def from_config(config_path):
        dbconfig = json.load(open(config_path))
        return SQLConnection(
            dbconfig["host"],
            dbconfig["database"],
            dbconfig["user"],
            dbconfig["pwd"]
        )

    def runQuery(self, query, parameters=None, as_dict=False, returns=True):

        if parameters is None:
            parameters = ()

        con = pyodbc.connect(self.conn_str)
        with con.cursor() as cur:
            cur.execute(query, parameters)

            if not returns:
                con.commit()
                return []

            if as_dict:
                column_names = [col[0] for col in cur.description]
                return [
                    dict(zip(column_names, row))
                    for row in cur.fetchall()
                ]

            return cur.fetchall()

    def executeMany(self, sql, parameters):
        connection = pyodbc.connect(self.conn_str)
        cursor = connection.cursor()
        cursor.fast_executemany = True
        cursor.executemany(sql, parameters)
        connection.commit()
