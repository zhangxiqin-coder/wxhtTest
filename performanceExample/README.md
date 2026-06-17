# 性能测试示例

本目录包含处理大量数据时的推荐写法和性能测试示例。

## 目录结构

```
performanceExample/
├── README.md                      # 说明文档
├── best_practices.md              # 性能测试最佳实践
├── data_processing_examples.py    # 数据处理推荐写法
├── file_io_examples.py            # 文件读写高效写法
├── parallel_processing_examples.py # 并行处理示例
├── example_performance_test.py    # pytest 性能测试示例
├── locust_example.py              # Locust 负载测试示例
└── selenium_performance.py        # Selenium 性能测试示例
```

## 核心示例说明

### 1. 数据处理推荐写法 (data_processing_examples.py)

| 技术 | 适用场景 |
|------|----------|
| 生成器 | 处理超过内存限制的数据集 |
| 批量处理 | 数据库批量插入、API批量调用 |
| itertools | 高效处理迭代操作 |
| lru_cache | 缓存重复计算结果 |
| numpy/pandas | 大量数值计算、数据分析 |

### 2. 文件读写高效写法 (file_io_examples.py)

| 技术 | 适用场景 |
|------|----------|
| 逐行读取 | 处理大型日志文件 |
| 批量写入 | 大量数据写入，减少IO次数 |
| CSV模块 | 大型CSV数据处理 |
| JSON Lines | 大量数据序列化为JSON |
| gzip压缩 | 压缩的大型文件存储 |
| 内存映射 | 处理超大文件 |

### 3. 并行处理示例 (parallel_processing_examples.py)

| 技术 | 适用场景 |
|------|----------|
| ThreadPoolExecutor | IO密集型操作（网络请求、文件读写） |
| ProcessPoolExecutor | CPU密集型操作（数值计算） |
| asyncio | 高并发IO操作 |
| 生产者-消费者模式 | 流式数据处理 |

## 运行示例

```bash
# 运行数据处理示例
python performanceExample/data_processing_examples.py

# 运行文件读写示例
python performanceExample/file_io_examples.py

# 运行并行处理示例
python performanceExample/parallel_processing_examples.py

# 运行 pytest 性能测试
pytest performanceExample/example_performance_test.py -v

# 运行 Locust 负载测试
locust -f performanceExample/locust_example.py --host=https://fangdong.fun

# 运行 Selenium 性能测试
python performanceExample/selenium_performance.py
```

## 性能指标关注

- **响应时间** (Response Time)
- **吞吐量** (Throughput)
- **并发用户数** (Concurrent Users)
- **错误率** (Error Rate)
- **资源使用率** (CPU/Memory/Network)