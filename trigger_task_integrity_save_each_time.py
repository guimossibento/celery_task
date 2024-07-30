from tasks import cpu_intensive_task, cpu_integrity_task

if __name__ == "__main__":

    num_tasks = 14
    task_size = 10
    for i in range(num_tasks):
        cpu_integrity_task.delay(i, task_size)
