
import sqlite3

DATABASE_NAME = "submissions.db"


def get_connection():
    """Create and return a database connection."""
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    """Create the submissions table if it does not exist."""
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            registration_number TEXT NOT NULL,
            assignment_title TEXT NOT NULL,
            submission_url TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def save_submission(student_name, registration_number,
                    assignment_title, submission_url):
    """Save a new assignment submission."""
    connection = get_connection()

    cursor = connection.execute("""
        INSERT INTO submissions (
            student_name,
            registration_number,
            assignment_title,
            submission_url
        )
        VALUES (?, ?, ?, ?)
    """, (
        student_name,
        registration_number,
        assignment_title,
        submission_url
    ))

    connection.commit()
    submission_id = cursor.lastrowid
    connection.close()

    return submission_id


def get_all_submissions():
    """Return all saved submissions."""
    connection = get_connection()

    submissions = connection.execute(
        "SELECT * FROM submissions ORDER BY id DESC"
    ).fetchall()

    connection.close()

    return [dict(submission) for submission in submissions]
