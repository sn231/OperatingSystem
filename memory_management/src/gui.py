import tkinter as tk
from tkinter import ttk, messagebox
from partition_manager import PartitionManager
from page_manager import PageManager
import time

class MemoryManagementGUI:
    def __init__(self, root):
        self.root = root
        self.partition_manager = PartitionManager()
        self.page_manager = PageManager()
        
        # 创建标签页
        self.notebook = ttk.Notebook(root)
        self.partition_frame = ttk.Frame(self.notebook)
        self.page_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.partition_frame, text="动态分区管理")
        self.notebook.add(self.page_frame, text="动态分页管理")
        self.notebook.pack(expand=True, fill="both", padx=10, pady=5)
        
        self._setup_partition_page()
        self._setup_page_management_page()
    
    def _setup_partition_page(self):
        # 分区管理控制面板
        control_frame = ttk.LabelFrame(self.partition_frame, text="控制面板")
        control_frame.pack(fill="x", padx=5, pady=5)
        
        # 作业输入区域
        ttk.Label(control_frame, text="作业名称:").grid(row=0, column=0, padx=5, pady=5)
        self.job_name = tk.StringVar(value="JOB1")
        ttk.Entry(control_frame, textvariable=self.job_name).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(control_frame, text="作业大小(KB):").grid(row=0, column=2, padx=5, pady=5)
        self.job_size = tk.StringVar(value="12")
        ttk.Entry(control_frame, textvariable=self.job_size).grid(row=0, column=3, padx=5, pady=5)
        
        # 分配算法选择
        self.alloc_algorithm = tk.StringVar(value="first_fit")
        ttk.Radiobutton(control_frame, text="首次适应", variable=self.alloc_algorithm, 
                       value="first_fit").grid(row=1, column=0, padx=5, pady=5)
        ttk.Radiobutton(control_frame, text="最佳适应", variable=self.alloc_algorithm, 
                       value="best_fit").grid(row=1, column=1, padx=5, pady=5)
        ttk.Radiobutton(control_frame, text="最坏适应", variable=self.alloc_algorithm, 
                       value="worst_fit").grid(row=1, column=2, padx=5, pady=5)
        
        # 操作按钮
        ttk.Button(control_frame, text="分配内存", 
                  command=self._allocate_memory).grid(row=1, column=3, padx=5, pady=5)
        ttk.Button(control_frame, text="释放内存", 
                  command=self._release_memory).grid(row=1, column=4, padx=5, pady=5)
        
        # 分区状态显示
        status_frame = ttk.LabelFrame(self.partition_frame, text="分区状态")
        status_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # 创建树形视图
        columns = ("size", "start_address", "status", "job")
        self.partition_tree = ttk.Treeview(status_frame, columns=columns, show="headings")
        
        # 设置列标题
        self.partition_tree.heading("size", text="分区大小(KB)")
        self.partition_tree.heading("start_address", text="起始地址(KB)")
        self.partition_tree.heading("status", text="状态")
        self.partition_tree.heading("job", text="作业名")
        
        # 设置列宽
        for col in columns:
            self.partition_tree.column(col, width=120, anchor="center")
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(status_frame, orient="vertical", 
                                command=self.partition_tree.yview)
        self.partition_tree.configure(yscrollcommand=scrollbar.set)
        
        self.partition_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 更新显示
        self._update_partition_display()
    
    def _setup_page_management_page(self):
        # 页面管理控制面板
        control_frame = ttk.LabelFrame(self.page_frame, text="控制面板")
        control_frame.pack(fill="x", padx=5, pady=5)
        
        # 内存访问控制
        ttk.Label(control_frame, text="页号:").grid(row=0, column=0, padx=5, pady=5)
        self.page_number = tk.StringVar(value="0")
        ttk.Entry(control_frame, textvariable=self.page_number).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(control_frame, text="页内偏移:").grid(row=0, column=2, padx=5, pady=5)
        self.page_offset = tk.StringVar(value="072")
        ttk.Entry(control_frame, textvariable=self.page_offset).grid(row=0, column=3, padx=5, pady=5)
        
        # 操作类型
        self.operation_type = tk.StringVar(value="read")
        ttk.Radiobutton(control_frame, text="读取", variable=self.operation_type, 
                       value="read").grid(row=1, column=0, padx=5, pady=5)
        ttk.Radiobutton(control_frame, text="写入", variable=self.operation_type, 
                       value="write").grid(row=1, column=1, padx=5, pady=5)
        
        # 访问内存按钮
        ttk.Button(control_frame, text="访问内存", 
                  command=self._access_memory).grid(row=1, column=3, padx=5, pady=5)
        
        # 页表状态显示
        status_frame = ttk.LabelFrame(self.page_frame, text="页表状态")
        status_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # 创建树形视图
        columns = ("page_num", "present", "frame_num", "modified", "disk_pos")
        self.page_tree = ttk.Treeview(status_frame, columns=columns, show="headings")
        
        # 设置列标题
        self.page_tree.heading("page_num", text="页号")
        self.page_tree.heading("present", text="存在位")
        self.page_tree.heading("frame_num", text="内存块号")
        self.page_tree.heading("modified", text="修改位")
        self.page_tree.heading("disk_pos", text="磁盘位置")
        
        # 设置列宽
        for col in columns:
            self.page_tree.column(col, width=100, anchor="center")
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(status_frame, orient="vertical", 
                                command=self.page_tree.yview)
        self.page_tree.configure(yscrollcommand=scrollbar.set)
        
        self.page_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 访问日志显示
        log_frame = ttk.LabelFrame(self.page_frame, text="访问日志")
        log_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.log_text = tk.Text(log_frame, height=10)
        self.log_text.pack(fill="both", expand=True)
        
        # 更新显示
        self._update_page_table_display()
    
    def _allocate_memory(self):
        try:
            job_name = self.job_name.get()
            size = int(self.job_size.get()) * 1024  # 转换为字节
            algorithm = self.alloc_algorithm.get()
            
            success = False
            if algorithm == "first_fit":
                success = self.partition_manager.first_fit(job_name, size)
            elif algorithm == "best_fit":
                success = self.partition_manager.best_fit(job_name, size)
            else:  # worst_fit
                success = self.partition_manager.worst_fit(job_name, size)
            
            if success:
                messagebox.showinfo("成功", f"成功为作业 {job_name} 分配 {size//1024}KB 内存")
            else:
                messagebox.showerror("失败", "内存分配失败，没有足够的连续空间")
            
            self._update_partition_display()
            
        except ValueError as e:
            messagebox.showerror("错误", str(e))
    
    def _release_memory(self):
        job_name = self.job_name.get()
        if self.partition_manager.release(job_name):
            messagebox.showinfo("成功", f"成功释放作业 {job_name} 的内存")
        else:
            messagebox.showerror("失败", f"未找到作业 {job_name} 占用的内存")
        
        self._update_partition_display()
    
    def _access_memory(self):
        try:
            page_num = int(self.page_number.get())
            offset = int(self.page_offset.get())
            is_write = self.operation_type.get() == "write"
            
            physical_addr, page_fault, replacement_info = self.page_manager.access_memory(
                page_num, offset, is_write)
            
            # 更新日志
            log_msg = f"访问页面 {page_num}，偏移量 {offset}，"
            if page_fault:
                if replacement_info:
                    victim_page, frame = replacement_info
                    log_msg += f"发生缺页中断，置换出页面 {victim_page}"
                else:
                    log_msg += "发生缺页中断，使用空闲帧"
            else:
                log_msg += "页面已在内存中"
            log_msg += f"，物理地址：{physical_addr}\n"
            
            self.log_text.insert("1.0", log_msg)
            self._update_page_table_display()
            
        except ValueError as e:
            messagebox.showerror("错误", str(e))
    
    def _update_partition_display(self):
        # 清除现有显示
        for item in self.partition_tree.get_children():
            self.partition_tree.delete(item)
        
        # 获取并显示分区状态
        for size, start_addr, is_allocated, job_name in self.partition_manager.get_partition_status():
            status = "已分配" if is_allocated else "空闲"
            self.partition_tree.insert("", "end", values=(
                size//1024,  # 转换为KB
                start_addr//1024,
                status,
                job_name if is_allocated else ""
            ))
    
    def _update_page_table_display(self):
        # 清除现有显示
        for item in self.page_tree.get_children():
            self.page_tree.delete(item)
        
        # 获取并显示页表状态
        for page_num, present, frame_num, modified, disk_pos in self.page_manager.get_page_table_status():
            self.page_tree.insert("", "end", values=(
                page_num,
                "是" if present else "否",
                frame_num if frame_num is not None else "-",
                "是" if modified else "否",
                disk_pos
            )) 