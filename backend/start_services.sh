stop_containers() {
  echo "Stopping containers and removing orphans..."
  docker-compose down --remove-orphans
}

free_ports() {
  ports=(15920 5920 6490 5438 6235 8000 5020)
  for port in "${ports[@]}"; do
    echo "Freeing up port $port..."
    sudo kill -9 $(sudo lsof -t -i:$port) 2>/dev/null
  done
}

start_containers() {
  echo "Starting containers..."
  docker-compose up --build -d
}

stop_containers
free_ports
start_containers

echo "Backend services are up and running."