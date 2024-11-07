import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Database configuration from environment variables
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "your_database_name")

class DB:
    def __init__(self):
        self.conn = None
        try:
            # Initialize the connection
            self.conn = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASS,
                database=DB_NAME
            )
            if self.conn.is_connected():
                print("Connected to DB.")
        except Error as e:
            print(f"Connection error: {e}")

    def exec(self, query, params=None):
        """Execute a query with optional parameters and commit changes."""
        try:
            cur = self.conn.cursor()
            cur.execute(query, params)
            self.conn.commit()
            print("Query executed.")
        except Error as e:
            print(f"Execution error: {e}")
            raise e
        finally:
            cur.close()

    def fetch(self, query, params=None):
        """Fetch results from a SELECT query."""
        results = None
        try:
            cur = self.conn.cursor(dictionary=True)
            cur.execute(query, params)
            results = cur.fetchall()
        except Error as e:
            print(f"Fetch error: {e}")
        finally:
            cur.close()
        return results

    def close(self):
        """Close the DB connection."""
        if self.conn.is_connected():
            self.conn.close()
            print("DB connection closed.")


db = DB()
