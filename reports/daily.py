import os
import argparse
import sqlite3
from datetime import datetime

import pyperclip

repo_path = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(repo_path, "..", "worklog.db")


def daily_report(category=None):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    today = datetime.now().strftime("%Y-%m-%d")
    query = """
        SELECT * FROM logs
        WHERE DATE(timestamp) = DATE(?)
    """
    if category == "dcc":
        query += " AND category = 'dcc'"
    elif category == "shaver":
        query += (
            " AND (category = 'shaver' OR category = 'team' OR category = 'general')"
        )

    c.execute(query, (today,))

    logs = c.fetchall()

    category_str = category or "all categories"
    if len(logs) == 0:
        print(f"No logs found for {today} in {category_str}.")
        return

    print(f"Logs for {today} in {category_str}:")
    for log in logs:
        print(f"- {log[3]}")

    pyperclip.copy("\n".join([f"- {log[3]}" for log in logs]))
    print("Daily report copied to clipboard. Press Cmd+V to paste.")
    conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Daily Report")
    parser.add_argument("--category", type=str, help="The category of the log message")
    args = parser.parse_args()
    daily_report(args.category)
