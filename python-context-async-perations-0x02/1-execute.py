import sqlite3
import os
print("Current working directory:", os.getcwd())

class ExecuteQuery:
    def __init__(self, query, params=()):
        self.query = query
        self.params = params
        self.conn = None
        self.results = None

    def __enter__(self):
        db_path = r'C:\Users\My Delight\Documents\alx-backend-python\python-context-async-perations-0x02\users.db'
        self.conn = sqlite3.connect(db_path)
        cursor = self.conn.cursor()
        cursor.execute(self.query, self.params)
        self.results = cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()

if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)
    with ExecuteQuery(query, params) as results:
        print(results)
