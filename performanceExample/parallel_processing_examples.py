"""
并行处理大量数据示例

本文件包含使用多线程、多进程和异步处理大量数据的推荐写法
"""

import time
import threading
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from typing import List, Callable, Any


# ==================== 1. 使用 ThreadPoolExecutor ====================
def process_item_thread(item: Any) -> Any:
    """
    单项目处理函数（线程安全）
    
    推荐场景：IO密集型操作（网络请求、文件读写等）
    """
    # 模拟IO操作
    time.sleep(0.01)
    return item * 2


def parallel_with_threads(data: List[Any], max_workers: int = 4):
    """
    使用线程池并行处理数据
    
    推荐场景：IO密集型任务，如API调用、数据库查询等
    """
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交所有任务
        futures = [executor.submit(process_item_thread, item) for item in data]
        
        # 获取结果
        results = [future.result() for future in futures]
    
    return results


# ==================== 2. 使用 ProcessPoolExecutor ====================
def process_item_process(item: Any) -> Any:
    """
    单项目处理函数（可序列化）
    
    推荐场景：CPU密集型操作（数值计算、数据处理等）
    """
    # 模拟CPU密集型计算
    result = 0
    for i in range(100000):
        result += item * i
    return result


def parallel_with_processes(data: List[Any], max_workers: int = None):
    """
    使用进程池并行处理数据
    
    推荐场景：CPU密集型任务，充分利用多核CPU
    """
    if max_workers is None:
        max_workers = multiprocessing.cpu_count()
    
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # 使用 map 方法简化操作
        results = list(executor.map(process_item_process, data))
    
    return results


# ==================== 3. 使用多线程处理IO绑定任务 ====================
def fetch_url(url: str) -> str:
    """
    模拟网络请求
    
    推荐场景：批量API调用
    """
    import requests
    response = requests.get(url, timeout=10)
    return f"{url}: {response.status_code}"


def batch_fetch_urls(urls: List[str]):
    """批量获取URL内容"""
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(fetch_url, urls))
    
    for result in results:
        print(result)


# ==================== 4. 使用多进程处理CPU绑定任务 ====================
def compute_factorial(n: int) -> int:
    """计算阶乘"""
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result


def parallel_factorials(numbers: List[int]):
    """并行计算多个数的阶乘"""
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(compute_factorial, numbers))
    
    for n, result in zip(numbers, results):
        print(f"{n}! = {result}")


# ==================== 5. 异步并行处理 ====================
async def async_process_item(item: Any) -> Any:
    """
    异步处理单项目
    
    推荐场景：大量IO操作的异步处理
    """
    import asyncio
    
    # 模拟异步IO操作
    await asyncio.sleep(0.01)
    return item * 2


async def async_parallel_process(data: List[Any]):
    """
    使用 asyncio 异步并行处理
    
    推荐场景：高并发IO操作
    """
    import asyncio
    
    # 创建所有任务
    tasks = [async_process_item(item) for item in data]
    
    # 并发执行
    results = await asyncio.gather(*tasks)
    
    return results


# ==================== 6. 生产者-消费者模式 ====================
def producer(queue: multiprocessing.Queue, data: List[Any]):
    """生产者：将数据放入队列"""
    for item in data:
        queue.put(item)
    queue.put(None)  # 结束标记


def consumer(queue: multiprocessing.Queue, results: List[Any]):
    """消费者：从队列获取数据并处理"""
    while True:
        item = queue.get()
        if item is None:
            queue.put(None)  # 传递结束标记
            break
        
        # 处理数据
        result = process_item_process(item)
        results.append(result)


def producer_consumer_pattern(data: List[Any]):
    """
    使用生产者-消费者模式处理数据
    
    推荐场景：流式数据处理，数据生成和处理速度不匹配
    """
    manager = multiprocessing.Manager()
    queue = manager.Queue(maxsize=100)
    results = manager.list()
    
    # 创建生产者进程
    producer_process = multiprocessing.Process(
        target=producer,
        args=(queue, data)
    )
    
    # 创建消费者进程
    consumer_process = multiprocessing.Process(
        target=consumer,
        args=(queue, results)
    )
    
    # 启动进程
    producer_process.start()
    consumer_process.start()
    
    # 等待完成
    producer_process.join()
    consumer_process.join()
    
    return list(results)


# ==================== 7. 使用 threading 模块 ====================
def thread_process(data_chunk: List[Any], results: List[Any], lock: threading.Lock):
    """线程处理函数"""
    for item in data_chunk:
        result = item * 2
        
        # 使用锁保护共享数据
        with lock:
            results.append(result)


def manual_threading(data: List[Any], num_threads: int = 4):
    """
    手动创建线程处理数据
    
    推荐场景：需要更细粒度控制的线程操作
    """
    # 分割数据
    chunk_size = len(data) // num_threads
    chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
    
    # 创建共享结果列表和锁
    results = []
    lock = threading.Lock()
    
    # 创建线程
    threads = []
    for chunk in chunks:
        thread = threading.Thread(
            target=thread_process,
            args=(chunk, results, lock)
        )
        threads.append(thread)
        thread.start()
    
    # 等待所有线程完成
    for thread in threads:
        thread.join()
    
    return results


# ==================== 性能对比测试 ====================
def performance_comparison():
    """对比不同并行方式的性能"""
    data = list(range(100))
    
    # 串行处理
    start = time.time()
    serial_results = [process_item_process(item) for item in data]
    serial_time = time.time() - start
    print(f"串行处理: {serial_time:.4f}s")
    
    # 多线程处理
    start = time.time()
    thread_results = parallel_with_threads(data, max_workers=4)
    thread_time = time.time() - start
    print(f"多线程处理: {thread_time:.4f}s")
    
    # 多进程处理
    start = time.time()
    process_results = parallel_with_processes(data, max_workers=4)
    process_time = time.time() - start
    print(f"多进程处理: {process_time:.4f}s")


# ==================== 示例运行 ====================
if __name__ == "__main__":
    print("=" * 60)
    print("并行处理大量数据示例")
    print("=" * 60)
    
    # 性能对比
    print("\n1. 性能对比测试:")
    performance_comparison()
    
    # 多进程阶乘计算
    print("\n2. 多进程阶乘计算:")
    parallel_factorials([5, 10, 15])
    
    # 生产者-消费者模式
    print("\n3. 生产者-消费者模式:")
    data = list(range(20))
    results = producer_consumer_pattern(data)
    print(f"处理结果数量: {len(results)}")
    
    print("\n" + "=" * 60)
    print("所有示例运行完成")
    print("=" * 60)
