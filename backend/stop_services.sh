stop_containers() {
  echo "Stopping containers and removing orphans..."
  docker-compose down --remove-orphans
  sleep 0.1
  docker stop `docker ps -qa`
  sleep 0.1
  docker rm -f `docker ps -qa`
  sleep 0.1
  sudo systemctl restart docker.socket docker.service docker
}

free_ports() {
  ports=(15920 5920 6490 5438 6235 8000 5020 5920 5540 8888 9090 3000 6300 5439 15673 5673 5441 8081 8080 28081 27017 7017 8085 3030)
  for port in "${ports[@]}"; do
    echo "Freeing up port $port..."
    sudo kill -9 $(sudo lsof -t -i:$port) 2>/dev/null
    sleep 0.025
  done
}

recreate_network() {
  echo "Recreating network..."
  docker network rm backend-network
  docker network rm frontend-network
  sleep 0.1
  docker network create --driver bridge backend-network
  docker network create --driver bridge frontend-network
}

remove_volumes() {
  echo "Removing volumes..."
  docker volume rm $(docker volume ls -q | grep "^backend_")
}

stop_containers
free_ports
recreate_network
remove_volumes

echo "Backend services are stopped gracefully."
