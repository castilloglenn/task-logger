import shutil
import os
import datetime

repo_path = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(repo_path, "worklog.db")


def backup_database():
    current_datetime = datetime.datetime.now()
    previous_datetime = current_datetime - datetime.timedelta(days=1)

    date_format = "%Y%m%d"
    current_str = current_datetime.strftime(date_format)
    previous_str = previous_datetime.strftime(date_format)

    backup_dir = os.path.join(repo_path, "backups")
    os.makedirs(backup_dir, exist_ok=True)

    current_backup_dir = os.path.join(backup_dir, f"backup_{current_str}.db")
    previous_backup_dir = os.path.join(backup_dir, f"backup_{previous_str}.db")

    if not os.path.exists(current_backup_dir):
        shutil.copy(db_path, current_backup_dir)
        if os.path.exists(previous_backup_dir):
            os.remove(previous_backup_dir)


if __name__ == "__main__":
    backup_database()
