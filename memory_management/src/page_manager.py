from dataclasses import dataclass
from typing import List, Optional, Dict
from collections import deque

@dataclass
class PageTableEntry:
    page_number: int
    present: bool = False
    frame_number: Optional[int] = None
    modified: bool = False
    disk_position: str = ""

class PageManager:
    def __init__(self, total_frames: int = 4):
        self.PAGE_SIZE = 1024  # 1KB
        self.total_frames = total_frames
        self.allocated_frames: List[Optional[int]] = [None] * total_frames
        self.page_table: List[PageTableEntry] = []
        self.frame_queue = deque()  # 用于FIFO页面置换
        
        # 初始化页表
        self.initialize_page_table()
    
    def initialize_page_table(self):
        """初始化页表"""
        initial_pages = [
            (0, True, 5, False, "010"),
            (1, True, 8, False, "012"),
            (2, True, 9, False, "013"),
            (3, True, 1, False, "021"),
            (4, False, None, False, "022"),
            (5, False, None, False, "023"),
            (6, False, None, False, "125")
        ]
        
        self.page_table = []
        for page_num, present, frame_num, modified, disk_pos in initial_pages:
            entry = PageTableEntry(
                page_number=page_num,
                present=present,
                frame_number=frame_num if present else None,
                modified=modified,
                disk_position=disk_pos
            )
            self.page_table.append(entry)
            if present:
                self.frame_queue.append(page_num)
    
    def access_memory(self, page_number: int, offset: int, is_write: bool = False) -> tuple[int, bool, Optional[tuple]]:
        """
        访问内存
        返回：(物理地址, 是否发生缺页, 页面置换信息)
        """
        if page_number >= len(self.page_table):
            raise ValueError(f"页号 {page_number} 超出范围")
        
        if offset >= self.PAGE_SIZE:
            raise ValueError(f"页内偏移 {offset} 超出范围")
        
        page = self.page_table[page_number]
        page_fault = False
        replacement_info = None
        
        if not page.present:
            page_fault = True
            # 需要进行页面置换
            if len(self.frame_queue) >= self.total_frames:
                # 执行FIFO页面置换
                victim_page_num = self.frame_queue.popleft()
                victim_page = self.page_table[victim_page_num]
                old_frame = victim_page.frame_number
                replacement_info = (victim_page_num, old_frame)
                
                # 更新被置换出去的页面
                victim_page.present = False
                victim_page.frame_number = None
                
                # 将新页面放入该帧
                page.frame_number = old_frame
            else:
                # 还有空闲帧，找到一个空闲帧
                used_frames = set(p.frame_number for p in self.page_table if p.present)
                for i in range(self.total_frames):
                    if i not in used_frames:
                        page.frame_number = i
                        break
            
            page.present = True
            self.frame_queue.append(page_number)
        
        if is_write:
            page.modified = True
        
        # 计算物理地址
        physical_address = (page.frame_number * self.PAGE_SIZE) + offset
        
        return physical_address, page_fault, replacement_info
    
    def get_page_table_status(self) -> List[tuple]:
        """获取页表状态"""
        return [(p.page_number, p.present, p.frame_number, 
                 p.modified, p.disk_position) for p in self.page_table] 