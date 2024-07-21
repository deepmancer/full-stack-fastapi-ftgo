stop_containers() {
  echo "Stopping containers and removing orphans..."
  docker-compose down --remove-orphans
  sleep 0.2
  docker stop `docker ps -qa`
  sleep 0.2
  sudo systemctl restart docker.socket docker.service
  sleep 0.2
  docker stop `docker ps -qa`
  sleep 0.2
}

free_ports() {
  ports=(15920 5920 6490 5438 6235 8000 5020 5920 15920)
  for port in "${ports[@]}"; do
    echo "Freeing up port $port..."
    sudo kill -9 $(sudo lsof -t -i:$port) 2>/dev/null
    sleep 0.1
  done
}

stop_containers
free_ports

echo "Backend services are stopped."