# Dockerfile for Celery Worker
FROM python:3.9-slim

RUN pip install celery redis billiard

WORKDIR /app
COPY tasks.py /app/
COPY trigger_task.py /app/

CMD ["celery", "-A", "tasks", "worker", "--loglevel=info"]
