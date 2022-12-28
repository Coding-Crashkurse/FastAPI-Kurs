import time
import asyncio

ones = [1] * 10

def blocking_task(n: int) -> int:
    time.sleep(n)
    return n

async def non_blocking_task(n: int) -> int:
    await asyncio.sleep(n)
    return n

def blocking_function():
    results = []
    for n in ones:
        results.append(blocking_task(n))
    return results

async def non_blocking_function():
    results = []
    for n in ones:
        task = asyncio.create_task(non_blocking_task(n))
        results.append(task)
    return await asyncio.gather(*results)

start = time.perf_counter()
print(blocking_function())
end = time.perf_counter()
print(f"Blocking function took {end - start:.2f} seconds")

start = time.perf_counter()
print(asyncio.run(non_blocking_function()))
end = time.perf_counter()
print(f"Non-blocking function took {end - start:.2f} seconds")