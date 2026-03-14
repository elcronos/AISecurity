FROM python:3.11-slim

WORKDIR /app

# curl for healthcheck in entrypoint; libjpeg-dev + libpng-dev for Pillow
RUN apt-get update && apt-get install -y curl libjpeg-dev libpng-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x entrypoint.sh

EXPOSE 8080

ENTRYPOINT ["./entrypoint.sh"]
