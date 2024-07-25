from celery import Celery
from billiard import cpu_count

app = Celery('tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0')

def calculate_primes(limit):
    def is_prime(n):
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True

    primes = []
    for num in range(2, limit):
        if is_prime(num):
            primes.append(num)
    return primes

@app.task
def cpu_intensive_task(limit):
    num_cpus = cpu_count()
    chunk_size = limit // num_cpus
    ranges = [(i * chunk_size, (i + 1) * chunk_size) for i in range(num_cpus)]

    def compute_chunk(start, end):
        return calculate_primes(end)  # Compute primes in the given range

    from billiard import Pool
    with Pool(processes=num_cpus) as pool:
        results = pool.starmap(compute_chunk, ranges)

    # Flatten the results list and count primes
    all_primes = [prime for sublist in results for prime in sublist]
    total_primes = len(all_primes)
    return total_primes
