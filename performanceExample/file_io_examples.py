"""
文件读写高效写法示例

本文件包含处理大量文件和数据时的最佳实践
"""

import os
import csv
import json
import gzip
from typing import Generator


# ==================== 1. 逐行读取大文件 ====================
def read_large_file_line_by_line(file_path: str) -> Generator[str, None, None]:
    """
    逐行读取大文件，避免一次性加载到内存
    
    推荐场景：处理超过内存限制的大文件（如日志文件）
    """
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            yield line.strip()


def process_large_log_file(file_path: str):
    """处理大型日志文件"""
    error_count = 0
    
    for line in read_large_file_line_by_line(file_path):
        if "ERROR" in line:
            error_count += 1
            # 处理错误日志
            process_error(line)
    
    print(f"Found {error_count} errors")


def process_error(line: str):
    """处理错误日志"""
    # 示例处理逻辑
    pass


# ==================== 2. 批量写入文件 ====================
def write_data_in_batches(data: list, file_path: str, batch_size: int = 1000):
    """
    批量写入数据到文件
    
    推荐场景：大量数据写入，减少IO次数
    """
    with open(file_path, "w", encoding="utf-8") as f:
        for i in range(0, len(data), batch_size):
            batch = data[i:i + batch_size]
            # 批量写入
            lines = "\n".join(str(item) for item in batch) + "\n"
            f.write(lines)


# ==================== 3. 使用 csv 模块处理 CSV 文件 ====================
def read_csv_efficiently(file_path: str):
    """
    高效读取 CSV 文件
    
    推荐场景：大型 CSV 数据处理
    """
    with open(file_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            # 逐行处理，避免一次性加载
            process_csv_row(row)


def write_csv_efficiently(data: list, file_path: str):
    """
    高效写入 CSV 文件
    
    推荐场景：大量数据导出为 CSV
    """
    if not data:
        return
    
    # 获取表头
    headers = data[0].keys()
    
    with open(file_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        
        # 批量写入
        for i in range(0, len(data), 1000):
            batch = data[i:i + 1000]
            writer.writerows(batch)


# ==================== 4. 处理 JSON 数据 ====================
def read_json_large_file(file_path: str):
    """
    读取大型 JSON 文件
    
    推荐场景：JSON Lines 格式的大文件
    """
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                obj = json.loads(line)
                yield obj


def write_json_lines(data: list, file_path: str):
    """
    写入 JSON Lines 格式文件
    
    推荐场景：大量数据序列化为 JSON
    """
    with open(file_path, "w", encoding="utf-8") as f:
        for item in data:
            json_line = json.dumps(item, ensure_ascii=False)
            f.write(json_line + "\n")


# ==================== 5. 使用压缩文件 ====================
def read_gzip_file(file_path: str):
    """
    读取 gzip 压缩文件
    
    推荐场景：压缩的大型日志或数据文件
    """
    with gzip.open(file_path, "rt", encoding="utf-8") as f:
        for line in f:
            yield line.strip()


def write_gzip_file(data: list, file_path: str):
    """
    写入 gzip 压缩文件
    
    推荐场景：大量数据压缩存储
    """
    with gzip.open(file_path, "wt", encoding="utf-8") as f:
        for item in data:
            f.write(str(item) + "\n")


# ==================== 6. 目录遍历优化 ====================
def walk_directory(root_dir: str) -> Generator[str, None, None]:
    """
    高效遍历目录树
    
    推荐场景：扫描大量文件的目录结构
    """
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # 过滤掉隐藏目录
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        
        for filename in filenames:
            yield os.path.join(dirpath, filename)


def count_files_by_extension(root_dir: str):
    """统计目录中各类型文件数量"""
    extension_counts = {}
    
    for filepath in walk_directory(root_dir):
        _, ext = os.path.splitext(filepath)
        extension_counts[ext] = extension_counts.get(ext, 0) + 1
    
    for ext, count in sorted(extension_counts.items()):
        print(f"{ext}: {count} files")


# ==================== 7. 使用临时文件 ====================
def use_temp_file():
    """
    使用临时文件处理中间数据
    
    推荐场景：处理过程中产生大量临时数据
    """
    import tempfile
    
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as f:
        # 写入临时数据
        for i in range(10000):
            f.write(f"line_{i}\n")
        
        temp_path = f.name
    
    try:
        # 处理临时文件
        with open(temp_path, "r") as f:
            lines = f.readlines()
            print(f"Temp file has {len(lines)} lines")
    finally:
        # 清理临时文件
        os.unlink(temp_path)


# ==================== 8. 内存映射文件 ====================
def use_memory_map(file_path: str):
    """
    使用内存映射文件处理超大文件
    
    推荐场景：处理超过内存限制的超大文件（如几GB）
    """
    import mmap
    
    with open(file_path, "r+b") as f:
        # 创建内存映射
        with mmap.mmap(f.fileno(), length=0, access=mmap.ACCESS_READ) as mm:
            # 查找内容
            if mm.find(b"ERROR") != -1:
                print("Found ERROR in file")
            
            # 读取指定位置
            content = mm[100:200].decode("utf-8")
            print(f"Content at position 100-200: {content}")


# ==================== 示例运行 ====================
if __name__ == "__main__":
    print("=" * 60)
    print("文件读写高效写法示例")
    print("=" * 60)
    
    # 创建测试数据
    test_data = [{"id": i, "name": f"item_{i}"} for i in range(1000)]
    
    # 示例：写入 CSV
    write_csv_efficiently(test_data, "test_output.csv")
    print("\n1. CSV 写入完成")
    
    # 示例：写入 JSON Lines
    write_json_lines(test_data, "test_output.jsonl")
    print("2. JSON Lines 写入完成")
    
    # 示例：目录遍历
    print("\n3. 目录文件统计:")
    count_files_by_extension(".")
    
    # 示例：临时文件
    print("\n4. 临时文件示例:")
    use_temp_file()
    
    print("\n" + "=" * 60)
    print("所有示例运行完成")
    print("=" * 60)
