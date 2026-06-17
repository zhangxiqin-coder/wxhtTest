"""
大量数据处理的推荐写法示例

本文件包含处理大量数据时的最佳实践和推荐写法
"""

import itertools
import functools
import gc
from typing import Generator, List, Dict, Any


# ==================== 1. 使用生成器代替列表 ====================
def generate_large_data(size: int) -> Generator[Dict, None, None]:
    """
    使用生成器生成大量数据，避免一次性加载到内存
    
    推荐场景：处理超过内存限制的数据集
    """
    for i in range(size):
        yield {
            "id": i,
            "name": f"item_{i:06d}",
            "value": i * 2.5,
            "active": i % 3 == 0
        }


def process_with_generator():
    """使用生成器处理大数据"""
    # 生成器不会一次性加载所有数据到内存
    data_generator = generate_large_data(1_000_000)
    
    total = 0
    for item in data_generator:
        if item["active"]:
            total += item["value"]
    
    print(f"Total value of active items: {total}")


# ==================== 2. 批量处理数据 ====================
def batch_process(data: List[Dict], batch_size: int = 1000):
    """
    批量处理数据，减少内存压力
    
    推荐场景：数据库批量插入、API批量调用等
    """
    for i in range(0, len(data), batch_size):
        batch = data[i:i + batch_size]
        yield batch


def process_in_batches(data: List[Dict]):
    """分批处理数据"""
    for batch in batch_process(data, batch_size=1000):
        # 处理每一批数据
        process_batch(batch)


def process_batch(batch: List[Dict]):
    """处理单个批次"""
    # 示例：批量保存到数据库
    # db.session.add_all(batch)
    # db.session.commit()
    print(f"Processed {len(batch)} items")


# ==================== 3. 使用 itertools 优化循环 ====================
def use_itertools():
    """使用 itertools 高效处理迭代"""
    # 示例1: 无限迭代器
    counter = itertools.count(start=1, step=2)
    
    # 示例2: 合并多个迭代器
    iter1 = generate_large_data(1000)
    iter2 = generate_large_data(1000)
    merged = itertools.chain(iter1, iter2)
    
    # 示例3: 分组处理
    data = generate_large_data(10000)
    grouped = itertools.groupby(data, key=lambda x: x["active"])
    
    for is_active, items in grouped:
        count = sum(1 for _ in items)
        print(f"Active={is_active}: {count} items")


# ==================== 4. 使用 functools.lru_cache 缓存结果 ====================
@functools.lru_cache(maxsize=128)
def expensive_calculation(param: int) -> int:
    """
    使用缓存避免重复计算
    
    推荐场景：重复调用相同参数的计算密集型函数
    """
    # 模拟耗时计算
    result = 0
    for i in range(1_000_000):
        result += param * i
    return result


def use_caching():
    """使用缓存优化性能"""
    # 第一次调用会计算
    result1 = expensive_calculation(42)
    
    # 第二次调用会使用缓存
    result2 = expensive_calculation(42)
    
    assert result1 == result2


# ==================== 5. 内存优化：避免不必要的对象创建 ====================
def memory_efficient_processing():
    """内存高效的数据处理"""
    # 避免在循环中创建重复对象
    template = "Item: {id}, Value: {value}"
    
    data = generate_large_data(100000)
    
    for item in data:
        # 使用预定义的模板，避免每次创建新字符串
        message = template.format(id=item["id"], value=item["value"])
        # process(message)


# ==================== 6. 异步处理大量数据 ====================
async def async_process_data(data: List[Dict]):
    """
    使用异步处理大量数据
    
    推荐场景：IO密集型操作，如网络请求、文件读写等
    """
    import asyncio
    
    async def process_item(item: Dict):
        # 模拟异步IO操作
        await asyncio.sleep(0.001)
        return item["value"]
    
    # 并发处理所有项目
    tasks = [process_item(item) for item in data]
    results = await asyncio.gather(*tasks)
    
    total = sum(results)
    print(f"Async processing complete. Total: {total}")


# ==================== 7. 使用内置函数优化 ====================
def use_builtins():
    """使用Python内置函数提高性能"""
    data = list(generate_large_data(100000))
    
    # 使用 map() 代替手动循环
    values = list(map(lambda x: x["value"], data))
    
    # 使用 filter() 过滤数据
    active_items = list(filter(lambda x: x["active"], data))
    
    # 使用 sum() 代替手动累加
    total = sum(item["value"] for item in data if item["active"])
    
    print(f"Total of active items: {total}")


# ==================== 8. 数据库批量操作 ====================
def database_batch_operations():
    """
    数据库批量操作示例
    
    推荐场景：大量数据的数据库插入/更新
    """
    # 示例1: 使用 executemany 批量插入
    # cursor.executemany(
    #     "INSERT INTO items (id, name, value) VALUES (?, ?, ?)",
    #     [(item["id"], item["name"], item["value"]) for item in data]
    # )
    
    # 示例2: 使用 SQLAlchemy 批量操作
    # from sqlalchemy import insert
    # stmt = insert(Item).values([
    #     {"id": item["id"], "name": item["name"], "value": item["value"]}
    #     for item in data
    # ])
    # db.session.execute(stmt)
    # db.session.commit()
    pass


# ==================== 9. 使用 numpy/pandas 处理数值数据 ====================
def use_numpy_pandas():
    """
    使用 numpy/pandas 高效处理数值数据
    
    推荐场景：大量数值计算、数据分析
    """
    try:
        import numpy as np
        import pandas as pd
        
        # 使用 numpy 处理数值数组
        values = np.arange(1_000_000) * 2.5
        
        # 向量化操作，比Python循环快100倍以上
        result = np.sum(values[values > 1000])
        
        # 使用 pandas 处理表格数据
        df = pd.DataFrame({
            "id": np.arange(100000),
            "value": np.random.rand(100000)
        })
        
        # 快速聚合
        summary = df.groupby(df["id"] % 10)["value"].sum()
        
        print(f"NumPy result: {result}")
        print(f"Pandas summary:\n{summary}")
        
    except ImportError:
        print("请安装 numpy 和 pandas: pip install numpy pandas")


# ==================== 10. 垃圾回收控制 ====================
def controlled_gc():
    """
    控制垃圾回收时机，优化性能
    
    推荐场景：长时间运行的批处理任务
    """
    # 在关键代码段禁用GC
    gc.disable()
    
    try:
        # 执行内存密集型操作
        data = list(generate_large_data(100000))
        process_data(data)
    finally:
        # 恢复GC
        gc.enable()
        gc.collect()  # 手动触发一次GC


def process_data(data: List[Dict]):
    """处理数据"""
    total = sum(item["value"] for item in data)
    print(f"Processed {len(data)} items. Total: {total}")


# ==================== 示例运行 ====================
if __name__ == "__main__":
    print("=" * 60)
    print("大量数据处理推荐写法示例")
    print("=" * 60)
    
    # 运行各个示例
    print("\n1. 使用生成器处理大数据:")
    process_with_generator()
    
    print("\n2. 使用内置函数优化:")
    use_builtins()
    
    print("\n3. 使用缓存优化:")
    use_caching()
    
    print("\n4. 使用 numpy/pandas:")
    use_numpy_pandas()
    
    print("\n" + "=" * 60)
    print("所有示例运行完成")
    print("=" * 60)
