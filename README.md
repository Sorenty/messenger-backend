docker run -p 8080:5000  -e DATABASE_URL=postgresql://postgres:12@host.docker.internal:5432/messenger_db -e SECRET_KEY=dev -e PORT=5000 messenger-app


docker-compose up --build

http://localhost:8080

docker-compose up --build --scale app=3

docker ps

POST http://localhost:8080/api/channels/test/messages

{
  "sender": "alex",
  "text": "hello"
}

GET http://localhost:8080/api/channels/test/messages

docker stop messenger-backend-main-app-1

docker kill messenger-backend-main-db-1

docker ps

docker stop messenger-backend-main-app-1
docker stop messenger-backend-main-app-2
docker stop messenger-backend-main-app-3

docker-compose up -d

GET http://localhost:8080/api/channels/test/messages