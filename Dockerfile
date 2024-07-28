# Dockerfile for Celery Worker
FROM python:3.9-slim

RUN pip install celery redis billiard

WORKDIR /app
COPY tasks.py /app/
COPY trigger_task_integrity_save_each_time.py /app/
COPY trigger_task_integrity_save_lot.py /app/

CMD ["celery", "-A", "tasks", "worker", "--loglevel=info"]
