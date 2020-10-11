import sqlite3

class Database():
    def __init__(self, db_name):
        # connect to db
        self.conn = sqlite3.connect(db_name)
        # create cursor
        self.cursor = self.conn.cursor()
        # sql-command
        sql = "CREATE TABLE IF NOT EXISTS book (id INTEGER PRIMARY KEY, title TEXT, author TEXT, year INTEGER, ISBN INTEGER)"
        # execute sql command
        self.cursor.execute(sql)
        # commit changes to db
        self.conn.commit()

    def insert(self, title, author, year, isbn):
        # sql-command
        sql = "INSERT INTO book VALUES (NULL, ?,?,?,?)" #NULL-value is placeholder for auto-incrementing "id"
        # execute sql command
        self.cursor.execute(sql, (title, author, year, isbn))
        # commit changes to db
        self.conn.commit()

    def view(self):
        # sql-command
        sql = "SELECT * FROM book" 
        # execute sql command
        self.cursor.execute(sql)
        # save results in variable
        result = self.cursor.fetchall()
        # return query results
        return result

    def search(self, title=None, author=None, year=None, isbn=None):
        # sql-command
        sql = "SELECT * FROM book WHERE title=? OR author=? OR year=? or ISBN=?" 
        # execute sql command
        self.cursor.execute(sql, (title, author, year, isbn))
        # save results in variable
        result = self.cursor.fetchall()
        # return query results
        return result

    def search_by_id(self, id):
        # sql-command
        sql = "SELECT * FROM book WHERE id=?" 
        # execute sql command
        self.cursor.execute(sql, (id,))
        # save results in variable --> only 1 result should be returned, so select first item in returned list
        result = self.cursor.fetchall()[0]
        # return query results
        return result

    def delete(self, id):
        # sql-command
        sql = "DELETE FROM book WHERE id=?" 
        # execute sql command
        self.cursor.execute(sql, (id,))
        # commit changes to db
        self.conn.commit()

    def update(self, id, title, author, year, isbn):
        # sql-command
        sql = "UPDATE book SET title=?, author=?, year=?, ISBN=? WHERE id =?" 
        # execute sql command
        self.cursor.execute(sql, (title, author, year, isbn, id))
        # commit changes to db
        self.conn.commit()

    def close(self):
        self.conn.close()

    # a destructor method - destroys all class instances when script is closed
    def __del__(self): #in case app is closed without hitting "close"-button
        self.conn.close()