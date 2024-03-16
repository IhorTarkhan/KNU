from tkinter import Listbox, Scrollbar

import os
import tkinter as tk


def list_directory(path):
    left_panel.delete(0, tk.END)
    left_panel.insert(tk.END, '..')
    path_label.config(text=path)
    global current_path
    current_path = path
    for item in os.listdir(path):
        left_panel.insert(tk.END, item)


def on_item_double_click(event):
    selection = left_panel.curselection()
    if selection:
        index = selection[0]
        item = left_panel.get(index)
        if item == '..':
            new_path = os.path.dirname(current_path)
        else:
            new_path = os.path.join(current_path, item)
        if os.path.isdir(new_path):
            list_directory(new_path)


def on_item_select(event):
    selection = left_panel.curselection()
    if selection:
        index = selection[0]
        item = left_panel.get(index)
        if item != '..':
            new_path = os.path.join(current_path, item)
            update_info(new_path, item)
        else:
            clear_info()


def update_info(new_path, item):
    name_label.config(text=f'Name: {item}')
    if os.path.isdir(new_path):
        extra_label.config(text=f'Top Folder: {os.path.basename(os.path.dirname(new_path))}')
        content_label.pack_forget()
        content_text.pack_forget()
    else:
        extra_label.config(text=f'Size: {os.path.getsize(new_path)} bytes')
        if os.path.splitext(item)[1] == '.txt':
            display_file_content(new_path)
        else:
            content_label.pack_forget()
            content_text.pack_forget()


def display_file_content(path):
    content_label.pack(fill=tk.X)
    content_text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
    content_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    content_text.config(state='normal')
    content_text.delete(1.0, tk.END)
    try:
        with open(path, 'r') as file_content:
            content_text.insert(tk.END, file_content.read())
    except:
        content_text.insert(tk.END, 'Content: Not readable')
    content_text.config(state='disabled')


def clear_info():
    name_label.config(text='')
    extra_label.config(text='')
    content_label.pack_forget()
    content_text.pack_forget()


root = tk.Tk()
root.geometry('1000x600')

path_label = tk.Label(root)
path_label.grid(row=0, column=0, columnspan=2, sticky='ew', padx=10, pady=5)

main_frame = tk.Frame(root)
main_frame.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=10, pady=5)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

left_panel = Listbox(main_frame)
left_panel.grid(row=0, column=0, sticky='nsew')
main_frame.grid_rowconfigure(0, weight=1)
main_frame.grid_columnconfigure(0, weight=1)
left_panel.bind('<Double-1>', on_item_double_click)
left_panel.bind('<<ListboxSelect>>', on_item_select)

right_panel = tk.Frame(main_frame)
right_panel.grid(row=0, column=1, sticky='nsew')
main_frame.grid_columnconfigure(1, weight=1)

name_label = tk.Label(right_panel, text='')
name_label.pack(fill=tk.X)

extra_label = tk.Label(right_panel, text='')
extra_label.pack(fill=tk.X)

content_label = tk.Label(right_panel, text='Content:')
content_text = tk.Text(right_panel, height=10, state='disabled')
content_scroll = Scrollbar(right_panel, command=content_text.yview)
content_text.configure(yscrollcommand=content_scroll.set)

current_path = os.path.dirname(os.path.abspath(__file__))
list_directory(current_path)

root.mainloop()
