import pymysql.cursors

class MySQLConnection:
    def __init__(self, db:str):
        self.connection = pymysql.connect(
            host = 'localhost',
            user = 'root', 
            password = 'root', # YOUR PASSWORD HERE INSTEAD OF 'root'
            db = db,
            charset = 'utf8mb4',
            cursorclass = pymysql.cursors.DictCursor, # this structures our returned data in the form of dictionaries or lists of dictionaries
            autocommit = True
        )
    def query_db(self, query:str, data:dict=None):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                print("Running Query:", query)
                cursor.execute(query)
                # notice we return the cursor directly now, this is so we can handle the different commands in our base model instead
                # this cleans up our code quite a bit, and also avoids the need to have branching conditions
                return cursor
            except Exception as e:
                print("Something went wrong", e) # If our query fails, we should see this in our terminal output
                return False
            finally:
                self.connection.close()

def connectToMySQL(db) -> MySQLConnection:
    return MySQLConnection(db)
