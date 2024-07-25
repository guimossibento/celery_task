# tasks.py
from celery import Celery
from billiard import Pool, cpu_count
import math

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

    with Pool(processes=num_cpus) as pool:
        results = pool.starmap(cpu_intensive_workload, ranges)

    return sum(results)
