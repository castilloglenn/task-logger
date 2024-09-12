import os
import sqlite3
from datetime import datetime, timedelta
from dataclasses import dataclass

import pyperclip

repo_path = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(repo_path, "..", "worklog.db")


@dataclass
class Task:
    status: str
    assigned_date: datetime
    finished_date: datetime
    start_time: datetime
    end_time: datetime
    estimated_duration: float
    actual_duration: float
    description: str
    completion_grade: str
    estimated_hours: float
    actual_hours: float

    def __str__(self):
        date_format = "%m/%d/%Y"
        hours_format = "%I:%M %p"
        line = "\t".join(
            [
                self.status,
                self.assigned_date.strftime(date_format),
                self.finished_date.strftime(date_format),
                self.start_time.strftime(hours_format),
                self.end_time.strftime(hours_format),
                str(self.estimated_duration),
                str(self.actual_duration),
                self.description,
                self.completion_grade,
                str(self.estimated_hours),
                str(self.actual_hours),
            ]
        )
        return line + "\n"


def calculate_total_work_hours_in_month():
    # Get the current date
    today = datetime.today()

    # Get the first day of the month and the next month's first day
    first_day_of_month = today.replace(day=1)
    next_month = first_day_of_month.replace(month=today.month % 12 + 1, day=1)

    # Calculate the total number of days in the current month
    total_days_in_month = (next_month - first_day_of_month).days

    # Initialize work hours
    total_work_hours = 0

    # Iterate through each day in the current month
    for day in range(total_days_in_month):
        current_day = first_day_of_month + timedelta(days=day)
        if current_day.weekday() < 5:  # Monday to Friday are counted as workdays
            total_work_hours += 8

    return total_work_hours


def is_weekday(date):
    return date.weekday() < 5  # Monday is 0 and Sunday is 6


def get_next_available_slot(start_datetime):
    if start_datetime.hour < 9:
        start_datetime = start_datetime.replace(
            hour=9, minute=0, second=0, microsecond=0
        )
    elif 12 <= start_datetime.hour < 13:
        start_datetime = start_datetime.replace(
            hour=13, minute=0, second=0, microsecond=0
        )
    elif start_datetime.hour >= 18:
        start_datetime = start_datetime + timedelta(days=1)
        start_datetime = start_datetime.replace(
            hour=9, minute=0, second=0, microsecond=0
        )

    # Ensure the start_datetime is a weekday
    while not is_weekday(start_datetime):
        start_datetime += timedelta(days=1)
        start_datetime = start_datetime.replace(
            hour=9, minute=0, second=0, microsecond=0
        )

    return start_datetime


def monthly_report():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Calculate the start and end dates of the current month
    today = datetime.now()
    start_of_month = datetime(today.year, today.month, 1)
    # Ensure start date is a valid weekday
    if not is_weekday(start_of_month):
        while not is_weekday(start_of_month):
            start_of_month += timedelta(days=1)

    end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(
        days=1
    )

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
    if len(logs) == 0:
        print("No logs found in the current month.")
        return
    conn.close()

    # Calculate total work hours in the month
    hours_worked = calculate_total_work_hours_in_month()

    # Calculate duration per log
    log_size = len(logs)
    duration_per_log = (
        timedelta(hours=hours_worked / log_size) if log_size > 0 else timedelta(hours=0)
    )

    # Generate the report
    report = ""
    start_time = start_of_month.replace(hour=9, minute=0, second=0, microsecond=0)
    excess_time = timedelta(hours=0)

    for log in logs:
        task_start = get_next_available_slot(start_time)
        task_end = task_start + duration_per_log + excess_time
        if 12 <= task_end.hour < 13:
            excess_time = task_end - task_end.replace(hour=12, minute=0, second=0)
            task_end = task_end.replace(hour=12, minute=0, second=0)
        elif task_end.hour >= 18:
            excess_time = task_end - task_end.replace(hour=18, minute=0, second=0)
            task_end = task_end.replace(hour=18, minute=0, second=0)
        elif task_start.hour < 12 and task_end.hour >= 13:
            excess_time = timedelta(hours=1)
        else:
            excess_time = timedelta(hours=0)

        duration = None
        if task_start.hour < 12 and task_end.hour >= 13:
            before_lunch = task_start.replace(hour=12, minute=0, second=0) - task_start
            after_lunch = task_end - task_end.replace(hour=13, minute=0, second=0)
            duration = (before_lunch + after_lunch).total_seconds() / 3600
        else:
            duration = (task_end - task_start).total_seconds() / 3600

        # Create a Task object
        task = Task(
            status="Complete",
            assigned_date=task_start,
            finished_date=task_end,
            start_time=task_start,
            end_time=task_end,
            estimated_duration=duration / 8,
            actual_duration=duration / 8,
            description=log[3],
            completion_grade="100.00%",
            estimated_hours=duration,
            actual_hours=duration,
        )

        report += str(task)
        start_time = task_end

    # Copy the report to the clipboard
    pyperclip.copy(report)
    print("Monthly report copied to clipboard (use Cmd+V to paste)")


if __name__ == "__main__":
    monthly_report()
