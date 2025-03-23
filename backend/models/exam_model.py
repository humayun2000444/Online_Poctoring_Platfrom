from database.db import get_db_connection

def create_exam(title, description, date, duration, created_by):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO exams (title, description, date, duration, created_by)
        VALUES (%s, %s, %s, %s, %s)
    """, (title, description, date, duration, created_by))
    conn.commit()
    conn.close()

def get_all_exams():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM exams")
    exams = cursor.fetchall()
    conn.close()
    return exams
