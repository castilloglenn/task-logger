import os
import argparse
import sqlite3
from datetime import datetime

repo_path = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(repo_path, "worklog.db")
# db_path = os.path.join(repo_path, "worklog_test.db")


def log_entry(message, category):
    now = datetime.now()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(
        "INSERT INTO logs (timestamp, category, message) VALUES (?, ?, ?)",
        (now.isoformat(), category, message),
    )
    conn.commit()
    print(f"{category.upper()} logs for {now.strftime('%Y-%m-%d')}:")

    today = now.strftime("%Y-%m-%d")
    c.execute(
        "SELECT * FROM logs WHERE category = ? AND DATE(timestamp) = DATE(?)",
        (category, today),
    )
    logs = c.fetchall()

    # For displaying, get the total logs count and only show the latest max of 3 logs
    logs_count = len(logs)
    if logs_count > 3:
        logs = logs[-3:]
    print(f"Total logs: {logs_count}, the following is the latest three logs:")
    for log in logs:
        formatted_time = datetime.strptime(log[1], "%Y-%m-%dT%H:%M:%S.%f").strftime(
            "%I:%M:%S %p"
        )
        print(f"- [{formatted_time}] {log[3]}")

    conn.close()


def undo_last_entry():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM logs ORDER BY id DESC LIMIT 1")
    last_entry = c.fetchone()
    if last_entry:
        c.execute("DELETE FROM logs WHERE id = ?", (last_entry[0],))
        conn.commit()
        conn.close()
        print(f"Deleted last entry: {last_entry[1]}: {last_entry[3]}")
    else:
        conn.close()
        print("No logs to delete.")


def clear_db():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("DELETE FROM logs")
    conn.commit()
    conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Task Logger")
    parser.add_argument("command", type=str, help="The command to execute")
    parser.add_argument(
        "--category",
        type=str,
        default="general",
        help="The category of the log message",
    )
    parser.add_argument(
        "--message",
        type=str,
        help="The log message",
    )
    args = parser.parse_args()

    if args.command == "log":
        log_entry(args.message, args.category)
    elif args.command == "undo":
        undo_last_entry()
