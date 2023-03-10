from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DB

class Model:
    @staticmethod
    def format_data(delim:str, data:dict) -> str: # utilizing type annotations here just for better documentation, they don't affect the codes behavior at all
        # rough JS equivalent would be something like: return Object.keys(data).map(col => `${col}=%(${col})`).join(delim)
        return delim.join(f"`{col}`=%({col})s" for col in data)

    @classmethod
    def create(cls, **data:dict) -> int:
        # notice the utilizing of the ** operator here which takes all key word arguments passed in and wraps them into a dictionary
        # syntax here is a bit different than a normal insert, because MySQL allows you to use the set syntax for insert as well as update
        query = f'''
                INSERT INTO `{cls.table}`
                SET {cls.format_data(", ", data)};
                '''
        return connectToMySQL(DB).query_db(query, data).lastrowid # returns the id of the inserted row

    @classmethod
    def retrieve_one(cls, **data:dict):
        # using LIMIT 1 to fetch only one result, even if more than one thing matches
        query = f'''
                SELECT * FROM `{cls.table}`
                WHERE {cls.format_data(" AND ", data)}
                LIMIT 1;
                '''
        row = connectToMySQL(DB).query_db(query, data).fetchone() # returns a single row as a dictionary
        # check to make sure that a row was returned (its None if nothing matched, or False if the query fails)
        if row:
            # we once again see the ** operator
            # however this time it is doing the opposite action: taking a dictionary, and spreading it out into key word arguments
            return cls(**row)

    @classmethod
    def retrieve_all(cls, **data:dict):
        # only add a WHERE clause if data was provided
        query = f'''
                SELECT * FROM `{cls.table}`
                {"WHERE " + cls.format_data(" AND ", data) if data else ""};
                '''
        rows = connectToMySQL(DB).query_db(query, data).fetchall() # returns all matching rows as a list of dictionaries
        # list comprehension to generate a list of objects from the list of dictionaries
        # works similar to using .map in JS where you can iterate over a list, transform the data, and return a new list

        return [cls(**row) for row in rows if rows] 

    @classmethod
    def update(cls, id, **data:dict):
        # notice how id is seperated out from the rest of the data, this is so it's not included when formatting the set statement
        query = f'''
                UPDATE `{cls.table}`
                SET {cls.format_data(", ", data)} 
                WHERE `id`=%(id)s;
                '''
        # we add back in the id now that the query has been formatted properly, since it needs to be provided still for the where clause
        data['id'] = id
        # we also don't return anything as there is no data to return for update (or delete) operations
        connectToMySQL(DB).query_db(query, data)

    @classmethod
    def delete(cls, **data:dict):
        query = f'''
                DELETE FROM `{cls.table}`
                WHERE {cls.format_data(" AND ", data)};
                '''
        connectToMySQL(DB).query_db(query, data)