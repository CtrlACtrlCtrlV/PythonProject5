import os
import tkinter as tk
import shlex


def expand(s: str):
    for k in os.environ:
        s = s.replace("$" + k, os.environ[k])
    return s


def run_cmd():
    raw = expand(entry.get())
    text.insert(tk.END, f"vfs> {raw}\n")

    try:
        parts = shlex.split(raw)
    except ValueError as e:
        text.insert(tk.END, f"Ошибка разбора: {e}\n")
        entry.delete(0, tk.END)
        return

    if not parts:
        entry.delete(0, tk.END)
        return

    cmd, *args = parts

    if cmd == "exit":
        root.destroy()
    elif cmd == "ls":
        text.insert(tk.END, f"ls вызван с аргументами: {args}\n")
    elif cmd == "cd":
        text.insert(tk.END, f"cd вызван с аргументами: {args}\n")
    else:
        text.insert(tk.END, f"Ошибка: неизвестная команда '{cmd}'\n")

    entry.delete(0, tk.END)


root = tk.Tk()
root.title("VFS")
text = tk.Text(root, height=10, width=50)
text.pack()
entry = tk.Entry(root, width=50)
entry.pack()
entry.bind('<Return>', lambda e: run_cmd())
tk.Button(root, text="Run", command=run_cmd).pack()
root.mainloop()