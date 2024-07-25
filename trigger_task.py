# trigger_task.py
from tasks import cpu_intensive_task

if __name__ == "__main__":
    num_tasks = 100  # Adjust this number as needed
    task_size = 10**7  # Increase this number to make the task more CPU-intensive
    for _ in range(num_tasks):
        cpu_intensive_task.delay(task_size)

