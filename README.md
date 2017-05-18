docker build -t aiolos/alg-request-service:v1 .
docker run -d -p 82:8080 -v /$(pwd)/app:/app --name aiolos-websocket aiolos/alg-request-service:v1