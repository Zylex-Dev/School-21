#!/bin/sh

input_file="../ex03/hh_positions.csv"
output_file="hh_uniq_positions.csv"

echo "Script started..."

if [ ! -f "$input_file" ]; then
  echo "[ERROR] The input file '$input_file' was not found."
  exit 1
else 
  echo "[INFO] Input file '$input_file' was found."
fi

echo "[INFO] Extracting unique positions and counts..."
# Extract the name column, count unique values, and sort by count
awk -F, 'NR > 1 {print $3}' "$input_file" | sort | uniq -c | sort -nr | \
# Format the output as CSV and add the header
awk 'BEGIN {print "\"name\",\"count\""} {print $2 "," $1}' > "$output_file"

if [ $? -eq 0 ]; then
  echo "[INFO] Data successfully processed and saved to '$output_file'."
else
  echo "[ERROR] Failed to process the data."
  exit 1
fi

echo "Script finished successfully..."

