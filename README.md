
# **🍕 Full-stack Microservice-Based Food Ordering Application**

> FTGO is a scalable, microservice-based food ordering application built with Python (FastAPI) and Vue.js, designed following object-oriented design principles.

**💎 You can use this project as a template to build your backend microservice project in Python 💎**

🔊 New features and technologies will be added soon!

### 🔥 Technology Stack and Features

- ⚡ [**FastAPI**](https://fastapi.tiangolo.com):
    - 🔮 [pydantic](https://docs.pydantic.dev) for setting and validation.
    - 🔑 JWT middleware for secure authentication.
    - 🚧 Permission manager for role-based access control on routes.
    - 📛 Rate limiting for API protection.
    - ⌚ RequestId, Timing, and many exciting middlewares!
    - 🔒 Secure password hashing by default.
    - 🌀 Customizable profilers with [Prometheus][https://prometheus.io/].

- 🌱 [**MongoDB**](https://www.mongodb.com/): 
  - Async client with [motor](https://github.com/mongodb/motor) and Object Document Mapping (ODM) with [beanie](https://beanie-odm.dev/).
  - [mongo-motors](https://github.com/alirezaheidari-cs/mongo-motors) package for singleton and managed connection.

- 🧰 [**Redis**](https://redis.io/):
  - Async operations for caching and session management.
  - [redis-py](https://github.com/redis/redis-py) with [aredis-client](https://github.com/alirezaheidari-cs/aredis-client).

- 💾 **PostgreSQL**:
  - Async client with [aqlachemy](https://github.com/sqlalchemy/sqlalchemy) ORM & automatic migrations with [alembic](https://github.com/sqlalchemy/alembic)..
  - [asyncpg-client](https://github.com/alirezaheidari-cs/asyncpg-client) as the session manager.

- 🚀 [**RabbitMQ**](https://www.rabbitmq.com/):
  - Utilizing [rabbitmq-rpc](https://github.com/alirezaheidari-cs/rabbitmq-rpc) and [aio-pika](https://github.com/mosquito/aio-pika).
  - No server-side implementation.

- 🐋 [**Docker Compose**](https://www.docker.com):
  - Containers for simplified deployment and scaling.

- ✅ [**Pytest**](https://github.com/pytest-dev/pytest):
  - Async tests for pytest.

## **📂 GUI Management Tools**
- 🔆 [**Grafana**](https://grafana.com/): Automatic metric dashboards on endpoints using [Prometheus][https://prometheus.io/].
- 📉 [**Metabase**](https://www.metabase.com/): PostgreSQL/MongoDB analytics and reporting.
- 📕 [**RedisInsight**](https://redis.io/insight/): Redis data visualization and management.
- 🌿 [**Mongo-Express**](https://github.com/mongo-express/mongo-express): MongoDB management.
- 💥 [**RabbitMQ Management**](https://www.rabbitmq.com/docs/management): Visualizing and monitoring events.
 
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

## Interactive API Documentation
![image](https://github.com/user-attachments/assets/ebfe2c0e-b9e0-4e01-b266-89b54776428c)

## Admin Dashboards
### **Grafana [localhost:3000](localhost:3000):**
![image](https://github.com/user-attachments/assets/1b2a7305-c542-48a4-8d94-b64879027886)

### **Metabase [localhost:3030](localhost:3030):**
![image](https://github.com/user-attachments/assets/a6f962fa-ae6c-4d25-80ca-ed95837972e9)

### **RedisInsight [localhost:5540](localhost:5540):**
![image](https://github.com/user-attachments/assets/0e04ec30-8180-486d-bf7f-11c98f4476ae)

### **RabbitMQ Management [localhost:15673](localhost:15673):
![image](https://github.com/user-attachments/assets/17532670-8b31-4b2d-b305-723b8ce49f77)

### **Mongo Compass:**
![image](https://github.com/user-attachments/assets/11be638a-6cd3-4f9c-ad84-eedda8bc4867)
