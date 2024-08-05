#!/bin/bash

# Metabase API details
METABASE_URL="http://localhost:3030/api"
METABASE_USERNAME="youremail"
METABASE_PASSWORD="yourpassword"

NETWORK_NAME="backend-network"
# Retrieve the gateway IP for the Docker network
GATEWAY_IP=$(docker network inspect "$NETWORK_NAME" --format '{{range .IPAM.Config}}{{.Gateway}}{{end}}')

# Set to 127.0.0.1 if gateway IP is not available
if [ -z "$GATEWAY_IP" ]; then
  GATEWAY_IP="127.0.0.1"
  echo "Gateway IP for network $NETWORK_NAME not found. Using default IP $GATEWAY_IP."
else
  echo "Gateway IP for network $NETWORK_NAME is $GATEWAY_IP"
fi

# Database configurations: NAME|NETWORK_IP|PORT|DB_NAME|USER|PASSWORD
DATABASES=(
  "User Database|$GATEWAY_IP|5438|user_database|user_user|user_password"
  "Restaurant Database|$GATEWAY_IP|5440|restaurant_database|restaurant_user|restaurant_password"
  "Location Database|$GATEWAY_IP|5439|location_database|location_user|location_password"
)

# Function to authenticate with Metabase and retrieve a session token
authenticate_metabase() {
  echo "Authenticating with Metabase..."
  SESSION_ID=$(curl -s -X POST -H "Content-Type: application/json" \
    -d "{\"username\": \"${METABASE_USERNAME}\", \"password\": \"${METABASE_PASSWORD}\"}" \
    "${METABASE_URL}/session" | jq -r '.id')

  if [ -z "$SESSION_ID" ]; then
    echo "Authentication failed. Exiting."
    exit 1
  fi

  echo "Authenticated successfully. Session ID: ${SESSION_ID}"
}

# Function to add a database to Metabase
add_database() {
  local NAME=$1
  local HOST=$2
  local PORT=$3
  local DBNAME=$4
  local USER=$5
  local PASSWORD=$6

  echo "Adding database: $NAME..."
  
  RESPONSE=$(curl -s -X POST -H "Content-Type: application/json" -H "X-Metabase-Session: ${SESSION_ID}" \
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
    "${METABASE_URL}/database")

  if echo "$RESPONSE" | jq -e '.id' >/dev/null; then
    echo "Database '$NAME' added successfully."
  else
    echo "Failed to add database '$NAME'. Response: $RESPONSE"
  fi
}

# Main script execution
authenticate_metabase

for db in "${DATABASES[@]}"; do
  IFS='|' read -r DB_NAME DB_HOST DB_PORT DB_DBNAME DB_USER DB_PASSWORD <<< "$db"
  add_database "$DB_NAME" "$DB_HOST" "$DB_PORT" "$DB_DBNAME" "$DB_USER" "$DB_PASSWORD"
done

echo "Finished adding databases."