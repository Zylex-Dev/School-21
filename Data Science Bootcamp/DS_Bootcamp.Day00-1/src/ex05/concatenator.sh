#!/bin/sh

output_file="combined.csv"
input_folder="."

csv_files=$(find "$input_folder" -type f -name "*.csv" ! -name "$output_file" | sort)
if [ -z "$csv_files" ]; then
  echo "[ERROR] No CSV files found in folder"
  exit 1
else 
  echo "[INFO] Found the following files to concatenate:"
  echo "$csv_files"
fi

header=$(head -n 1 $(echo "$csv_files" | head -n 1))
echo "[INFO] Extracted header: $header"

echo "$header" > "$output_file"
echo "[INFO] Header written to $output_file"

for file in $csv_files; do
  echo "[INFO] Adding data from $file"
  tail -n +2 "$file" >> "$output_file"
done

echo "[INFO] Concatenation completed. Result saved to $output_file"