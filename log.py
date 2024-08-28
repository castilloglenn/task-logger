import os

import sqlite3
from datetime import datetime
from datetime import timedelta

repo_path = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(repo_path, "worklog.db")


def log_entry_for_the_day_each_work_hours_random_entry():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    days = 3
    hours = 8
    for day in range(days):
        for hour in range(1, hours):
            c.execute(
                "INSERT INTO logs (timestamp, message) VALUES (?, ?)",
                (
                    (
                        datetime.now() - timedelta(days=day, hours=hours - hour)
                    ).isoformat(),
                    f"Worked for {hour} hours",
                ),
            )
            conn.commit()
    conn.close()


def log_entry(message):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(
        "INSERT INTO logs (timestamp, message) VALUES (?, ?)",
        (datetime.now().isoformat(), message),
    )
    conn.commit()
    conn.close()


def delete_entry(id_):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("DELETE FROM logs WHERE id = ?", (id_,))
    conn.commit()
    conn.close()


def clear_db():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("DELETE FROM logs")
    conn.commit()
    conn.close()


if __name__ == "__main__":
    log_entry_for_the_day_each_work_hours_random_entry()
