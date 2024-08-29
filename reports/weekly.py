import os
import sqlite3
from datetime import datetime, timedelta

import pyperclip

repo_path = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(repo_path, "..", "worklog.db")


def weekly_report():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Calculate the start (Sunday) and end (Saturday) of the current week
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday() + 1)
    end_of_week = start_of_week + timedelta(days=6)

    # Format dates to match the timestamp format in the database
    start_of_week_str = start_of_week.strftime("%Y-%m-%d 00:00:00")
    end_of_week_str = end_of_week.strftime("%Y-%m-%d 23:59:59")
    pretty_format = "%B %d, %Y"
    start_pretty = start_of_week.strftime(pretty_format)
    end_pretty = end_of_week.strftime(pretty_format)
    print("Fetching logs between %s and %s" % (start_pretty, end_pretty))

    # Execute the query
    query = """
    SELECT * FROM logs
    WHERE timestamp BETWEEN ? AND ?
    """
    c.execute(query, (start_of_week_str, end_of_week_str))
    logs = c.fetchall()
    conn.close()

    # Generate the report
    header = f"*Weekly Report ({start_pretty} - {end_pretty})*\n"
    logs_list = "\n".join([f"- {log[2]}" for log in logs])
    report = header + logs_list

    # Copy the report to the clipboard
    pyperclip.copy(report)
    print("Weekly report copied to clipboard (use Cmd+V to paste)")


if __name__ == "__main__":
    weekly_report()
