#!/bin/bash

# Get the directory of the current script
script_dir=$(dirname "$0")

__combine_args() {
    combined_string=""
    for arg in "$@"; do
        combined_string="${combined_string}${arg} "
    done
    combined_string=$(echo "$combined_string" | xargs)
    echo "$combined_string"
}

tgen() {
    if [ -z "$1" ]; then
        echo "Usage: tgen <task>"
        return 1
    fi
    task=$(__combine_args "$@")
    python3 $script_dir/log.py log --message="$task"
}

ttea() {
    if [ -z "$1" ]; then
        echo "Usage: ttea <task>"
        return 1
    fi
    task=$(__combine_args "$@")
    python3 $script_dir/log.py log --category="team" --message="$task"
}

tdcc() {
    if [ -z "$1" ]; then
        echo "Usage: tdcc <task>"
        return 1
    fi
    task=$(__combine_args "$@")
    python3 $script_dir/log.py log --category="dcc" --message="$task"
}

tsha() {
    if [ -z "$1" ]; then
        echo "Usage: tsha <task>"
        return 1
    fi
    task=$(__combine_args "$@")
    python3 $script_dir/log.py log --category="shaver" --message="$task"
}

tushi() {
    if [ -z "$1" ]; then
        echo "Usage: tushi <task>"
        return 1
    fi
    task=$(__combine_args "$@")
    python3 $script_dir/log.py log --category="ushi" --message="$task"
}

tundo() {
    python3 $script_dir/log.py undo
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


    python3 $script_dir/reports/daily.py --category="$category" --date="$date"
}

tweekly() {
    python3 $script_dir/reports/weekly.py
}

tmonthly() {
    python3 $script_dir/reports/monthly.py
}

python3 $script_dir/backup.py
printf "\033[1;32m[SUCCESS]\033[0m Task Logger setup complete. \033[1;90m(Location: $script_dir)\033[0m\n"
