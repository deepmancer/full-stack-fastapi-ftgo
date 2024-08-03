#!/bin/bash

API_URL="http://localhost:5540/api"

NETWORK_NAME="backend-network"
GATEWAY_IP=$(docker network inspect $NETWORK_NAME --format '{{range .IPAM.Config}}{{.Gateway}}{{end}}')

if [ -z "$GATEWAY_IP" ]; then
  echo "Failed to retrieve gateway IP for network $NETWORK_NAME. Exiting."
  exit 1
fi
echo "Gateway IP for network $NETWORK_NAME is $GATEWAY_IP"

SETTINGS_PAYLOAD='{
  "agreements": {
    "eula": true,
    "analytics": false,
    "notifications": false,
    "encryption": false
  }
}'

curl -X GET "${API_URL}/settings" \
    -H "Content-Type: application/json" \
    -d "$SETTINGS_PAYLOAD"

REDIS_INSTANCES=(
  "Gateway Redis|6490|gateway_password|gateway_redis"
  "User Redis|6235|user_password|user_redis"
  "Restaurant Redis|6236|restaurant_password|restaurant_redis"
  "Location Redis|6300|location_password|location_redis"
  "Order Redis|6301|order_password|order_redis"
)

add_redis_database() {
  local NAME=$1
  local PORT=$2
  local PASSWORD=$3
  local DB_NAME=$4

  echo "Adding Redis database: $NAME..."

  curl -s -X POST -H "Content-Type: application/json" \
    -d "{
      \"host\": \"${GATEWAY_IP}\",
      \"port\": ${PORT},
      \"password\": \"${PASSWORD}\",
      \"name\": \"${DB_NAME}\"
    }" \
    "${API_URL}/databases" > /dev/null

  if [ $? -eq 0 ]; then
    echo "Successfully added Redis database: $NAME"
  else
    echo "Failed to add Redis database: $NAME"
  fi
}

for redis in "${REDIS_INSTANCES[@]}"; do
  IFS='|' read -r REDIS_NAME REDIS_PORT REDIS_PASSWORD REDIS_DB_NAME <<< "$redis"
  add_redis_database "$REDIS_NAME" "$REDIS_PORT" "$REDIS_PASSWORD" "$REDIS_DB_NAME"
done

echo "Finished adding Redis databases."
