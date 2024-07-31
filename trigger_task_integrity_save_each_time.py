from tasks import cpu_integrity_task

if __name__ == "__main__":

    num_tasks = 10
    task_size = 500
    for i in range(num_tasks):
        cpu_integrity_task.delay(i, task_size)
