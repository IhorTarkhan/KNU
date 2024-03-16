import tkinter as tk
from tkinter import Listbox, Scrollbar
import os
import time

def format_size(size):
    for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"

class FileSystemViewer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File System Navigator")
        self.geometry("1000x600")

        self.path_label = tk.Label(self, text="No folder selected", anchor="w")
        self.path_label.grid(row=0, column=0, columnspan=2, sticky='ew', padx=10, pady=5)

        self.main_frame = tk.Frame(self)
        self.main_frame.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=10, pady=5)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.listbox = Listbox(self.main_frame)
        self.listbox.grid(row=0, column=0, sticky='nsew')
        self.listbox.bind('<Double-1>', self.on_item_double_click)
        self.listbox.bind('<<ListboxSelect>>', self.on_item_select)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.info_frame = tk.Frame(self.main_frame)
        self.info_frame.grid(row=0, column=1, sticky='nsew')
        self.main_frame.grid_columnconfigure(1, weight=1)

        self.name_label = tk.Label(self.info_frame, text="")
        self.name_label.pack(fill=tk.X)

        self.extra_label = tk.Label(self.info_frame, text="")
        self.extra_label.pack(fill=tk.X)

        self.content_label = tk.Label(self.info_frame, text="Content:")
        self.content_text = tk.Text(self.info_frame, height=10, state='disabled')
        self.content_scroll = Scrollbar(self.info_frame, command=self.content_text.yview)
        self.content_text.configure(yscrollcommand=self.content_scroll.set)

        self.current_path = os.path.dirname(os.path.abspath(__file__))
        self.list_directory(self.current_path)

    def list_directory(self, path):
        self.listbox.delete(0, tk.END)
        self.listbox.insert(tk.END, "..")
        self.path_label.config(text=path)
        self.current_path = path
        for item in os.listdir(path):
            self.listbox.insert(tk.END, item)

    def on_item_double_click(self, event):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            item = self.listbox.get(index)
            if item == "..":
                new_path = os.path.dirname(self.current_path)
            else:
                new_path = os.path.join(self.current_path, item)
            if os.path.isdir(new_path):
                self.list_directory(new_path)

    def on_item_select(self, event):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            item = self.listbox.get(index)
            if item != "..":
                new_path = os.path.join(self.current_path, item)
                self.update_info(new_path, item)
            else:
                self.clear_info()

    def update_info(self, new_path, item):
        self.name_label.config(text=f"Name: {item}")
        if os.path.isdir(new_path):
            self.extra_label.config(text=f"Top Folder: {os.path.basename(os.path.dirname(new_path))}")
            self.content_label.pack_forget()
            self.content_text.pack_forget()
        else:
            self.extra_label.config(text=f"Size: {format_size(os.path.getsize(new_path))}")
            if os.path.splitext(item)[1] == '.txt':
                self.display_file_content(new_path)
            else:
                self.content_label.pack_forget()
                self.content_text.pack_forget()

    def display_file_content(self, path):
        self.content_label.pack(fill=tk.X)
        self.content_text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        self.content_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.content_text.config(state='normal')
        self.content_text.delete(1.0, tk.END)
        try:
            with open(path, 'r') as file_content:
                self.content_text.insert(tk.END, file_content.read())
        except:
            self.content_text.insert(tk.END, "Content: Not readable")
        self.content_text.config(state='disabled')

    def clear_info(self):
        self.name_label.config(text="")
        self.extra_label.config(text="")
        self.content_label.pack_forget()
        self.content_text.pack_forget()

if __name__ == "__main__":
    app = FileSystemViewer()
    app.mainloop()
