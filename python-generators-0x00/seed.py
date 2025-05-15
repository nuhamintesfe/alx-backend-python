import mysql.connector
import csv
import uuid

def connect_db():
    """Connect to MySQL server (no specific database)"""
    try:
        connection = mysql.connector.connect(
            host="localhost", 
            user="root",       
            password=""      
        )
        print("Connected to MySQL server")
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL server: {err}")
        return None

def create_database(connection):
    """Create ALX_prodev database if not exists"""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        print("Database ALX_prodev created or already exists")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")

def connect_to_prodev():
    """Connect to ALX_prodev database"""
    try:
        connection = mysql.connector.connect(
            host="localhost",  
            user="root",      
            password="",       
            database='ALX_prodev'
        )
        print("Connected to ALX_prodev database")
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to ALX_prodev: {err}")
        return None

def create_table(connection):
    """Create user_data table if it doesn't exist"""
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL,
            INDEX(user_id)
        );
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("Table user_data created or already exists")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")

def insert_data(connection, filename):
    cursor = connection.cursor()
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cursor.execute("SELECT 1 FROM user_data WHERE user_id = %s", (row['user_id'],))
            if cursor.fetchone():
                continue
            cursor.execute(
                "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                (row['user_id'], row['name'], row['email'], int(row['age']))
            )
    connection.commit()
    cursor.close()

def insert_data(connection, filename):
    cursor = connection.cursor()
    try:
        with open(filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Generate a unique user_id for each row
                user_id = str(uuid.uuid4())

                try:
                    cursor.execute(
                        "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                        (user_id, row['name'], row['email'], int(row['age']))
                    )
                except Exception as e:
                    print(f"Error inserting row {row}: {e}")

        connection.commit()
        print("Data inserted successfully")
    except Exception as e:
        print(f"Error reading file or inserting data: {e}")
    finally:
        cursor.close()

if __name__ == "__main__":
    conn = connect_db()
    if conn:
        create_database(conn)
        conn.close()

        conn = connect_to_prodev()
        if conn:
            create_table(conn)
            insert_data(conn, 'user_data.csv')
            conn.close()
