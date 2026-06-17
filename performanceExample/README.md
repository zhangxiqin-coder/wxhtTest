# 性能测试示例

本目录包含性能测试的示例代码和最佳实践，用于处理大量数据和高并发场景。

## 目录结构

```
performanceExample/
├── README.md              # 说明文档
├── best_practices.md      # 性能测试最佳实践
├── example_performance_test.py  # pytest 性能测试示例
├── locust_example.py      # Locust 负载测试示例
└── selenium_performance.py # Selenium 性能测试示例
```

## 性能测试类型

| 类型 | 工具 | 用途 |
|------|------|------|
| 单元性能测试 | pytest + timeit | 测试单个函数/方法的执行时间 |
| 负载测试 | Locust | 模拟大量并发用户 |
| UI 性能测试 | Selenium | 测试页面加载时间 |
| API 性能测试 | Locust/requests | 测试接口响应时间 |

## 运行示例

```bash
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