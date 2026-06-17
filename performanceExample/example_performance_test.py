"""
性能测试示例 - pytest 性能测试模板

用于测试大量数据场景下的性能表现
"""
import time
import pytest
from typing import List, Dict

# ==================== 测试数据生成 ====================
def generate_large_dataset(size: int) -> List[Dict]:
    """生成大型测试数据集"""
    return [
        {
            "id": i,
            "name": f"item_{i:06d}",
            "value": i * 2.5,
            "active": i % 3 == 0,
            "tags": [f"tag_{j}" for j in range(min(i, 5))]
        }
        for i in range(size)
    ]

# ==================== 被测函数 ====================
def process_large_dataset(data: List[Dict]) -> Dict:
    """处理大型数据集的示例函数"""
    result = {
        "total_count": 0,
        "active_count": 0,
        "sum_value": 0.0,
        "tag_counts": {}
    }
    
    for item in data:
        result["total_count"] += 1
        if item["active"]:
            result["active_count"] += 1
        result["sum_value"] += item["value"]
        
        for tag in item["tags"]:
            result["tag_counts"][tag] = result["tag_counts"].get(tag, 0) + 1
    
    return result

# ==================== 性能测试用例 ====================
class TestPerformance:
    """性能测试类"""
    
    def test_small_dataset_performance(self):
        """测试小型数据集 (1000 条)"""
        data = generate_large_dataset(1000)
        
        start = time.time()
        result = process_large_dataset(data)
        elapsed = time.time() - start
        
        assert result["total_count"] == 1000
        print(f"Small dataset (1000): {elapsed:.4f}s")
        
        # 性能断言：处理 1000 条数据应在 0.1 秒内完成
        assert elapsed < 0.1, f"Performance exceeded: {elapsed:.4f}s"
    
    def test_medium_dataset_performance(self):
        """测试中型数据集 (10000 条)"""
        data = generate_large_dataset(10000)
        
        start = time.time()
        result = process_large_dataset(data)
        elapsed = time.time() - start
        
        assert result["total_count"] == 10000
        print(f"Medium dataset (10000): {elapsed:.4f}s")
        
        # 性能断言：处理 10000 条数据应在 1 秒内完成
        assert elapsed < 1.0, f"Performance exceeded: {elapsed:.4f}s"
    
    def test_large_dataset_performance(self):
        """测试大型数据集 (100000 条)"""
        data = generate_large_dataset(100000)
        
        start = time.time()
        result = process_large_dataset(data)
        elapsed = time.time() - start
        
        assert result["total_count"] == 100000
        print(f"Large dataset (100000): {elapsed:.4f}s")
        
        # 性能断言：处理 100000 条数据应在 10 秒内完成
        assert elapsed < 10.0, f"Performance exceeded: {elapsed:.4f}s"
    
    def test_multiple_iterations(self):
        """多次执行取平均值"""
        data = generate_large_dataset(10000)
        iterations = 5
        total_time = 0
        
        for i in range(iterations):
            start = time.time()
            process_large_dataset(data)
            elapsed = time.time() - start
            total_time += elapsed
            print(f"Iteration {i+1}: {elapsed:.4f}s")
        
        avg_time = total_time / iterations
        print(f"Average time: {avg_time:.4f}s")
        
        assert avg_time < 0.8, f"Average performance exceeded: {avg_time:.4f}s"

# ==================== 内存使用测试 ====================
def test_memory_usage():
    """测试内存使用情况"""
    import sys
    
    # 生成数据前的内存参考
    data = generate_large_dataset(10000)
    
    # 计算列表占用的内存
    total_size = sum(sys.getsizeof(item) for item in data)
    print(f"Memory usage for 10000 items: {total_size / 1024 / 1024:.2f} MB")
    
    # 清理
    del data

# ==================== API 响应时间测试 ====================
def test_api_response_time():
    """测试 API 响应时间"""
    import requests
    
    url = "https://fangdong.fun/login"
    
    start = time.time()
    response = requests.get(url)
    elapsed = time.time() - start
    
    assert response.status_code == 200
    print(f"API response time: {elapsed:.4f}s")
    
    # 断言响应时间小于 2 秒
    assert elapsed < 2.0, f"API response time exceeded: {elapsed:.4f}s"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
