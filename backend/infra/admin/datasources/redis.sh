now, provide the "About" and README.md part for the repository of redisinsight-docker-autoconfig with the following docker compose and add_datasource.sh:

#!/bin/bash

# Constants
API_URL="http://localhost:5540/api"
NETWORK_NAME="backend-network"

# Retrieve the gateway IP for the Docker network
GATEWAY_IP=$(docker network inspect "$NETWORK_NAME" --format '{{range .IPAM.Config}}{{.Gateway}}{{end}}')

GATEWAY_IP=$(docker network inspect "$NETWORK_NAME" --format '{{range .IPAM.Config}}{{.Gateway}}{{end}}')

# Check if gateway IP was successfully retrieved
if [ -z "$GATEWAY_IP" ]; then
  echo "Warning: Unable to retrieve gateway IP for network '$NETWORK_NAME'. Using 127.0.0.1 as the default."
  GATEWAY_IP="127.0.0.1"
fi

echo "Gateway IP for network '$NETWORK_NAME' is $GATEWAY_IP"

# Initial RedisInsight settings payload
SETTINGS_PAYLOAD='{
  "agreements": {
    "eula": true,
    "analytics": false,
    "notifications": false,
    "encryption": false
  }
}'

# Apply settings to RedisInsight
curl -X GET "${API_URL}/settings" \
     -H "Content-Type: application/json" \
     -d "$SETTINGS_PAYLOAD" > /dev/null 2>&1

# Redis instances configuration
REDIS_INSTANCES=(
  "Gateway Redis|6490|gateway_password|gateway_redis"
  "User Redis|6235|user_password|user_redis"
  "Restaurant Redis|6236|restaurant_password|restaurant_redis"
  "Location Redis|6300|location_password|location_redis"
  "Order Redis|6301|order_password|order_redis"
)

# Function to add a Redis database to RedisInsight
add_redis_database() {
  local NAME=$1
  local PORT=$2
  local PASSWORD=$3
  local DB_NAME=$4

  echo "Adding Redis database: $NAME..."

  curl -s -X POST "${API_URL}/databases" \
       -H "Content-Type: application/json" \
       -d "{
            \"host\": \"${GATEWAY_IP}\",
            \"port\": ${PORT},
            \"password\": \"${PASSWORD}\",
            \"name\": \"${DB_NAME}\"
          }" > /dev/null

  if [ $? -eq 0 ]; then
    echo "Successfully added Redis database: $NAME"
  else
    echo "Error: Failed to add Redis database: $NAME"
  fi
}

# Iterate over the Redis instances and add them to RedisInsight
for redis in "${REDIS_INSTANCES[@]}"; do
  IFS='|' read -r REDIS_NAME REDIS_PORT REDIS_PASSWORD REDIS_DB_NAME <<< "$redis"
  add_redis_database "$REDIS_NAME" "$REDIS_PORT" "$REDIS_PASSWORD" "$REDIS_DB_NAME"
done

echo "All Redis databases have been added successfully."