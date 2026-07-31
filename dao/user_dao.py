from database import connection
from database.connection import DBConnection
from models.user import User


class UserDAO:

    def __init__(self):
        pass

    def login(self, username, password):
        """
        Check username and password
        Returns User object if found else None
        """

        conn = DBConnection.get_connection()

        if conn is None:
            return None

        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT *
            FROM users
            WHERE username=%s AND password=%s
        """

        cursor.execute(query, (username, password))

        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if row:
            return User(
                user_id=row["id"],
                username=row["username"],
                password=row["password"]
            )

        return None

    def get_all_users(self):

        conn = DBConnection.get_connection()

        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users")

        rows = cursor.fetchall()

        users = []

        for row in rows:
            users.append(
                User(
                    user_id=row["id"],
                    username=row["username"],
                    password=row["password"]
                )
            )

        cursor.close()
        conn.close()

        return users

    def add_user(self, user):

        conn = DBConnection.get_connection()

        cursor = conn.cursor()

        query = """
            INSERT INTO users(username,password)
            VALUES(%s,%s)
        """

        cursor.execute(
            query,
            (user.username, user.password)
        )

        conn.commit()

        cursor.close()
        conn.close()

    def update_user(self, user):

        conn = DBConnection.get_connection()

        cursor = conn.cursor()

        query = """
            UPDATE users
            SET username=%s,
                password=%s
            WHERE id=%s
        """

        cursor.execute(
            query,
            (
                user.username,
                user.password,
                user.user_id
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

    def delete_user(self, user_id):

        conn = DBConnection.get_connection()

        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM users WHERE id=%s",
            (user_id,)
        )

        conn.commit()

        cursor.close()
        conn.close()