#!/bin/sh

input_file="../ex02/hh_sorted.csv"
output_file="hh_positions.csv"

if [ ! -f "$input_file" ]; then
  echo "[ERROR] The input file '$input_file' was not found."
  exit 1
fi

echo "[INFO] Starting the cleaning process."

echo '"id","created_at","name","has_test","alternate_url"' > "$output_file"
echo "[INFO] Header written to output file."

line_count=0
tail -n +2 "$input_file" | while IFS= read -r line; do
  line_count=$((line_count + 1))
  echo "[INFO] Processing line: $line_count"

  id=$(echo "$line" | sed -E 's/^"([^"]*)".*/\1/')
  created_at=$(echo "$line" | sed -E 's/^"[^"]*","([^"]*)".*/\1/')
  name=$(echo "$line" | sed -E 's/^"[^"]*","[^"]*","([^"]*)".*/\1/')
  has_test=$(echo "$line" | sed -E 's/^"[^"]*","[^"]*","[^"]*",([^,]*).*/\1/')
  alternate_url=$(echo "$line" | sed -E 's/^.*,("https:[^"]*")$/\1/')


  name=$(echo "$name" | sed 's/^"//;s/"$//') # deleting ""

  position="-"
  if echo "$name" | grep -q "Junior"; then
    position="Junior"
    echo "[INFO] Found position level: Junior"
  fi
  if echo "$name" | grep -q "Middle"; then
    position=$(echo "$position" | sed 's/-/Middle/;t;s/$/\/Middle/')
    echo "[INFO] Found position level: Middle"
  fi
  if echo "$name" | grep -q "Senior"; then
    position=$(echo "$position" | sed 's/-/Senior/;t;s/$/\/Senior/')
    echo "[INFO] Found position level: Senior"
  fi

  if [ "$position" = "-" ]; then
    echo "[INFO] No position level found for: $name"
  fi

  alternate_url=$(echo "$alternate_url" | sed 's/^"//;s/"$//')
  
  echo "\"$id\",\"$created_at\",\"$position\",\"$has_test\",\"$alternate_url\"" >> "$output_file"
done

echo "[INFO] Cleaning complete. Output written to '$output_file'."
