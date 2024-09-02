import os
import sqlite3
from datetime import datetime, timedelta

import pyperclip

repo_path = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(repo_path, "..", "worklog.db")


def create_list_of_logs(logs):
    return "\n".join([f"- {log[3]}" for log in logs]) + "\n\n"


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
    print(
        "Fetching logs between %s and %s"
        % (
            start_of_week.strftime(pretty_format),
            end_of_week.strftime(pretty_format),
        )
    )

    # Query from different tables
    query = """
    SELECT * FROM logs
    WHERE timestamp BETWEEN ? AND ?
    """
    c.execute(query, (start_of_week_str, end_of_week_str))
    logs = c.fetchall()

    general = []
    team = []
    dcc = []
    shaver = []
    for log in logs:
        category = log[2]
        if category == "general":
            general.append(log)
        elif category == "team":
            team.append(log)
        elif category == "dcc":
            dcc.append(log)
        elif category == "shaver":
            shaver.append(log)

    if len(logs) == 0:
        print("No logs found for the current week.")
        return
    conn.close()

    # Generate the report
    monday_of_week = (start_of_week + timedelta(days=1)).strftime(pretty_format)
    friday_of_week = (end_of_week - timedelta(days=1)).strftime(pretty_format)
    report = f"*Weekly Report ({monday_of_week} - {friday_of_week})*\n\n"
    if len(dcc) > 0:
        report += "*Disk Cassette Content Project*\n"
        report += create_list_of_logs(dcc)
    if len(shaver) > 0:
        report += "*Shaver Project*\n"
        report += create_list_of_logs(shaver)
    if len(team) > 0:
        report += "*Team*\n"
        report += create_list_of_logs(team)
    if len(general) > 0:
        report += "*Personal*\n"
        report += create_list_of_logs(general)

    # Display the report
    print("=" * 55)
    print(report)
    print("=" * 55 + "\n")

    # Copy the report to the clipboard
    pyperclip.copy(report)
    print("Weekly report copied to clipboard (use Cmd+V to paste)")


if __name__ == "__main__":
    weekly_report()
