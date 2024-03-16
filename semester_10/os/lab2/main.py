from tkinter import Listbox, Scrollbar

import os
import tkinter as tk


def format_size(size):
    for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            if unit == 'bytes':
                return f"{size} {unit}"

            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"


class FileSystemViewer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File System Navigator")
        self.geometry("1000x600")

        self.path_label = tk.Label(self, text="No folder selected", anchor="w")
        self.path_label.pack(fill=tk.X, padx=10, pady=5)

        self.up_button = tk.Button(self, text="Go Up", command=self.navigate_up)
        self.up_button.pack(fill=tk.X, padx=10, pady=5)

        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.listbox = Listbox(self.main_frame)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.listbox.bind('<Double-1>', self.on_item_double_click)
        self.listbox.bind('<<ListboxSelect>>', self.on_item_select)

        self.info_frame = tk.Frame(self.main_frame)
        self.info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.name_label = tk.Label(self.info_frame, text="Name:")
        self.name_label.pack(fill=tk.X)

        self.size_label = tk.Label(self.info_frame, text="Size:")
        self.size_label.pack(fill=tk.X)

        self.content_text = tk.Text(self.info_frame, height=10, state='disabled')
        self.content_text.pack(fill=tk.BOTH, expand=True)
        self.content_scroll = Scrollbar(self.info_frame, command=self.content_text.yview)
        self.content_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.content_text.configure(yscrollcommand=self.content_scroll.set)

        self.current_path = os.path.dirname(os.path.abspath(__file__))
        self.list_directory(self.current_path)

    def list_directory(self, path):
        self.listbox.delete(0, tk.END)
        self.path_label.config(text=path)
        self.current_path = path
        for item in os.listdir(path):
            self.listbox.insert(tk.END, item)

    def on_item_double_click(self, event):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            item = self.listbox.get(index)
            new_path = os.path.join(self.current_path, item)
            if os.path.isdir(new_path):
                self.list_directory(new_path)

    def on_item_select(self, event):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            item = self.listbox.get(index)
            new_path = os.path.join(self.current_path, item)

            self.name_label.config(text=f"Name: {item}")
            folders_inside = [f for f in os.listdir(new_path) if
                              os.path.isdir(os.path.join(new_path, f))] if os.path.isdir(new_path) else []
            self.size_label.config(text=f"Size: {format_size(os.path.getsize(new_path))}" if os.path.isfile(new_path) else f"Subfolders: {len(folders_inside)}")

            self.content_text.config(state='normal')
            self.content_text.delete(1.0, tk.END)
            if os.path.isdir(new_path):
                subfolders = '\n'.join([f' - {f}' for f in folders_inside])
                self.content_text.insert(tk.END, f"Subfolders:\n{subfolders}")
            else:
                try:
                    with open(new_path, 'r') as file_content:
                        self.content_text.insert(tk.END, file_content.read())
                except:
                    self.content_text.insert(tk.END, "Content not readable")
            self.content_text.config(state='disabled')

    def navigate_up(self):
        upper_path = os.path.dirname(self.current_path)
        if os.path.isdir(upper_path) and upper_path != self.current_path:
            self.list_directory(upper_path)


if __name__ == "__main__":
    app = FileSystemViewer()
    app.mainloop()
