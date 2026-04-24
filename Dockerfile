FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir --default-timeout=100 --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

COPY . .

RUN chmod +x /app/entrypoint.sh

ARG VCS_REF=unknown
LABEL org.opencontainers.image.revision=$VCS_REF

STOPSIGNAL SIGTERM

CMD ["/app/entrypoint.sh"]