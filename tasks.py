# tasks.py
import os
import psycopg2
from celery import Celery
from billiard import Pool, cpu_count
import math
import time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
app = Celery('tasks',
             broker='redis://redis:6379/0',
             backend=f"db+postgresql://{os.environ['DATABASE_USER']}:{os.environ['DATABASE_PASSWORD']}@{os.environ['DATABASE_HOST']}:{os.environ['DATABASE_PORT']}/{os.environ['DATABASE_NAME']}")


def cpu_intensive_workload(start, end):
    x = 0
    for i in range(start, end):
        x += math.sqrt(i)
    return x


@app.task
def cpu_intensive_task(n):
    num_cpus = cpu_count()
    chunk_size = n // num_cpus
    ranges = [(i * chunk_size, (i + 1) * chunk_size) for i in range(num_cpus)]

    with Pool(processes=num_cpus) as pool:
        results = pool.starmap(cpu_intensive_workload, ranges)

    total_result = sum(results)

    return total_result


def save_to_postgresql(number, task_number):
    try:
        dbname = os.environ.get('DATABASE_NAME', 'test')
        user = os.environ.get('DATABASE_USER', 'postgres')
        password = os.environ.get('DATABASE_PASSWORD', 'secret')
        host = os.environ.get('DATABASE_HOST', 'localhost')
        port = os.environ.get('DATABASE_PORT', '5432')

        with psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port) as conn:
            with conn.cursor() as cur:
                insert_query = 'INSERT INTO sequences (number, task_type, task_number) VALUES (%s, %s, %s)'
                cur.execute(insert_query, (number, 'one', task_number))

                conn.commit()
    except Exception as e:
        print(f"Error saving to PostgreSQL: {e}")


def cpu_save_sequence(start, end, task_number):
    print(f'Starting save sequence from {start} to {end} for task {task_number}')
    for i in range(start, end):
        save_to_postgresql(i, task_number)
    return end - start  # Return the number of sequences saved in this chunk


@app.task
def cpu_integrity_task(task_number, n):
    start = 0
    end = n
    intensive_task = cpu_intensive_task.delay(5000000)
    intensive_task.wait()
    try:
        result = cpu_save_sequence(start, end, task_number)
        print(f"Task {task_number} completed. Sequences saved: {result}")
    except Exception as e:
        print(f"Error in task {task_number}: {e}")
        result = 0

    return result


@app.task
def cpu_integrity_task_lot(n, task_number, type):
    start = 0
    end = n
    # intensive_task = cpu_intensive_task.delay(5000000)
    # intensive_task.wait()

    # Create an array with all values in the range, each associated with the task_number and type
    values_range = [(i, task_number, type) for i in range(start, end)]

    # Return the list of tuples (value, task_number, type)
    return values_range


@app.task
def cpu_integrity_task_lot_chunk(start, end, task_number, type):
    intensive_task = cpu_intensive_task.delay(5000000)

    # Create an array with all values in the range, each associated with the task_number and type
    values_range = [(i, task_number, type) for i in range(start, end)]

    # Return the list of tuples (value, task_number, type)
    return values_range


