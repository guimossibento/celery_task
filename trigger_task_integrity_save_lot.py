# trigger.py

from tasks import cpu_integrity_task_lot
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def save_to_postgresql(results):
    try:
        dbname = os.environ.get('DATABASE_NAME', 'test')
        user = os.environ.get('DATABASE_USER', 'postgres')
        password = os.environ.get('DATABASE_PASSWORD', 'secret')
        host = os.environ.get('DATABASE_HOST', 'localhost')
        port = os.environ.get('DATABASE_PORT', '5432')

        with psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port) as conn:
            with conn.cursor() as cur:
                insert_query = 'INSERT INTO sequences (number, task_number, task_type) VALUES (%s, %s, %s)'
                cur.executemany(insert_query, results)
                conn.commit()
    except Exception as e:
        print(f"Error saving to PostgreSQL: {e}")


if __name__ == "__main__":
    num_tasks = 14
    task_size = 1000
    task_type = 'lot'

    all_results = []
    for i in range(num_tasks):
        # Trigger Celery tasks
        result = cpu_integrity_task_lot.delay(task_size, i, task_type)
        all_results.append(result)

    # Wait for all tasks to complete and collect results
    collected_results = []
    for result in all_results:
        task_results = result.wait()  # Adjust timeout as needed
        collected_results.extend(task_results)

    # Save the results to PostgreSQL
    save_to_postgresql(collected_results)
