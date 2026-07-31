from database.connection import get_db_connection
from datetime import date

class PaymentDAO:
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

    def get_all_payments(self):
        conn = get_db_connection()
        payments = []
        if conn:
            try:
                cursor = conn.cursor(dictionary=True)
                id_col = self._get_id_col(cursor)
                
                cursor.execute("SHOW COLUMNS FROM members LIKE 'amount'")
                has_amount = bool(cursor.fetchone())

                cursor.execute("SHOW COLUMNS FROM members LIKE 'payment_date'")
                has_date = bool(cursor.fetchone())

                cursor.execute("SHOW COLUMNS FROM members LIKE 'payment_status'")
                has_status = bool(cursor.fetchone())

                amt_sel = "m.amount" if has_amount else "'1000' as amount"
                dt_sel = "m.payment_date" if has_date else "CURRENT_DATE() as payment_date"
                st_sel = "m.payment_status" if has_status else "'Paid' as status"

                query = f"""
                SELECT 
                    m.{id_col} as id,
                    m.name as member_name,
                    {amt_sel},
                    'Cash/UPI' as mode,
                    {dt_sel},
                    {st_sel}
                FROM members m
                ORDER BY m.{id_col} DESC
                """
                cursor.execute(query)
                payments = cursor.fetchall()
                cursor.close()
                conn.close()
            except Exception as e:
                print(f"Error fetching payments: {e}")
        return payments

    def add_payment(self, member_id, amount, mode, pay_date, status):
        conn = get_db_connection()
        if not conn:
            return False, "Database connection failed!"
        
        try:
            cursor = conn.cursor()
            id_col = self._get_id_col(cursor)
            
            for col, col_type in [('amount', 'VARCHAR(50) DEFAULT "1000"'), 
                                  ('payment_date', 'VARCHAR(50)'), 
                                  ('payment_status', 'VARCHAR(50) DEFAULT "Paid"')]:
                try:
                    cursor.execute(f"SHOW COLUMNS FROM members LIKE '{col}'")
                    if not cursor.fetchone():
                        cursor.execute(f"ALTER TABLE members ADD COLUMN {col} {col_type}")
                        conn.commit()
                except Exception:
                    pass

            query = f"UPDATE members SET amount=%s, payment_date=%s, payment_status=%s WHERE {id_col}=%s"
            cursor.execute(query, (amount, pay_date, status, member_id))

            conn.commit()
            cursor.close()
            conn.close()
            return True, "Payment recorded successfully!"
        except Exception as e:
            return False, f"Database Error: {e}"