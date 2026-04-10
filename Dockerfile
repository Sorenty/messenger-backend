FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir --default-timeout=100 --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

COPY . .

ARG VCS_REF=unknown
LABEL org.opencontainers.image.revision=$VCS_REF

CMD ["sh", "-c", "gunicorn -w ${WEB_CONCURRENCY:-2} -b 0.0.0.0:${PORT:-5000} 'run:app'"]