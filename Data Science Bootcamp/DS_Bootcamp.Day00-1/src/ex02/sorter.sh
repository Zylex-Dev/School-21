#!/bin/sh

PROCESSED_FILE="../ex01/hh.csv"
OUTPUT_FILE="hh_sorted.csv"

echo "Starting the sorter.sh script..."
echo ""

if [ ! -f "$PROCESSED_FILE" ]; then
  echo "[ERROR] The CSV file '$PROCESSED_FILE' was not found. Please ensure the file exists and try again."
  exit 1
fi

echo "[INFO] Input file '$PROCESSED_FILE' found. Proceeding with sorting..."

header=$(head -n 1 "$PROCESSED_FILE")
if [ -z "$header" ]; then
  echo "[ERROR] The input file '$PROCESSED_FILE' is empty or does not contain a valid header."
  exit 1
fi

echo "[INFO] Header extracted successfully."

echo "[INFO] Sorting the file by 'created_at' (column 2) and then by 'id' (column 1)..."
tail -n +2 "$PROCESSED_FILE" | sort -t ',' -k2,2 -k1,1 -o "$OUTPUT_FILE"

if [ $? -ne 0 ]; then
  echo "[ERROR] Sorting failed. Please check the input file format and try again."
  exit 1
fi
echo "[INFO] Sorting completed successfully."

echo "[INFO] Adding the header back to the sorted file..."
echo "$header" | cat - "$OUTPUT_FILE" > temp_file && mv temp_file "$OUTPUT_FILE"

if [ $? -ne 0 ]; then
  echo "[ERROR] Failed to write the header to the sorted file."
  exit 1
fi
echo "[INFO] Header added successfully."

echo "[SUCCESS] Sorting process completed. The sorted file is saved as '$OUTPUT_FILE'."
