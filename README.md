# GC25 Project Documentation

## Overview

GC25 is a comprehensive system with multiple backend services communicating through gRPC. The project is designed for scheduling meetings, generating reports, handling chat functionality, and managing updates through an asynchronous architecture.

## System Architecture

The system consists of the following core components:

1. **gc-auth-backend**: Authentication service written in Python
2. **gc-chat-backend**: Chat functionality service written in Python
3. **gc-report-backend**: Report generation service written in Python
4. **gc-scheduler-backend**: Meeting scheduling service with asynchronous task processing
5. **gc-update-backend**: Update management service with asynchronous task processing
6. **gc-frontend**: Frontend built with Next.js and TypeScript

## Backend Services

### gc-auth-backend

Handles user authentication and authorization for the entire system.

**Key Components:**
- User authentication API
- Token generation and validation
- Role-based access control

### gc-chat-backend

A Python-based service that provides chat functionality, with gRPC integration to communicate with other services, particularly the scheduler service.

**Key Components:**
- gRPC client integration with scheduler service
- REST API endpoints for chat functionality
- WebSocket support for real-time communication

### gc-report-backend

Handles report generation and processing functionality.

**Key Components:**
- Report generation engine
- Data processing and visualization
- PDF/document export capabilities

### gc-scheduler-backend

A task scheduling and email notification system built with gRPC, Celery, Redis, and MongoDB.

**Key Features:**
- gRPC API with `ScheduleMeet` endpoint
- Asynchronous task execution with Celery
- Email notifications with HTML templating
- MongoDB integration for data persistence
- Redis for message brokering and tracking
- Automatic retry mechanism for failed tasks
- Scheduled tasks with Celery Beat

### gc-update-backend

Handles system updates and synchronization across services.

**Key Components:**
- Celery workers for asynchronous update processing
- Celery Beat for scheduled updates
- Integration with other services for consistency

## Frontend - gc-frontend

The frontend is built with **Next.js and TypeScript** and communicates with backend services via REST/gRPC APIs.

**Key Features:**
- Server-side rendering (SSR) and static site generation (SSG)
- WebSocket support for real-time chat
- Secure authentication integration with gc-auth-backend
- Modern UI with React and Tailwind CSS

## Fully Dockerized Setup

All services are containerized using Docker, making deployment and development easier. The project uses `docker-compose` to orchestrate multiple containers.

### Steps to Build and Run the Project Using Docker Compose

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-repo/gc25.git
   cd gc25
   ```

2. **Ensure Docker and Docker Compose are installed**.

3. **Build and run the services**:
   ```bash
   docker-compose up --build -d
   ```

4. **Access the frontend**:  
   Open [http://localhost:3000](http://localhost:3000) in your browser.

5. **Access backend services**:  
   The services are exposed on respective ports defined in `docker-compose.yml`.

6. **Shut down services**:
   ```bash
   docker-compose down
   ```

### Troubleshooting

- If any service fails, check logs using:
  ```bash
  docker-compose logs -f <service-name>
  ```
- If the frontend does not connect to the backend, ensure backend services are running correctly.
- Restart containers if necessary:
  ```bash
  docker-compose restart
  ```

## Communication Between Services

Services communicate primarily through gRPC, with protocol buffer definitions defining the interfaces. The scheduler service, for example, provides a `ScheduleMeet` endpoint that can be called by the chat backend.

## Technology Stack

- **Frontend**: Next.js with TypeScript
- **Backend**: Python (FastAPI/Flask with gRPC)
- **Task Processing**: Celery
- **Message Broker**: Redis
- **Database**: MongoDB
- **ODM**: Beanie (for MongoDB)
- **WebSockets**: Socket.io/WebSockets for real-time updates
- **Authentication**: JWT-based authentication
- **Containerization**: Docker & Docker Compose
- **Logging & Monitoring**: Prometheus & Grafana

## Development and Extension

When developing or extending functionality:

1. Ensure gRPC protocol buffers are synchronized across services.
2. Update Celery task definitions when adding new asynchronous operations.
3. Maintain MongoDB schema compatibility when changing data models.
4. Consider the distributed nature of the system when making changes.

---

This documentation provides a detailed overview of the project and instructions to get started with a fully Dockerized setup.
