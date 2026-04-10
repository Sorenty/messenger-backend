# Messenger Backend

Backend мессенджера на Flask с использованием Docker, PostgreSQL, Redis и CI/CD.

---

##  Запуск проекта

Собрать и запустить контейнеры:

---

docker compose up -d --build

docker-compose up --build --scale app=3

POST http://localhost:8080/api/channels/test/messages

{
  "sender": "alex",
  "text": "hello"
}

GET http://localhost:8080/api/channels/test/messages

docker compose up -d --build

docker compose logs -f app

curl.exe -H "X-Request-ID: demo-123" http://localhost:8080/health

curl.exe -c cookies.txt -b cookies.txt http://localhost:8080/api/channels/session-demo
curl.exe -c cookies.txt -b cookies.txt http://localhost:8080/api/channels/session-demo