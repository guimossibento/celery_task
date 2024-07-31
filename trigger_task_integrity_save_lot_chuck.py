from tasks import cpu_integrity_task_lot, cpu_integrity_task_lot_chunk
import os
from psycopg2 import OperationalError
import time
import psycopg2
import traceback
from dotenv import load_dotenv

load_dotenv()


def save_to_postgresql(results):
    retries = 5
    while retries > 0:
        try:
            dbname = os.environ.get('DATABASE_NAME', 'test')
            user = os.environ.get('DATABASE_USER', 'postgres')
            password = os.environ.get('DATABASE_PASSWORD', 'secret')
            host = os.environ.get('DATABASE_HOST', 'localhost')
            port = os.environ.get('DATABASE_PORT', '5432')

            print(f"Database credentials: dbname={dbname}, user={user}, host={host}, port={port}")

            print("Attempting to connect to the PostgreSQL database...")
            with psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port) as conn:
                print("Connection established successfully.")
                with conn.cursor() as cur:
                    insert_query = 'INSERT INTO sequences (number, task_number, task_type) VALUES (%s, %s, %s)'
                    print(f"Executing query: {insert_query} with values {results}")
                    cur.executemany(insert_query, results)
                    conn.commit()
                    print("Data inserted successfully.")
            break
        except OperationalError as e:
            retries -= 1
            print(f"Error saving to PostgreSQL: {e}")
            print(traceback.format_exc())
            print(f"Retrying... ({5 - retries} retries left)")
            time.sleep(5)
        except Exception as e:
            print(f"Unexpected error: {e}")
            print(traceback.format_exc())
            break


if __name__ == "__main__":
    num_tasks = 14
    task_size = 100
    task_type = 'lot_chunk'
    lot_size = 10

    print(f"Starting task execution: num_tasks={num_tasks}, task_size={task_size}, task_type={task_type}, lot_size={lot_size}")

    all_results = []
    for i in range(num_tasks):
        start = 0
        while start < task_size:
            end = start + lot_size
            print(f"Triggering Celery task for range ({start}, {end}), task_number={i}, task_type={task_type}")
            result = cpu_integrity_task_lot_chunk.delay(start, end, i, task_type)
            try:
                print(f"Waiting for result of task {i} for range ({start}, {end})")
                task_results = result.get()  # Adjust timeout as needed
                print(f"Task {i} for range ({start}, {end}) completed with results: {task_results}")
                save_to_postgresql(task_results)
            except Exception as e:
                print(f"Error waiting for result of task {i} for range ({start}, {end}): {e}")
                print(traceback.format_exc())
            start = end

    print("Finished executing all tasks.")
