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

tl() {
    if [ -z "$1" ]; then
        echo "Usage: tl <task>"
        return 1
    fi
    task=$(__combine_args "$@")
    python3 $script_dir/log.py "$task"
}

tl_weeklyreport() {
    python3 $script_dir/reports/weekly.py
}

tl_monthlyreport() {
    python3 $script_dir/reports/monthly.py
}

printf "\033[1;32m[SUCCESS]\033[0m Task Logger setup complete. \033[1;90m(Location: $script_dir)\033[0m\n"
