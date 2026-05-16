#!/bin/bash
set -e

if [ ! -f /app/search_topics.txt ]; then
    echo "ERROR: search_topics.txt not found."
    echo "Create it on the host and make sure it is bind-mounted."
    echo "Example: echo 'python scraping' > search_topics.txt"
    exit 1
fi

if [ -z "$DISPLAY" ]; then
    Xvfb :99 -screen 0 1920x1080x24 -ac &
    export DISPLAY=:99
fi

exec python main.py
