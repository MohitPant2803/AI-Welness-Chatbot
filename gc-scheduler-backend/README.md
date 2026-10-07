# GC Scheduler Backend

The **GC Scheduler Backend** is a task scheduling and email notification system built using **gRPC**, **Celery**, **Redis**, and **MongoDB**. It allows scheduling of email notifications for meetings and other events, ensuring reliable and asynchronous task execution. This backend is designed to handle high concurrency and provides a robust framework for managing scheduled tasks.

---

## Features

- **gRPC API**: Provides a `ScheduleMeet` endpoint for scheduling email notifications.
- **Asynchronous Task Execution**: Uses Celery with Redis as the message broker for handling tasks asynchronously.
- **Email Notifications**: Sends personalized email invitations using an HTML template.
- **Database Integration**: Stores queued tasks and user details in MongoDB using Beanie ODM.
- **Redis Integration**: Tracks sent emails to avoid duplicate notifications.
- **Retry Mechanism**: Automatically retries failed tasks with exponential backoff.
- **Scheduled Tasks**: Uses Celery Beat to schedule periodic tasks like sending queued emails.

---

## Table of Contents

1. Architecture Overview
2. Installation
3. Usage
4. API Reference
5. Configuration
6. Security Considerations
7. Future Improvements

---

## Architecture Overview

The GC Scheduler Backend is composed of the following key components:

1. **gRPC Server**:
   - Exposes the `ScheduleMeet` endpoint for scheduling tasks.
   - Validates requests and queues tasks using Celery.

2. **Celery Workers**:
   - Processes tasks asynchronously.
   - Sends email notifications using SMTP.

3. **Redis**:
   - Acts as the message broker for Celery.
   - Tracks sent emails to prevent duplicate notifications.

4. **MongoDB**:
   - Stores queued tasks and user details for persistence.

5. **Email Template**:
   - A customizable HTML template (`doc.html`) is used for email notifications.

6. **Celery Beat**:
   - Schedules periodic tasks, such as sending emails from the queue daily.

---

## Installation

### Prerequisites

- Python 3.9 or higher
- Redis server
- MongoDB instance
- gRPC tools (`grpcio` and `grpcio-tools`)

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/gc-scheduler-backend.git
   cd gc-scheduler-backend
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start Redis and MongoDB:
   - Ensure Redis is running on `localhost:6379`.
   - Ensure MongoDB is running and accessible via the URI in config.py.

5. Generate gRPC code (if not already generated):
   ```bash
   python -m grpc_tools.protoc -I./protos --python_out=./src/generated --pyi_out=./src/generated --grpc_python_out=./src/generated protos/task.proto
   ```

6. Start the Celery worker:
   ```bash
   celery -A proj worker --pool=threads --concurrency=10 -l INFO
   ```

7. Start the Celery Beat scheduler:
   ```bash
   celery -A proj beat --loglevel=info
   ```

8. Start the gRPC server:
   ```bash
   python server.py
   ```

---

## Usage

### Scheduling a Meeting

1. Use the gRPC client (`client.py`) to schedule a meeting:
   ```bash
   python client.py
   ```

2. Example request:
   ```python
   task_pb2.MeetRequest(
       empid="EMP001",
       emailID="example@example.com",
       message="Scheduled Chat with Mindi",
       empName="John Doe",
       timestamp=1672531200  # Unix timestamp
   )
   ```

3. Example response:
   ```json
   {
       "success": true,
       "job_id": "abc123"
   }
   ```

---

## API Reference

### gRPC Service: `Scheduler`

#### Method: `ScheduleMeet`

- **Request**: `MeetRequest`
  - `empid` (string): Employee ID.
  - `emailID` (string): Recipient's email address.
  - `message` (string): Email subject/message.
  - `empName` (string): Recipient's name.
  - `timestamp` (int64): Scheduled time (Unix timestamp).

- **Response**: `MeetResponse`
  - `success` (bool): Indicates if the task was successfully scheduled.
  - `job_id` (string): Unique identifier for the scheduled task.

---

## Configuration

### Redis Configuration

- Redis is used as the message broker and result backend for Celery.
- Default configuration:
  - Host: `localhost`
  - Port: `6379`

### MongoDB Configuration

- MongoDB is used to store queued tasks and user details.
- Update the connection URI in config.py:
  ```python
  MONGO_URI = "your-mongodb-uri"
  ```

### Email Configuration

- Update the SMTP credentials in tasks.py:
  ```python
  SMTP_SERVER = "smtp.gmail.com"
  SMTP_PORT = 465
  SENDER_EMAIL = "your-email@gmail.com"
  SENDER_PASSWORD = "your-email-password"
  ```

---

## Security Considerations

1. **Hardcoded Credentials**:
   - SMTP credentials are hardcoded in tasks.py. Replace them with environment variables or a secrets manager.

2. **Input Validation**:
   - Ensure all incoming gRPC requests are validated to prevent malicious data.

3. **Database Security**:
   - Use secure credentials for MongoDB and restrict access to trusted IPs.

4. **Redis Security**:
   - Use authentication for Redis in production environments.

---

## Future Improvements

1. **Environment Variables**:
   - Replace hardcoded credentials with environment variables.

2. **Unit Tests**:
   - Add comprehensive unit tests for gRPC server and Celery tasks.

3. **Error Handling**:
   - Improve error handling in the `sendMail` task to provide detailed feedback.

4. **Logging**:
   - Enhance logging to include more detailed information about task execution.

5. **Scalability**:
   - Add support for distributed task execution across multiple Celery workers.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a detailed description of your changes.

---

For any questions or issues, feel free to open an issue in the repository or contact the maintainer.
