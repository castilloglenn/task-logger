import os
import time
import argparse
import sqlite3
from datetime import datetime

import pyautogui
import pyperclip


repo_path = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(repo_path, "..", "worklog.db")
# db_path = os.path.join(repo_path, "..", "worklog_test.db")

WAIT_TIME = 3


def format_logs_for_auto_pasting(logs, show_only=False):
    num_logs = len(logs)
    if num_logs == 0:
        print("No logs to paste.")
        return None

    num_cells = 8
    formatted_logs = []

    if num_logs < num_cells:
        repetitions = [num_cells // num_logs] * num_logs
        extra_repeats = num_cells % num_logs

        for i in range(extra_repeats):
            repetitions[i] += 1

        for i, count in enumerate(repetitions):
            formatted_logs.extend([logs[i]] * count)

    elif num_logs > num_cells:
        merged_logs = []
        log_index = 0

        while len(merged_logs) < num_cells and log_index < num_logs:
            remaining_cells = num_cells - len(merged_logs)
            remaining_logs = num_logs - log_index
            merge_count = max(1, remaining_logs // remaining_cells)

            merged_log = "\n".join(logs[log_index : log_index + merge_count])
            merged_logs.append(merged_log)
            log_index += merge_count

        formatted_logs = merged_logs[:num_cells]

    else:
        formatted_logs = logs

    if show_only:
        time_slots = [
            "9:00AM-10:00AM",
            "10:00AM-11:00AM",
            "11:00AM-12:00PM",
            "1:00PM-2:00PM",
            "2:00PM-3:00PM",
            "3:00PM-4:00PM",
            "4:00PM-5:00PM",
            "5:00PM-6:00PM",
        ]
        print()
        for i, log in enumerate(formatted_logs, start=0):
            if i < len(time_slots):
                print(f"{time_slots[i]}\n{log}\n")
        return

    print("Move cursor to HRIS daily report and focus on 9-10 AM field.")
    print(f"You have {WAIT_TIME} seconds to move the cursor.")
    print("Press Ctrl+C to cancel.")

    t = WAIT_TIME
    while t > 0:
        print(f" {t}...", end="\r")
        time.sleep(1)
        t -= 1

    for log in formatted_logs:
        pyperclip.copy(log)

        pyautogui.keyDown("command")
        pyautogui.press("v")
        pyautogui.keyUp("command")

        pyautogui.press("tab")
    pyautogui.press("tab")
    pyautogui.press("tab")

    print("Done pasting logs.")


def daily_report(category, today, show_only=False):
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
    try:
        c.execute(query, (today.replace("/", "-"),))

        logs = c.fetchall()

        category_str = category or "all categories"
        if len(logs) == 0:
            print(f"No logs found for {today} in {category_str}.")
            return

        print(f"Logs have a total of {len(logs)} entries.")

        logs_list = [log[3] for log in logs]
        format_logs_for_auto_pasting(logs_list, show_only)
    finally:
        conn.close()


if __name__ == "__main__":
    DATE_FMT = "%Y/%m/%d"
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
    parser.add_argument(
        "--show-only",
        action="store_true",
        help="Show the formatted logs without auto-pasting",
    )
    args = parser.parse_args()

    try:
        date_ = args.date
        datetime.strptime(date_, DATE_FMT)
        daily_report(args.category, date_, args.show_only)
    except ValueError:
        print("Invalid date format. Please use the format YYYY-MM-DD.")
