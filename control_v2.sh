#!/bin/bash

# List of shell scripts to choose from
scripts=(
    "./slam.sh"
    "./slam_unity.sh"
    "./slam_ydlidar.sh"
    "./store_map.sh"
    "./localization.sh"
    "./localization_unity.sh"
    "./localization_ydlidar.sh"
    "./camera_astra.sh"
    "./camera_dabai.sh"
)

# Array to keep track of child process IDs
child_pids=()

# Function to display the menu
show_menu() {
    clear
    echo "Choose a script to run:"
    for i in "${!scripts[@]}"; do
        echo "$((i+1)). ${scripts[i]}"
    done
    echo "d. Shutdown all child processes"
    echo "q. Quit"
}

# Function to handle running the script
run_script() {
    local script=$1
    local print_logs=$2  # Boolean to control whether to print logs or not

    if [[ $print_logs == true ]]; then
        echo "Running $script with logs... Press 'b' to go back to menu without terminating, or 'q' to quit and terminate the process."
        (exec "$script") &
    else
        echo "Running $script without logs... Press 'b' to go back to menu without terminating, or 'q' to quit and terminate the process."
        (exec "$script") > /dev/null 2>&1 &
    fi
    script_pid=$!
    child_pids+=("$script_pid")

    # Wait for user to press 'q'
    while :; do
        read -n 1 input
        if [[ $input == "q" ]]; then
            echo -e "\nTerminating $script: $script_pid..."
            kill -SIGINT $script_pid
            wait $script_pid 2>/dev/null
            # Remove the process from child_pids array
            child_pids=("${child_pids[@]/$script_pid}")
            break
        elif [[ $input == "b" ]]; then
            echo -e "\nGoing back to the menu. The process $script: $script_pid will continue running."
            break
        fi
    done
}

# Function to shut down all child processes
shutdown_all_children() {
    if [[ ${#child_pids[@]} -eq 0 ]]; then
        echo "No child processes are running."
    else
        echo "Shutting down all child processes..."
        for pid in "${child_pids[@]}"; do
            echo "Terminating process: $pid"
            kill -SIGINT $pid
            wait $pid 2>/dev/null
        done
        child_pids=()
    fi
}

# Main loop
while true; do
    show_menu

    read -p "Enter your choice: " choice

    if [[ $choice == "q" ]]; then
        echo "Shutting down all child processes."
        shutdown_all_children
        echo "Exiting..."
        break
    elif [[ $choice == "d" ]]; then
        shutdown_all_children
    elif [[ $choice =~ ^[0-9]+$ ]] && (( choice >= 1 && choice <= ${#scripts[@]} )); then
        selected_script="${scripts[$((choice-1))]}"
        
        # Determine if we want to print logs (only for store_map.sh)
        if [[ $selected_script == "./store_map.sh" ]]; then
            run_script "$selected_script" true  # Print logs for store_map.sh
        else
            run_script "$selected_script" false  # Suppress logs for other scripts
        fi
    else
        echo "Invalid choice. Please try again."
    fi
    sleep 1
done
