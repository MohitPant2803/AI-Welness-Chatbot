FROM alpine:3.18

# Install runtime dependencies
RUN apk add --no-cache python3=~3.11 py3-pip

WORKDIR /app

# Install application dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Explicit binding for Windows compatibility
CMD ["python", "/app/app/main.py", "--host", "0.0.0.0", "--port", "8002"]