import numpy as np
import time

def memory_test(size_in_mb):
    # 计算需要分配的字节数
    size_in_bytes = size_in_mb * 1024 * 1024
    
    # 测试内存分配
    print(f"开始分配 {size_in_mb} MB 的内存...")
    start_time = time.time()
    data = np.random.rand(size_in_mb * 1024 * 1024 // 8)  # 创建一个大小为 size_in_mb 的 numpy 数组
    end_time = time.time()
    allocation_time = end_time - start_time
    print(f"内存分配完成, 耗时 {allocation_time:.4f} 秒")
    print(f"内存分配速度: {size_in_mb / allocation_time:.2f} MB/s")

    # 测试内存写入
    print(f"开始写入数据到内存...")
    start_time = time.time()
    data[:] = np.random.rand(len(data))  # 用新的随机数填充数据
    end_time = time.time()
    write_time = end_time - start_time
    print(f"内存写入完成, 耗时 {write_time:.4f} 秒")
    print(f"内存写入速度: {size_in_mb / write_time:.2f} MB/s")

    # 测试内存读取
    print(f"开始读取数据...")
    start_time = time.time()
    data_sum = np.sum(data)  # 读取数据进行计算
    end_time = time.time()
    read_time = end_time - start_time
    print(f"内存读取完成, 耗时 {read_time:.4f} 秒")
    print(f"内存读取速度: {size_in_mb / read_time:.2f} MB/s")
    
    # 释放内存
    del data
    print(f"内存已释放。\n")
    
    return data_sum

# 设置测试的内存大小（以 MB 为单位）
memory_size_mb = 1000  # 比如测试 100MB 内存

memory_test(memory_size_mb)
