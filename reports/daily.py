import os
import argparse
import sqlite3
from datetime import datetime

import pyperclip

repo_path = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(repo_path, "..", "worklog.db")


def format_logs_for_google_sheets(logs):
    num_logs = len(logs)
    if num_logs == 0:
        return ""

    num_cells = 8
    formatted_logs = []

    if num_logs < num_cells:
        # Calculate the repetition count for each log
        repetitions = [num_cells // num_logs] * num_logs
        extra_repeats = num_cells % num_logs

        # Distribute the remaining cells among the first few logs
        for i in range(extra_repeats):
            repetitions[i] += 1

        # Repeat the logs accordingly
        for i, count in enumerate(repetitions):
            formatted_logs.extend([logs[i]] * count)

    elif num_logs > num_cells:
        # Merge logs to fit into 8 cells
        merged_logs = []
        log_index = 0

        # Calculate how many logs to merge in the first few cells
        while len(merged_logs) < num_cells and log_index < num_logs:
            remaining_cells = num_cells - len(merged_logs)
            remaining_logs = num_logs - log_index
            merge_count = max(1, remaining_logs // remaining_cells)

            merged_log = "\n".join(logs[log_index : log_index + merge_count])
            merged_logs.append(f'"{merged_log}"')
            log_index += merge_count

        formatted_logs = merged_logs[:num_cells]

    else:
        # If the number of logs is exactly 8, just use them as is
        formatted_logs = logs

    # Add the blank cell in the 4th position
    formatted_logs.insert(3, "")

    return "\n".join(formatted_logs)


def daily_report(category, today):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    query = """
        SELECT * FROM logs
        WHERE DATE(timestamp) = DATE(?)
    """
    if category == "dcc":
        query += " AND category = 'dcc'"
    elif category == "ushi":
        query += " AND category = 'ushi'"
    elif category == "shaver":
        query += (
            " AND (category = 'shaver' OR category = 'team' OR category = 'general')"
        )

    c.execute(query, (today,))

    logs = c.fetchall()

    print("=" * 80)
    category_str = category or "all categories"
    if len(logs) == 0:
        print(f"No logs found for {today} in {category_str}.")
        return

    print(f"Logs for {today} in {category_str}:")
    for log in logs:
        raw_date = datetime.strptime(log[1], "%Y-%m-%dT%H:%M:%S.%f")
        formatted_date = raw_date.strftime("%I:%M %p")
        print(f"{formatted_date} - {log[3]}")

    logs_list = [log[3] for log in logs]
    google_sheets_format = format_logs_for_google_sheets(logs_list)

    print("=" * 80)
    print("Google Sheets format:")
    print(google_sheets_format)
    print("=" * 80)

    pyperclip.copy(google_sheets_format)
    print("Google Sheets format has been copied to clipboard. Press Cmd+V to paste.")
    conn.close()


if __name__ == "__main__":
    DATE_FMT = "%Y-%m-%d"
    parser = argparse.ArgumentParser(description="Daily Report")
    parser.add_argument(
        "--category",
        type=str,
        default="",
        help="The category of the log message",
    )
    parser.add_argument(
        "--date",
        type=str,
        default=datetime.now().strftime(DATE_FMT),
        help="The date of the log message",
    )
    args = parser.parse_args()

    try:
        date_ = args.date
        datetime.strptime(date_, DATE_FMT)
        daily_report(args.category, date_)
    except ValueError:
        print("Invalid date format. Please use the format YYYY-MM-DD.")
