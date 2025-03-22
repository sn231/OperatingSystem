import tkinter as tk
from tkinter import ttk
from gui import MemoryManagementGUI

def main():
    root = tk.Tk()
    root.title("内存管理模拟系统")
    root.geometry("1200x800")
    
    app = MemoryManagementGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 