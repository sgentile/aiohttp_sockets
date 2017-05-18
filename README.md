docker build -t aiolos/alg-request-service:v1 .

For windows: 

docker run -d -p 82:8080 -v C:/Users/steve.gentile/Projects/EIP-Docker/app:/app --name aiolos-websocket aiolos/alg-request-service:v1

For real OSs:

docker build -t aiolos/alg-request-service:v1 . docker run -d -p 82:8080 -v /$(pwd)/app:/app --name aiolos-websocket aiolos/alg-request-service:v1