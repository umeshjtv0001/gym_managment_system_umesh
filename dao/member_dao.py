from database.connection import get_db_connection
from datetime import date

class MemberDAO:
    def __init__(self):
        pass

    def _get_id_col(self, cursor):
        try:
            cursor.execute("SHOW COLUMNS FROM members LIKE 'member_id'")
            if cursor.fetchone():
                return "member_id"
        except Exception:
            pass
        return "id"

    def get_all_members(self):
        conn = get_db_connection()
        members = []
        if conn:
            try:
                cursor = conn.cursor(dictionary=True)
                id_col = self._get_id_col(cursor)
                cursor.execute(f"SELECT *, {id_col} as id FROM members ORDER BY {id_col} DESC")
                members = cursor.fetchall()
                cursor.close()
                conn.close()
            except Exception as e:
                print(f"Error fetching members: {e}")
        return members

    def add_member(self, name, phone, gender, plan, payment_status="Paid", amount="1000", payment_date=None):
        if not payment_date:
            payment_date = str(date.today())

        conn = get_db_connection()
        if not conn:
            return False, "Database connection failed!"
            
        try:
            cursor = conn.cursor()
            # Dynamic Table columns handling
            cursor.execute("SHOW COLUMNS FROM members")
            cols = [col[0] for col in cursor.fetchall()]

            if 'amount' in cols and 'payment_date' in cols and 'payment_status' in cols:
                query = "INSERT INTO members (name, phone, gender, plan, payment_status, amount, payment_date) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(query, (name, phone, gender, plan, payment_status, amount, payment_date))
            elif 'payment_status' in cols:
                query = "INSERT INTO members (name, phone, gender, plan, payment_status) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(query, (name, phone, gender, plan, payment_status))
            else:
                query = "INSERT INTO members (name, phone, gender, plan) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (name, phone, gender, plan))

            conn.commit()
            cursor.close()
            conn.close()
            return True, "Member added successfully!"
        except Exception as e:
            return False, f"Database Error: {e}"

    def update_member(self, member_id, name, phone, gender, plan, payment_status="Paid", amount="1000", payment_date=None):
        if not payment_date:
            payment_date = str(date.today())

        conn = get_db_connection()
        if not conn:
            return False, "Database connection failed!"
        try:
            cursor = conn.cursor()
            id_col = self._get_id_col(cursor)
            query = f"UPDATE members SET name=%s, phone=%s, gender=%s, plan=%s WHERE {id_col}=%s"
            cursor.execute(query, (name, phone, gender, plan, member_id))

            conn.commit()
            cursor.close()
            conn.close()
            return True, "Member updated successfully!"
        except Exception as e:
            return False, f"Database Error: {e}"

    def delete_member(self, member_id):
        conn = get_db_connection()
        if not conn:
            return False, "Database connection failed!"
        try:
            cursor = conn.cursor()
            id_col = self._get_id_col(cursor)
            query = f"DELETE FROM members WHERE {id_col}=%s"
            cursor.execute(query, (member_id,))

            conn.commit()
            cursor.close()
            conn.close()
            return True, "Member deleted successfully!"
        except Exception as e:
            return False, f"Database Error: {e}"