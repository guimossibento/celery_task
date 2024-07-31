from tasks import cpu_integrity_task

if __name__ == "__main__":

    num_tasks = 4
    task_size = 10000
    for i in range(num_tasks):
        cpu_integrity_task.delay(i, task_size)
