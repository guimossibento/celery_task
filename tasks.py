from celery import Celery
from billiard import Pool, cpu_count
import math
import time
from datetime import datetime

app = Celery('tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0')

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

    start_time = time.time()  # Record the start time

    with Pool(processes=num_cpus) as pool:
        results = pool.starmap(cpu_intensive_workload, ranges)

    total_result = sum(results)

    end_time = time.time()  # Record the end time
    elapsed_time = end_time - start_time

    # Write completion time to a file
    log_file = './log_file.txt'  # Adjust the path as needed
    with open(log_file, 'a') as f:
        f.write(f"Task completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Time taken: {elapsed_time} seconds\n")

    return total_result
