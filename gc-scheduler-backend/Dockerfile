FROM alpine:3.18

# Install runtime + build dependencies
RUN apk add --no-cache python3=~3.11 py3-pip && \
    apk add --virtual .build-deps gcc musl-dev python3-dev

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Cleanup build dependencies
RUN apk del .build-deps

# Single foreground process with --beat flag
CMD ["celery", "-A", "proj", "worker", "--pool=threads", "--concurrency=10", "-l", "INFO", "--beat", "--hostname", "scheduler@%h"]