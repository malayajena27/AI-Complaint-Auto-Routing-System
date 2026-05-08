import sqlite3


def create_database():

    conn = sqlite3.connect(
        "complaints.db"
    )

    cursor = conn.cursor()

    # Officers Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS officers (
        officer_id TEXT PRIMARY KEY,
        name TEXT,
        department TEXT,
        skills TEXT,
        languages TEXT,
        region TEXT,
        workload INTEGER
    )
    """)

    # Complaints Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS complaints (
        complaint_id INTEGER PRIMARY KEY AUTOINCREMENT,
        complaint_text TEXT,
        language TEXT,
        input_type TEXT,
        priority TEXT,
        eta_days REAL,
        assigned_officer_id TEXT,
        status TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Similar Complaints Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS similar_complaints (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        complaint_id INTEGER,
        similar_complaint TEXT,
        similarity_score REAL
    )
    """)

    conn.commit()

    conn.close()

    print("Database and tables created successfully")


if __name__ == "__main__":
    create_database()