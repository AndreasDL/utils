import json
import psycopg2
import psycopg2.errorcodes
import psycopg2.extras

class SQLConnection():
    def __init__(self, user, pwd, host, port, database):
        self.user = user
        self.pwd = pwd
        self.database = database
        self.host = host
        self.port = port

    def get_connection(self):
        return psycopg2.connect(
            user=self.user,
            password= self.pwd,
            host=self.host,
            port=self.port,
            database=self.database
        )

    @staticmethod
    def from_config(config_path):
        dbconfig = json.load(open(config_path))
        return SQLConnection(
            dbconfig["user"],
            dbconfig["pwd"],
            dbconfig["host"],
            dbconfig["port"],
            dbconfig["database"]
        )

    def runQuery(self, query, parameters=None, returns=True):

        results = None

        try:
            con = psycopg2.connect(
                user=self.user,
                password= self.pwd,
                host=self.host,
                port=self.port,
                database=self.database
            )

            cur = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            if parameters is None:
                cur.execute(query)

            else:
                cur.execute(query, parameters)


            if returns:
                results = cur.fetchall()
            
            con.commit()

        except (Exception, psycopg2.Error) as error:
            print("ERROR", error)
        finally:
            if (con):
                cur.close()
                con.close()

        return results

    def executeMany(self, query, parameters):
        #try:
        con = psycopg2.connect(
            user=self.user,
            password= self.pwd,
            host=self.host,
            port=self.port,
            database=self.database
        )

        cur = con.cursor()
        cur.executemany(query, parameters)
        con.commit()

        #except (Exception, psycopg2.Error) as error:
        #    print("ERROR", error, type(error))

        #finally:
        #    if (con):
        #        cur.close()
        #        con.close()
