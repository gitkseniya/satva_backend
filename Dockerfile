# Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System deps for psycopg
RUN apt-get update && apt-get install -y \
    build-essential libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Entrypoint runs migrations then starts Flask
RUN chmod +x docker/entrypoint.sh || true

EXPOSE 5000
CMD ["/app/docker/entrypoint.sh"]
