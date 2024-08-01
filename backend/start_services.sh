start_infra_services() {
  docker-compose -f infra/docker-compose.yaml up -d
  sleep 8
}

start_backend_services() {
  docker-compose up --build
}

start_infra_services
start_backend_services

echo "Backend services are up and running."