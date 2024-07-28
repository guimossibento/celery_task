# trigger.py

from tasks import cpu_integrity_task_lot, cpu_integrity_task_lot_chunk
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
    task_type = 'lot_chunk'
    lot_size = 100

    all_results = []
    for i in range(num_tasks):
        start = 0
        while start < task_size:
            end = start + lot_size
            result = cpu_integrity_task_lot_chunk.delay(start, end, i, task_type)
            task_results = result.wait()
            # print(f"Processed result: {task_results}")
            save_to_postgresql(task_results)
            start = end
