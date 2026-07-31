import mysql.connector
from mysql.connector import Error

def get_db_connection():
    """Database connection return karta hai."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",          # Apka MySQL username
            password="umesh2008",          # Apka MySQL password (agar hai to likhein)
            database="gym_db"     # Apka Database Name
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Database Connection Error: {e}")
        return None

# Class version (agar kisi aur file me use ho raha ho)
class DatabaseConnection:
    @staticmethod
    def get_connection():
        return get_db_connection()

if __name__ == "__main__":
    conn = get_db_connection()
    if conn:
        print("Database connected successfully!")
        conn.close()
    else:
        print("Failed to connect to Database.")