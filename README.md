  # Messenger Backend

  Backend мессенджера на Flask с использованием Docker, PostgreSQL, Redis и CI/CD.

  ---

  ##  Запуск проекта

  ### 1. Клонировать репозиторий
  git clone https://github.com/your-username/messenger-backend.git
  cd messenger-backend
  2. Запустить контейнеры
  docker compose up -d --build
  3. Применить миграции
  docker compose exec app flask db upgrade
  4. Готово
  Сервер доступен по адресу:

  http://localhost:8080

  ### Регистрация

  POST /api/auth/register

  ```json
  {
    "email": "admin@example.com",
    "password": "admin123"
  }
  ```

  ---