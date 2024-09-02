import os
import sqlite3

repo_path = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(repo_path, "worklog.db")


def init_db():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS
            logs
            (
                id INTEGER PRIMARY KEY,
                timestamp TEXT,
                category TEXT,
                message TEXT
            )
        """
    )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
