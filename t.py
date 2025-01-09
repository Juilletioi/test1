import os
import sys
from pathlib import Path

class Node:
    def __init__(self, rel_addr, map_addr):
        self.rel_addr = rel_addr  # 节点的数据
        self.map_addr = map_addr
        self.next = None  # 指向下一个节点的指针，默认为None


class addr_list:
    def __init__(self):
        self.head = None

    def append(self, rel_addr, map_addr):
        new_node = Node(rel_addr, map_addr)  # 创建一个新节点
        if not self.head:  # 如果链表为空
            self.head = new_node  # 将新节点设置为头节点
            return
        last = self.head
        while last.next:  # 遍历到链表的最后一个节点
            last = last.next
        last.next = new_node  # 将新节点连接到链表末尾

def init_addr_map(page_size):
# 生成一个地址映射表
    list_num = 0x40000000 / page_size
    map_list = addr_list()
    for i in list_num:
        if (i % 2 == 0):
            map_list.append(i*page_size, i*page_size)
        else:
            map_list.append(i*page_size + 0x20000000, i*page_size)


def split_bin_file(input_file, chunk_size, start_addr):
    # 检查文件是否存在
    if not os.path.exists(input_file):
        print(f"file {input_file} not exit!")
        return
    file_path = "{}_interleave_file" .format(input_file)
    try:
        os.makedirs(file_path)
        print(f"dir '{file_path}' craete success")
    except FileExistsError:
        print(f"dir '{file_path}' exit")
    except Exception as e:
        print(f"mkdir err: {e}") 
    # 获取文件的大小
    file_size = os.path.getsize(input_file)
    
    # 计算需要分割的份数
    num_chunks = (file_size + chunk_size - 1) // chunk_size  # 向上取整
    if (start_addr % chunk_size != 0):
        print("please set start address align to interleave size")
        return
    
    print(f"file_size：{file_size} bytes")
    print(f"interleaver {num_chunks} parts，each size：{chunk_size} bytes")

    # 打开源文件
    with open(input_file, 'rb') as f:
        with open(f'{input_file}_load_ddr.tcl', 'w+', encoding='utf-8') as file:
            for i in range(num_chunks):
                # 计算当前分块的开始位置和结束位置
                start = i * chunk_size
                end = min((i + 1) * chunk_size, file_size)
                chunk_data = f.read(end - start)
                ddr_block = i % 2
                print(ddr_block)
                
                # 创建分块文件
                chunk_filename = f"{file_path}\{input_file}.part{i + 1}" 
                if ddr_block == 0:
                    ddr0_start = int(start / 16) + int(start_addr/16)
                    text = "memory -load %pd_raw2 gc2_tb_top.gc2_chip_inst.u_ddr{}_subsys.u_ddr_subsys.u_axisram_DDR.u_blkmem.RAM -file {} -start {} -little_endian -nofill\n"  .format(ddr_block, chunk_filename, hex(ddr0_start))
                else:
                    ddr1_start = int(((i -1) * chunk_size) / 16) + int(start_addr/16)
                    text = "memory -load %pd_raw2 gc2_tb_top.gc2_chip_inst.u_ddr{}_subsys.u_ddr_subsys.u_axisram_DDR.u_blkmem.RAM -file {} -start {} -little_endian -nofill\n"  .format(ddr_block, chunk_filename, hex(ddr1_start))
                with open(chunk_filename, 'wb') as chunk_file:
                    chunk_file.write(chunk_data)
                file.write(text)
       
                print(f"ready create file: {chunk_filename}, size: {len(chunk_data)} bytes")

if __name__ == "__main__":
    input_file = sys.argv[1]
    chunk_size = int(sys.argv[2])
    start_addr = int(sys.argv[3], 16)
    split_bin_file(input_file, int(chunk_size), start_addr)
