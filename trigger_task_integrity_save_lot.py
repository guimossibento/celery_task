from tasks import cpu_integrity_task_lot
import os
import psycopg2
import socket
from dotenv import load_dotenv
from datetime import datetime
import traceback

load_dotenv()


def get_host_ip():
    try:
        hostname = socket.gethostname()
        host_ip = socket.gethostbyname(hostname)
        print(f"Host IP resolved: {host_ip}")
        return host_ip
    except Exception as e:
        print(f"Error getting host IP: {e}")
        return 'unknown'


def save_to_postgresql(results, host_ip):
    try:
        dbname = os.environ.get('DATABASE_NAME', 'test')
        user = os.environ.get('DATABASE_USER', 'postgres')
        password = os.environ.get('DATABASE_PASSWORD', 'secret')
        db_host = os.environ.get('DATABASE_HOST', 'localhost')
        port = os.environ.get('DATABASE_PORT', '5432')

        print(f"Database credentials: dbname={dbname}, user={user}, host={db_host}, port={port}")

        print("Attempting to connect to the PostgreSQL database...")
        with psycopg2.connect(dbname=dbname, user=user, password=password, host=db_host, port=port) as conn:
            print("Connection established successfully.")
            with conn.cursor() as cur:
                insert_query = 'INSERT INTO sequences (number, task_number, task_type, host_ip, created_at) VALUES (%s, %s, %s, %s, %s)'
                created_at = datetime.now()
                data_to_insert = [(result[0], result[1], result[2], host_ip, created_at) for result in results]

                print(f"Data to insert: {data_to_insert}")
                cur.executemany(insert_query, data_to_insert)
                conn.commit()
                print("Data inserted successfully.")
    except Exception as e:
        print(f"Error saving to PostgreSQL: {e}")
        print(traceback.format_exc())


if __name__ == "__main__":
    num_tasks = 14
    task_size = 100
    task_type = 'lot'

    print(f"Starting task execution: num_tasks={num_tasks}, task_size={task_size}, task_type={task_type}")
    host_ip = get_host_ip()

    all_results = []
    for i in range(num_tasks):
        print(f"Triggering Celery task {i} with size {task_size} and type {task_type}")
        task_result = cpu_integrity_task_lot.delay(task_size, i, task_type)
        all_results.append(task_result)

    # Wait for all tasks to complete and collect results
    collected_results = []
    for i, task_result in enumerate(all_results):
        try:
            print(f"Waiting for result of task {i}")
            task_results = task_result.wait()  # Adjust timeout as needed
            collected_results.extend(task_results)
            print(f"Task {i} completed with results: {task_results}")
        except Exception as e:
            print(f"Error waiting for result of task {i}: {e}")
            print(traceback.format_exc())

    # Save the results to PostgreSQL
    print("Saving results to PostgreSQL...")
    save_to_postgresql(collected_results, host_ip)
    print("Finished saving results to PostgreSQL.")
