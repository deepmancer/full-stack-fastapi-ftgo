
# **🍕 Full-stack Microservice-Based Food Ordering Application**

FTGO is a scalable, microservice-based food ordering application built with Python and Vue.js, designed following object-oriented design principles.

**💎 You can use this project as a template to build your backend microservice project in python 💎**
🔨 New features and technologies will be added soon!

## **💡 Backend Overview**

The backend is composed of multiple microservices, each handling specific functionalities and communicating asynchronously via RabbitMQ. The application uses MongoDB, PostgreSQL, and Redis, with FastAPI serving as the API framework in the Gateway microservice.

### **🔥 Technical Features**
  - ⚡ [**FastAPI**](https://fastapi.tiangolo.com):
    -  [pydantic](https://docs.pydantic.dev) for setting and validation.
    - 🔑 JWT middleware for secure authentication.
    - 🚧 Permission manager for role-based access control on routes.
    - 📛 Rate limiting for API protection.
    - ⌚ RequestId, Timing, and many exciting middlewares!
    - 🔒 Secure password hashing by default.

- 🌱 [**MongoDB**](https://www.mongodb.com/): 
  - Async operations using [motor](https://github.com/mongodb/motor).
  - ODM with [beanie](https://beanie-odm.dev/).
  - [mongo-motors](https://github.com/alirezaheidari-cs/mongo-motors) package for singleton and managed connection.

- 🧰 [**Redis**](https://redis.io/):
  - Async operations for caching and session management.
  - [redis-py](https://github.com/redis/redis-py) with [aredis-client](https://github.com/alirezaheidari-cs/aredis-client).

- 💾 **PostgreSQL**:
  - Async with [aqlachemy](https://github.com/sqlalchemy/sqlalchemy) ORM.
  - Database migrations with [alembic](https://github.com/sqlalchemy/alembic).
  - [asyncpg-client](https://github.com/alirezaheidari-cs/asyncpg-client) as the session manager.

- 🚀 [**RabbitMQ**](https://www.rabbitmq.com/):
  - As the message broker for inter-microservice communications.
  - Utilizing [rabbitmq-rpc](https://github.com/alirezaheidari-cs/rabbitmq-rpc) and [aio-pika](https://github.com/mosquito/aio-pika).
  - No server-side implementation.

- 🐋 [**Docker Compose**](https://www.docker.com):
  - Containers for simplified deployment and scaling.

- ✅ [**Pytest**](https://github.com/pytest-dev/pytest):
  - Async tests for pytest.

### **📂 GUI Management Tools**

- 📉 [**Metabase**](https://www.metabase.com/): PostgreSQL/MongoDB analytics and reporting. localhost:3000
- 📕 [**RedisInsight**](https://redis.io/insight/): Redis data visualization and management.
- 🌿 [**Mongo-Express**](https://github.com/mongo-express/mongo-express): For MongoDB management.

These tools are configured and run via Docker in the `infra/admin/docker-compose.yaml`.

## **Setup Instructions**

### **Step 1: Create Docker Networks**

Create Docker networks for backend and frontend services.

```bash
docker network create --driver bridge backend-network
docker network create --driver bridge frontend-network
```

### **Step 2: Build and Run Infrastructure**

Navigate to the infrastructure directory and start the services, including databases and GUI tools.

```bash
cd backend/infra
docker compose up --build
```

#### **Infrastructure Layout:**

```bash
backend/infra
├── admin (Metabase, RedisInsight, Mongo-Express)
├── mongo
├── monitoring (Grafana, Prometheus)
├── postgres
├── rabbitmq (with the Management extension)
└── redis
```

### **Step 3: Build and Run Microservices**

Navigate to the backend directory and start all microservices.

```bash
cd backend/
docker compose up --build
```

## **Frontend Setup**

The frontend is built with Vue.js for a dynamic and responsive user experience.

### **Step 1: Install Dependencies**

Navigate to the `ui/` directory and install the required packages.

```bash
cd ui/
npm install
```

### **Step 2: Start Development Server**

Run the development server with hot-reloading enabled.

```bash
npm run serve
```

## **Additional Features**

- **Monitoring and Logging**: Integrated logging, rate limiting, and monitoring with Grafana and Prometheus.
- **Security**: JWT authentication, role-based access control, and Pydantic data validation.
