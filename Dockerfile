# Базовый образ
FROM python:3.10

# Рабочая папка внутри контейнера
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Открываем порт
EXPOSE 5000

# Команда запуска
CMD ["python", "run.py"]