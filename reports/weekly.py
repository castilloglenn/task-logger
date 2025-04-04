import os
import sqlite3
from datetime import datetime, timedelta

import pyperclip
import google.generativeai as genai
from dotenv import load_dotenv

repo_path = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(repo_path, "..", "worklog.db")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, "..", ".env"))

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)


def summarize(data):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt_format = ""
    prompt_path = os.path.join(BASE_DIR, "prompt.txt")
    with open(prompt_path, "r", encoding="utf-8") as file:
        prompt_format = file.read()
    if not prompt_format:
        return "Error: Prompt format not found.", 500

    try:
        prompt = prompt_format.format(data_=data)
        response = model.generate_content(prompt)
        text = response.text.strip()
        separator = "=" * 80
        print(f"GENERATED SUMMARY\n{separator}\n{text}\n{separator}\n")
        return response.text, 200
    except Exception as e:
        return f"An error occurred: {e}", 500


def weekly_report():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    today = datetime.now()
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

    formatted_logs = []
    for log in logs:
        raw_date = datetime.strptime(log[1], "%Y-%m-%dT%H:%M:%S.%f")
        week_day = raw_date.strftime("%A")
        formatted_logs.append(f"{week_day} - {log[3]}")
    formatted_logs = "\n".join(formatted_logs)

    summary, status_code = summarize(formatted_logs)
    if status_code != 200:
        print("Error generating summary:", summary)
        return

    pyperclip.copy(summary.strip())
    print("Summarized report copied to clipboard (use Cmd+V to paste)")


if __name__ == "__main__":
    weekly_report()
