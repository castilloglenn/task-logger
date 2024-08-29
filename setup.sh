#!/bin/bash

printf "\033[1;34m[INFO]\033[0m Setting up Task Logger..."

script_dir=$(dirname "$0")
printf "\n\033[1;34m[INFO]\033[0m Script directory: \033[1m%s\033[0m\n" "$script_dir"

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

printf "\033[1;32m[SUCCESS]\033[0m Task Logger setup complete.\n\n"
