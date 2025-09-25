#!/bin/sh

FILTER_FILE="filter.jq"
JSON_FILE="../ex00/hh.json"
OUTPUT_FILE="hh.csv"

echo "Getting started with the script json_to_csv.sh..."
echo ""

if [ ! -f "$FILTER_FILE" ]; then
  echo "Error: filter file '$FILTER_FILE' not found"
  exit 1
fi

if [ ! -f "$JSON_FILE" ]; then
  echo "Error: JSON-file '$JSON_FILE' not found"
  exit 1
fi

echo "Adding headers to $OUTPUT_FILE..."
echo '"id","created_at","name","has_test","alternate_url"' > "$OUTPUT_FILE"

echo "Running jq with a filter from '$FILTER_FILE' to process the '$JSON_FILE' file..."
jq -r -f "$FILTER_FILE" "$JSON_FILE" >> "$OUTPUT_FILE"

if [ $? -ne 0 ]; then
  echo "Error: The jq command failed with an error."
  exit 1
fi

echo ""
echo "The script has been successfully completed. The result is saved in '$OUTPUT_FILE'."