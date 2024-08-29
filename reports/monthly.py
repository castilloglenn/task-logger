import os
import sqlite3
from datetime import datetime, timedelta

import pyperclip

repo_path = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(repo_path, "..", "worklog.db")


def monthly_report():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Calculate the start and end dates of the current month
    today = datetime.now()
    start_of_month = datetime(today.year, today.month, 1)
    end_of_month = datetime(today.year, (today.month + 1 % 12), 1) - timedelta(days=1)

    # Format dates to match the timestamp format in the database
    start_of_month_str = start_of_month.strftime("%Y-%m-%d 00:00:00")
    end_of_month_str = end_of_month.strftime("%Y-%m-%d 23:59:59")
    print("Fetching logs in %s" % end_of_month.strftime("%B, %Y"))

    # Execute the query
    query = """
    SELECT * FROM logs
    WHERE timestamp BETWEEN ? AND ?
    """
    c.execute(query, (start_of_month_str, end_of_month_str))
    logs = c.fetchall()
    print("Number of logs:", len(logs))
    conn.close()

    # Generate the report
    report = "\n".join([log[2] for log in logs])

    # Copy the report to the clipboard
    pyperclip.copy(report)
    print("Monthly report copied to clipboard (use Cmd+V to paste)")


if __name__ == "__main__":
    monthly_report()
