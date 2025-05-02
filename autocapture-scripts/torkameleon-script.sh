#!/bin/bash

# Configuration
ITERATIONS=5
PROGRAM_DIRS=("Bridge" "Broker" "Client" "Proxy")
DELAY_BETWEEN=3          # seconds between launching programs
POST_RUN_DELAY=10         # seconds to wait after last program
INTERFACE="en0"         # Change this to your network interface

for (( i=1; i<=ITERATIONS; i++ ))
do
    echo "Iteration $i"

    # Start tshark in background
    PCAP_FILE="dtls_capture_$i.pcap"
    echo "Starting tshark capture to $PCAP_FILE..."
    tshark -i "$INTERFACE" -w "$PCAP_FILE" &
    TSHARK_PID=$!

    # Give tshark a moment to initialize
    sleep 2

    PIDS=()
    for dir in "${PROGRAM_DIRS[@]}"; do
        echo "Building and running $dir..."
        (
            cd "$dir" || exit
            go build .
            ./$(basename "$dir") &
            echo $! > "../$dir.pid"
        )
        PIDS+=("$(cat $dir.pid)")
        sleep "$DELAY_BETWEEN"
    done

    echo "All programs started. Waiting $POST_RUN_DELAY seconds..."
    sleep "$POST_RUN_DELAY"

    echo "Killing programs..."
    for pid in "${PIDS[@]}"; do
        kill "$pid" 2>/dev/null
    done

    echo "Stopping tshark..."
    kill "$TSHARK_PID" 2>/dev/null

    sleep 2
    echo "Iteration $i complete."
    echo "-------------------------"
done

