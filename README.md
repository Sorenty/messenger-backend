# Messenger Backend

Backend мессенджера на Flask с использованием Docker, PostgreSQL, Redis и CI/CD.

---

##  Запуск проекта

Собрать и запустить контейнеры:

---

docker compose up -d --build

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


docker compose exec app flask db upgrade
docker compose exec db psql -U postgres -d messenger_db -c "\dt"
Invoke-RestMethod -Method Post -Uri "http://localhost:8080/api/channels/test/messages" -ContentType "application/json" -Body '{"sender":"alex","text":"hello"}'
curl.exe "http://localhost:8080/api/channels/test/messages"

curl.exe http://localhost:8080/api/channels/sleep/10      
docker kill --signal=SIGTERM messenger-backend-app-1
curl.exe http://localhost:8080/health