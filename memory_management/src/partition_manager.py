from dataclasses import dataclass
from typing import List, Optional, Tuple

@dataclass
class Partition:
    size: int
    start_address: int
    is_allocated: bool = False
    job_name: str = ""

class PartitionManager:
    def __init__(self):
        # 初始化空闲分区列表
        self.partitions = [
            Partition(35*1024, 100*1024),  # 35KB, 起始地址100KB
            Partition(12*1024, 156*1024),  # 12KB, 起始地址156KB
            Partition(28*1024, 200*1024)   # 28KB, 起始地址200KB
        ]
    
    def first_fit(self, job_name: str, size: int) -> bool:
        """首次适应算法"""
        for i, partition in enumerate(self.partitions):
            if not partition.is_allocated and partition.size >= size:
                # 分割分区
                if partition.size > size:
                    new_partition = Partition(
                        partition.size - size,
                        partition.start_address + size
                    )
                    self.partitions.insert(i + 1, new_partition)
                    partition.size = size
                
                partition.is_allocated = True
                partition.job_name = job_name
                return True
        return False
    
    def best_fit(self, job_name: str, size: int) -> bool:
        """最佳适应算法"""
        best_fit_index = -1
        min_fragment = float('inf')
        
        for i, partition in enumerate(self.partitions):
            if not partition.is_allocated and partition.size >= size:
                fragment = partition.size - size
                if fragment < min_fragment:
                    min_fragment = fragment
                    best_fit_index = i
        
        if best_fit_index != -1:
            partition = self.partitions[best_fit_index]
            if partition.size > size:
                new_partition = Partition(
                    partition.size - size,
                    partition.start_address + size
                )
                self.partitions.insert(best_fit_index + 1, new_partition)
                partition.size = size
            
            partition.is_allocated = True
            partition.job_name = job_name
            return True
        return False
    
    def worst_fit(self, job_name: str, size: int) -> bool:
        """最坏适应算法"""
        worst_fit_index = -1
        max_fragment = -1
        
        for i, partition in enumerate(self.partitions):
            if not partition.is_allocated and partition.size >= size:
                fragment = partition.size - size
                if fragment > max_fragment:
                    max_fragment = fragment
                    worst_fit_index = i
        
        if worst_fit_index != -1:
            partition = self.partitions[worst_fit_index]
            if partition.size > size:
                new_partition = Partition(
                    partition.size - size,
                    partition.start_address + size
                )
                self.partitions.insert(worst_fit_index + 1, new_partition)
                partition.size = size
            
            partition.is_allocated = True
            partition.job_name = job_name
            return True
        return False
    
    def release(self, job_name: str) -> bool:
        """释放作业占用的内存并合并相邻空闲分区"""
        found = False
        i = 0
        while i < len(self.partitions):
            if self.partitions[i].job_name == job_name:
                self.partitions[i].is_allocated = False
                self.partitions[i].job_name = ""
                found = True
                
                # 向前合并
                if i > 0 and not self.partitions[i-1].is_allocated:
                    self.partitions[i-1].size += self.partitions[i].size
                    self.partitions.pop(i)
                    i -= 1
                
                # 向后合并
                if i < len(self.partitions)-1 and not self.partitions[i+1].is_allocated:
                    self.partitions[i].size += self.partitions[i+1].size
                    self.partitions.pop(i+1)
            i += 1
        return found
    
    def get_partition_status(self) -> List[Tuple[int, int, bool, str]]:
        """获取所有分区的状态"""
        return [(p.size, p.start_address, p.is_allocated, p.job_name) 
                for p in self.partitions] 