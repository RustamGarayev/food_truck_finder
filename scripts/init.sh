#!/bin/sh

# Directory where the marker file is stored to ensure database is only populated once
MARKER_DIR=/persistent_data

# Ensure directory exists
mkdir -p $MARKER_DIR

# Run migrations
poetry run python manage.py migrate

# Path to the marker file
MARKER_FILE=$MARKER_DIR/db_populated.marker

# Check if database is populated
if [ ! -f "$MARKER_FILE" ]; then
    echo "Populating database..."
    poetry run python manage.py populate_database --path "$CSV_FILE_PATH"
    touch "$MARKER_FILE"
fi

# Start the Django server
poetry run python manage.py runserver 0.0.0.0:8000
