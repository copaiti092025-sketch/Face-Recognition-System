import pickle
import numpy as np
from database import get_db_connection
from datetime import datetime

THRESHOLD = 0.6

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def mark_attendance(embedding):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, embedding FROM students")
    students = cursor.fetchall()

    for student_id, db_emb in students:
        db_emb = pickle.loads(db_emb)
        similarity = cosine_similarity(embedding, db_emb)

        if similarity > THRESHOLD:
            cursor.execute(
                "INSERT INTO attendance (student_id, date, time, status) VALUES (%s,%s,%s,%s)",
                (student_id, datetime.now().date(), datetime.now().time(), "Present")
            )
            conn.commit()
            conn.close()
            return student_id

    conn.close()
    return None
