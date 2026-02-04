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

# lg() {
#     if [ -z "$1" ]; then
#         echo "Usage: lg <task>"
#         return 1
#     fi
#     task=$(__combine_args "$@")
#     python3 $task_logger_path/log.py log --message="$task"
# }

# lt() {
#     if [ -z "$1" ]; then
#         echo "Usage: lt <task>"
#         return 1
#     fi
#     task=$(__combine_args "$@")
#     python3 $task_logger_path/log.py log --category="team" --message="$task"
# }

lp() {
    if [ -z "$1" ]; then
        echo "Usage: lp <project>"
        return 1
    fi
    task=$(__combine_args "$@")
    python3 $task_logger_path/log.py log --category="project" --message="$task"

    # This requires the other repo shell-scripts to be set up
    commit $task
}

tundo() {
    python3 $task_logger_path/log.py undo
}

tdaily() {
    if [ "$1" = "show" ]; then
        python3 $task_logger_path/reports/daily.py --show-only
        return 0
    fi

    # tdaily -d 2025-03-10
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
        date=$(date +"%Y/%m/%d")
    fi

    echo "Category: $category"
    echo "Date: $date"

    python3 $task_logger_path/reports/daily.py --category="$category" --date="$date"
}

tweekly() {
    local date=""

    while getopts ":d:" opt; do
        case $opt in
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

    if [ -z "$date" ]; then
        date=$(date +"%Y/%m/%d")
    fi

    echo "Date: $date"

    python3 $task_logger_path/reports/weekly.py --date="$date"
}

tmonthly() {
    python3 $task_logger_path/reports/monthly.py
}

python3 $task_logger_path/backup.py
