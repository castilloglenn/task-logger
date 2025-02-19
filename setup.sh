#!/bin/bash

# Get the directory of the current script
task_logger_path=$(dirname "$0")

__combine_args() {
    combined_string=""
    for arg in "$@"; do
        combined_string="${combined_string}${arg} "
    done
    combined_string=$(echo "$combined_string" | xargs)
    echo "$combined_string"
}

lg() {
    if [ -z "$1" ]; then
        echo "Usage: lg <task>"
        return 1
    fi
    task=$(__combine_args "$@")
    python3 $task_logger_path/log.py log --message="$task"
}

lt() {
    if [ -z "$1" ]; then
        echo "Usage: lt <task>"
        return 1
    fi
    task=$(__combine_args "$@")
    python3 $task_logger_path/log.py log --category="team" --message="$task"
}

lp() {
    if [ -z "$1" ]; then
        echo "Usage: lp <project>"
        return 1
    fi
    task=$(__combine_args "$@")
    python3 $task_logger_path/log.py log --category="project" --message="$task"
}

tundo() {
    python3 $task_logger_path/log.py undo
}

tdaily() {
    local category=""
    local date=""

    while getopts ":c:d:" opt; do
        case $opt in
            c)
                category=$OPTARG
                ;;
            d)
                date=$OPTARG
                ;;
            \?)
                echo "Invalid option: -$OPTARG" >&2
                return 1
                ;;
        esac
    done

    shift $((OPTIND - 1))

    # Provide default values if parameters are missing
    if [ -z "$category" ]; then
        category=""
    fi

    if [ -z "$date" ]; then
        date=$(date +"%Y-%m-%d")
    fi

    echo "Category: $category"
    echo "Date: $date"


    python3 $task_logger_path/reports/daily.py --category="$category" --date="$date"
}

tweekly() {
    python3 $task_logger_path/reports/weekly.py
}

tmonthly() {
    python3 $task_logger_path/reports/monthly.py
}

python3 $task_logger_path/backup.py
printf "\033[1;32m[SUCCESS]\033[0m Task Logger setup complete. \033[1;90m(Location: $task_logger_path)\033[0m\n"
