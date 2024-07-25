from tasks import cpu_intensive_task


def trigger_tasks():
    limit = 10 ** 6  # Set the limit for prime number calculation
    num_tasks = 1  # Number of tasks to trigger
    for _ in range(num_tasks):
        result = cpu_intensive_task.delay(limit)
        print(f"Task ID: {result.id}")

        # Wait for the result and print the total number of primes
        total_primes = result.get(timeout=3600)  # Wait up to 1 hour for the result
        print(f"Total number of primes found: {total_primes}")


if __name__ == "__main__":
    trigger_tasks()
