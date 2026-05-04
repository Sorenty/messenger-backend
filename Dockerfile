FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir --default-timeout=100 --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

COPY . .

ARG VCS_REF=unknown
LABEL org.opencontainers.image.revision=$VCS_REF

STOPSIGNAL SIGTERM

CMD ["python", "run.py"]

#FROM python:3.12-slim
#
#WORKDIR /app
#
#ENV PYTHONUNBUFFERED=1
#
#COPY requirements.txt .
#RUN pip install --no-cache-dir --default-timeout=100 --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
#
#COPY . .
#
#ARG VCS_REF=unknown
#LABEL org.opencontainers.image.revision=$VCS_REF
#
#STOPSIGNAL SIGTERM
#
#CMD ["gunicorn", "-b", "0.0.0.0:5000", "--workers", "3", "--graceful-timeout", "30", "--timeout", "60", "--access-logfile", "-", "--error-logfile", "-", "run:app"]