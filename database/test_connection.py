import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="umesh2008",
        database="gym_managment",
        port=3306
    )

    print("✅ Connected Successfully")

except Exception as e:
    print("❌ Error:", e)