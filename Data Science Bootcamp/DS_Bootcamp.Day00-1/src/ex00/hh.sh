# /bin/sh


API_URL="https://api.hh.ru/vacancies"
USER_AGENT="my-app-sigfrydj@student.21-school.ru"

TEXT="$1"

if [ -z "$TEXT" ]; then
  echo "Please provide a vacancy name"
  exit 1
fi 

PAGE=0
PER_PAGE=20
TEXT=$(echo "$TEXT" | jq -sRr @uri) # string coding

QUERY_STRING="?page=$PAGE&per_page=$PER_PAGE&text=$TEXT"

curl -s "$API_URL$QUERY_STRING" -H "User-Agent: $USER_AGENT" | jq . > hh.json

if [ $? -ne 0 ]; then
  echo "Error fetching data"
  exit 1
fi 

echo "Data saved to hh.json"