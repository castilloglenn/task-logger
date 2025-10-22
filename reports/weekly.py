import os
import sqlite3
from datetime import datetime, timedelta

import pyperclip

repo_path = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(repo_path, "..", "worklog.db")


def weekly_report():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    today = datetime.now() - timedelta(days=1)
    if today.weekday() == 5:
        start_of_week = today
    else:
        start_of_week = today - timedelta(days=(today.weekday() + 2) % 7)

    end_of_week = start_of_week + timedelta(days=7)

    start_of_week_str = start_of_week.strftime("%Y-%m-%d 00:00:00")
    end_of_week_str = end_of_week.strftime("%Y-%m-%d 00:00:00")

    query = """
    SELECT * FROM logs
    WHERE timestamp BETWEEN ? AND ?
    """
    c.execute(query, (start_of_week_str, end_of_week_str))
    logs = c.fetchall()

    if len(logs) == 0:
        print("No logs found for the current week.")
        conn.close()
        return
    conn.close()

    # Group logs by day
    logs_by_day = {}
    for log in logs:
        raw_date = datetime.strptime(log[1], "%Y-%m-%dT%H:%M:%S.%f")
        day_key = raw_date.date()
        if day_key not in logs_by_day:
            logs_by_day[day_key] = []
        logs_by_day[day_key].append(log[3])

    # Format the report
    formatted_logs = []
    formatted_logs.append(
        "Hello everyone! I'd like to share my weekly task summary report!"
    )

    current_date = start_of_week.date()
    while current_date < end_of_week.date():
        # Skip Saturday and Sunday entirely if no logs exist for those days
        if current_date.weekday() in (5, 6) and current_date not in logs_by_day:
            current_date += timedelta(days=1)
            continue

        week_day = current_date.strftime("%A")
        formatted_logs.append(f"\nFor {week_day}:")

        if current_date in logs_by_day:
            for task in logs_by_day[current_date]:
                formatted_logs.append(f"  - {task}")
        else:
            default_logs = [
                "  - Continued working on several projects",
                "  - Code review, mentorship, and architecture planning",
                "  - Team meetings and collaboration",
            ]
            formatted_logs.extend(default_logs)

        current_date += timedelta(days=1)

    formatted_logs.append(
        "\nThat's all for this week! Looking forward to another productive week ahead. Thank you! 🙇🏻"
    )
    formatted_logs = "\n".join(formatted_logs)

    pyperclip.copy(formatted_logs.strip())
    print("Formatted report copied to clipboard (use Cmd+V to paste)")


if __name__ == "__main__":
    weekly_report()
