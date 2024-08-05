#!/bin/bash

# Metabase API details
METABASE_URL="http://localhost:3030/api"
METABASE_USERNAME="youremail"
METABASE_PASSWORD="yourpassword"

NETWORK_NAME="backend-network"
GATEWAY_IP=$(docker network inspect $NETWORK_NAME --format '{{range .IPAM.Config}}{{.Gateway}}{{end}}')

if [ -z "$GATEWAY_IP" ]; then
  echo "Failed to retrieve gateway IP for network $NETWORK_NAME. Exiting."
  exit 1
fi
echo "Gateway IP for network $NETWORK_NAME is $GATEWAY_IP"

# Database configurations with the gateway IP
DATABASES=(
  "User Database|$GATEWAY_IP|5438|user_database|user_user|user_password"
    "Restaurant Database|$GATEWAY_IP|5440|restaurant_database|restaurant_user|restaurant_password"
  "Location Database|$GATEWAY_IP|5439|location_database|location_user|location_password"
  "Order Database|$GATEWAY_IP|5432|order_database|order_user|order_password"
)

# Function to authenticate with Metabase and get a session token
authenticate_metabase() {
  echo "Attempting to authenticate with Metabase..."
  SESSION_ID=$(curl -s -X POST -H "Content-Type: application/json" \
    -d "{\"username\": \"${METABASE_USERNAME}\", \"password\": \"${METABASE_PASSWORD}\"}" \
    "${METABASE_URL}/session" | grep -o '"id":"[^"]*' | grep -o '[^"]*$')

  if [ -z "$SESSION_ID" ]; then
    echo "Failed to authenticate with Metabase. Exiting."
    exit 1
  else
    echo "Authenticated. Session ID: ${SESSION_ID}"
  fi
}


RETRY_COUNT=0
MAX_RETRIES=30
SLEEP_INTERVAL=5

# Function to add a database to Metabase
add_database() {
  local NAME=$1
  local HOST=$2
  local PORT=$3
  local DBNAME=$4
  local USER=$5
  local PASSWORD=$6

  echo "Adding database: $NAME..."

  curl -s -X POST -H "Content-Type: application/json" -H "X-Metabase-Session: ${SESSION_ID}" \
    -d "{
      \"name\": \"${NAME}\",
      \"engine\": \"postgres\",
      \"details\": {
        \"host\": \"${HOST}\",
        \"port\": ${PORT},
        \"dbname\": \"${DBNAME}\",
        \"user\": \"${USER}\",
        \"password\": \"${PASSWORD}\"
      }
    }" \
    "${METABASE_URL}/database" > /dev/null

  if [ $? -eq 0 ]; then
    echo "Successfully added database: $NAME"
  else
    echo "Failed to add database: $NAME"
  fi
}


authenticate_metabase

# Loop through each database configuration and add it to Metabase
for db in "${DATABASES[@]}"; do
  IFS='|' read -r DB_NAME DB_HOST DB_PORT DB_DBNAME DB_USER DB_PASSWORD <<< "$db"
  add_database "$DB_NAME" "$DB_HOST" "$DB_PORT" "$DB_DBNAME" "$DB_USER" "$DB_PASSWORD"
done

echo "Finished adding databases."
