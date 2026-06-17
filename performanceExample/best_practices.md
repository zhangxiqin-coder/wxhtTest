# 性能测试最佳实践

## 1. 测试环境准备

- 使用与生产环境相似的硬件配置
- 确保测试环境隔离，避免其他负载干扰
- 测试前清理缓存和日志

## 2. 测试数据准备

```python
# 生成大量测试数据
def generate_test_data(size: int):
    """生成指定大小的测试数据"""
    return [{"id": i, "name": f"item_{i}"} for i in range(size)]
```

## 3. 单元性能测试

```python
# 使用 timeit 装饰器
import time

def measure_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"{func.__name__} took {elapsed:.4f} seconds")
        return result
    return wrapper
```

## 4. 避免常见陷阱

### 陷阱 1: 忽略初始化时间

```python
# 错误做法
def test_performance():
    data = generate_large_data()  # 初始化时间被计入
    start = time.time()
    process_data(data)
    elapsed = time.time() - start

# 正确做法
def test_performance():
    data = generate_large_data()  # 初始化在计时外
    start = time.time()
    process_data(data)
    elapsed = time.time() - start
```

### 陷阱 2: 单次测试不可靠

```python
# 正确做法：多次执行取平均值
def test_performance():
    data = generate_large_data()
    total_time = 0
    iterations = 10
    
    for _ in range(iterations):
        start = time.time()
        process_data(data)
        total_time += time.time() - start
    
    avg_time = total_time / iterations
    print(f"Average time: {avg_time:.4f}s")
```

### 陷阱 3: 忽略垃圾回收

```python
import gc

def test_performance():
    gc.collect()  # 测试前执行垃圾回收
    gc.disable()  # 测试期间禁用垃圾回收
    
    start = time.time()
    process_data()
    elapsed = time.time() - start
    
    gc.enable()  # 恢复垃圾回收
```

## 5. 性能测试断言

```python
def test_api_response_time():
    response = requests.get("https://api.example.com/data")
    
    # 断言响应时间小于 200ms
    assert response.elapsed.total_seconds() < 0.2, \
        f"Response time {response.elapsed.total_seconds():.4f}s exceeds 0.2s"
```

## 6. 性能测试工具推荐

| 工具 | 用途 | 安装 |
|------|------|------|
| pytest-benchmark | pytest 性能基准测试 | `pip install pytest-benchmark` |
| Locust | 负载测试 | `pip install locust` |
| cProfile | Python 内置性能分析 | 内置 |
| line_profiler | 行级性能分析 | `pip install line_profiler` |

## 7. 性能优化技巧

### 数据处理优化

```python
# 避免在循环中重复计算
def process_items(items):
    # 预计算常量
    threshold = calculate_threshold()
    
    # 使用生成器减少内存
    results = (process_item(item, threshold) for item in items)
    
    # 批量操作
    return batch_save(results)
```

### 数据库优化

```python
# 使用批量插入
def bulk_insert(data):
    # 避免逐条插入
    with db.session.begin():
        db.session.add_all(data)
    db.session.commit()
```

### 缓存策略

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_computation(param):
    # 缓存计算结果
    return compute(param)
```

## 8. 性能测试报告

测试完成后生成报告，包含：
- 测试环境配置
- 测试数据规模
- 响应时间分布
- 吞吐量统计
- 资源使用情况
- 性能瓶颈分析