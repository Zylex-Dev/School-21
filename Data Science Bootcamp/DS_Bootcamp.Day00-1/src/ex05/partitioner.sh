#!/bin/sh

input_file="../ex03/hh_positions.csv"


echo "Script Starting..."

if [ ! -f "$input_file" ]; then
  echo "[ERROR] The input file '$input_file' was not found."
  exit 1
else 
  echo "[INFO] Input file '$input_file' was found."
fi

echo "[INFO] Processing input file: $input_file"

header=$(head -n 1 "$input_file")
echo "[INFO] Header extracted: $header"

echo "[INFO] Extracting unique dates from the 'created_at' column..."
awk -F ',' 'NR > 1 {split($2, a, "T"); sub(/^"/, "", a[1]); print a[1]}' "$input_file" | uniq | while read date; do

  if [ -z "$date" ]; then
    echo "[WARNING] Encountered an empty date. Skipping..."
    continue
  fi 

  output_file="${date}.csv"
  echo "[INFO] Creating file for date: $date -> $output_file"

  echo "$header" > "$output_file"
  echo "[INFO] Header added to $output_file"

  echo "[INFO] Filtering rows for date: $date"
  tail -n +2 "$input_file" | awk -F ',' -v d="$date" '$2 ~d {print}' >> "$output_file"
  echo "[INFO] Rows for date $date added to $output_file"
done

echo "Script completed successfully..."
