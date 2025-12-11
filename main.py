import os
import tkinter as tk
import shlex
import sys
import argparse

# Глобальные переменные для хранения параметров
VFS_PATH = None
SCRIPT_PATH = None


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


def execute_script(script_path):
    """Выполнение команд из стартового скрипта"""
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        text.insert(tk.END, f"\n=== Выполнение скрипта: {script_path} ===\n")

        for line_num, line in enumerate(lines, 1):
            command = line.strip()

            # Пропускаем пустые строки и комментарии
            if not command or command.startswith('#'):
                continue

            text.insert(tk.END, f"[скрипт:{line_num}] vfs> {command}\n")
            root.update()  # Обновляем интерфейс

            try:
                # Обрабатываем команду
                raw = expand(command)
                parts = shlex.split(raw)

                if not parts:
                    continue

                cmd, *args = parts

                if cmd == "exit":
                    text.insert(tk.END, "Команда exit в скрипте игнорируется\n")
                elif cmd == "ls":
                    text.insert(tk.END, f"ls вызван с аргументами: {args}\n")
                elif cmd == "cd":
                    text.insert(tk.END, f"cd вызван с аргументами: {args}\n")
                else:
                    text.insert(tk.END, f"Ошибка: неизвестная команда '{cmd}'\n")

            except ValueError as e:
                text.insert(tk.END, f"Ошибка разбора строки {line_num}: {e}\n")
                continue  # Пропускаем ошибочную строку

        text.insert(tk.END, f"=== Скрипт {script_path} выполнен ===\n\n")

    except FileNotFoundError:
        text.insert(tk.END, f"ОШИБКА: Скрипт не найден: {script_path}\n")
    except Exception as e:
        text.insert(tk.END, f"ОШИБКА выполнения скрипта: {e}\n")


def parse_arguments():
    """Парсинг аргументов командной строки"""
    parser = argparse.ArgumentParser(description='VFS Emulator')
    parser.add_argument('--vfs-path', help='Путь к физическому расположению VFS')
    parser.add_argument('--script', help='Путь к стартовому скрипту')

    # Парсим только известные аргументы, чтобы избежать конфликтов с tkinter
    args_list = sys.argv[1:]
    parsed_args = {}

    i = 0
    while i < len(args_list):
        if args_list[i] == '--vfs-path' and i + 1 < len(args_list):
            parsed_args['vfs_path'] = args_list[i + 1]
            i += 2
        elif args_list[i] == '--script' and i + 1 < len(args_list):
            parsed_args['script'] = args_list[i + 1]
            i += 2
        else:
            i += 1

    return parsed_args


def main():
    global VFS_PATH, SCRIPT_PATH

    # Парсим аргументы командной строки
    args = parse_arguments()

    VFS_PATH = args.get('vfs_path', os.getcwd())
    SCRIPT_PATH = args.get('script')

    # Создаем главное окно
    global root, text, entry
    root = tk.Tk()
    root.title("VFS")

    # Создаем текстовое поле с увеличенной высотой
    text = tk.Text(root, height=15, width=60)
    text.pack()

    # Отладочный вывод параметров при запуске
    text.insert(tk.END, "=== Параметры запуска VFS ===\n")
    text.insert(tk.END, f"VFS Path: {VFS_PATH}\n")
    if SCRIPT_PATH:
        text.insert(tk.END, f"Script: {SCRIPT_PATH}\n")
    else:
        text.insert(tk.END, "Script: не указан\n")
    text.insert(tk.END, "=" * 35 + "\n\n")

    # Поле ввода
    entry = tk.Entry(root, width=60)
    entry.pack()
    entry.bind('<Return>', lambda e: run_cmd())

    # Кнопка Run
    tk.Button(root, text="Run", command=run_cmd).pack()

    # Если указан скрипт, выполняем его после небольшой задержки
    if SCRIPT_PATH:
        root.after(500, lambda: execute_script(SCRIPT_PATH))

    root.mainloop()


if __name__ == "__main__":
    main()