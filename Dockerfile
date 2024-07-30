# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Install build tools and PostgreSQL client library
RUN apt-get update && apt-get install -y gcc python3-dev libpq-dev

# Create a non-root user
RUN useradd -ms /bin/bash celeryuser

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir sqlalchemy celery[sqlalchemy]

# Change ownership of the working directory to the non-root user
RUN chown -R celeryuser:celeryuser /app

RUN chown -R celeryuser:celeryuser .
RUN chmod -R o+w .

# Switch to the non-root user
USER celeryuser

# Run the Celery worker when the container launches
CMD ["celery", "-A", "tasks", "worker", "--loglevel=info"]
