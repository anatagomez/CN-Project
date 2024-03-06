import os
import tkinter as tk
from tkinter import messagebox, Entry

def block_websites():
    url = block_entry.get() # input url
    print(url)
    print("afadfasdf")
    command = f'sudo iptables -A OUTPUT -d {url} -j DROP'
    result = os.system(command)
    if result == 0:
        messagebox.showinfo("Success", f"{url} has been blocked.")
    else:
        messagebox.showerror("Error", "Failed to block the website.")

def unblock_websites():
    url = unblock_entry().get()  # input url
    command = f'sudo iptables -D OUTPUT -d {url} -j DROP'
    result = os.system(command)
    if result == 0:
        messagebox.showinfo("Success", f"{url} has been unblocked.")
    else:
        messagebox.showerror("Error", "Failed to block the unwebsite.")
      
window = tk.Tk()
window.title("Website Blocker")
window.geometry("429x200")

# block
block_frame = tk.Frame(window)
block_frame.pack(expand=True)

block_label = tk.Label(block_frame, text="Enter the URL of the website to block:")
block_label.grid(row=0, column=0, sticky="w")
block_entry = tk.Entry(block_frame)
block_entry.grid(row=1, column=0, sticky="ew")

block_button = tk.Button(block_frame, text="Block", command=block_websites)
block_button.grid(row=2, column=0, pady=5)

# unblock
unblock_frame = tk.Frame(window)
unblock_frame.pack(expand=True)

unblock_label = tk.Label(unblock_frame, text="Enter the URL of the website to unblock:")
unblock_label.grid(row=0, column=0, sticky="w")
unblock_entry = tk.Entry(unblock_frame)
unblock_entry.grid(row=1, column=0, sticky="ew")

unblock_button = tk.Button(unblock_frame, text="Unblock", command=unblock_websites)
unblock_button.grid(row=2, column=0, pady=5)

window.mainloop()