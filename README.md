# FTGO

## Backend Setup

### Create Dockers Networks
```
 docker network create frontend-network
 docker network create backend-network
```

### Build and Run Infrastructure
```
cd backend/infra
docker compose up --build
```

### Build and Run Microservices
```
cd backend/
docker compose up --build
```

## Fronted Setup

### Requirements Installation
```
cd ui/
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```
