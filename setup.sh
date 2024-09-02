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

tundo() {
    python3 $script_dir/log.py undo
}

tdaily() {
    if [ -z "$1" ]; then
        python3 $script_dir/reports/daily.py
    else
        python3 $script_dir/reports/daily.py --category="$1"
    fi
}

tweekly() {
    python3 $script_dir/reports/weekly.py
}

tmonthly() {
    python3 $script_dir/reports/monthly.py
}

printf "\033[1;32m[SUCCESS]\033[0m Task Logger setup complete. \033[1;90m(Location: $script_dir)\033[0m\n"
