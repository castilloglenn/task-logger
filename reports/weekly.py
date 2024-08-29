import os
import sqlite3

from datetime import datetime, timedelta

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
    print(
        "Fetching logs between %s and %s"
        % (
            start_of_week.strftime(pretty_format),
            end_of_week.strftime(pretty_format),
        )
    )

    # Execute the query
    query = """
    SELECT * FROM logs
    WHERE timestamp BETWEEN ? AND ?
    """
    c.execute(query, (start_of_week_str, end_of_week_str))

    logs = c.fetchall()
    print("Number of logs:", len(logs))

    conn.close()
    return logs


if __name__ == "__main__":
    weekly_report()