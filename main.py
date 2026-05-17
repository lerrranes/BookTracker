import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# Имя файла для хранения данных
DATA_FILE = "books_data.json"

# Список для хранения данных о книгах в памяти
books = []

# --- ФУНКЦИИ ЛОГИКИ ---

def save_data():
    """Функция сохранения данных в JSON"""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(books, f, ensure_ascii=False, indent=2)
        messagebox.showinfo("Успех", "Данные сохранены в файл!")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось сохранить данные: \n{e}")

def load_data():
    """Функция загрузки данных из JSON"""
    global books
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                books = json.load(f)
            update_table()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные: \n{e}")

def add_book():
    """Добавление новой книги"""
    title = entry_title.get().strip()
    author = entry_author.get().strip()
    genre = entry_genre.get().strip()
    pages = entry_pages.get().strip()

    # Проверка на пустые поля
    if not (title and author and genre and pages):
        messagebox.showwarning("Внимание", "Все поля должны быть заполнены!")
        return

    # Проверка, что количество страниц — это число
    try:
        pages_int = int(pages)
    except ValueError:
        messagebox.showwarning("Внимание", "Количество страниц должно быть целым числом!")
        return

    # Создаем словарь с данными и добавляем в список
    new_book = {
        "title": title,
        "author": author,
        "genre": genre,
        "pages": pages_int
    }
    books.append(new_book)
    
    save_data() # Сохраняем в JSON после добавления
    update_table() # Обновляем таблицу на экране
    clear_entries()

def update_table(display_list=None):
    """Обновление данных в таблице интерфейса"""
    # Очищаем текущую таблицу
    for item in tree.get_children():
        tree.delete(item)
    
    # Если список для отображения не передан, берем основной список книг
    list_to_show = display_list if display_list is not None else books
    
    for book in list_to_show:
        tree.insert("", tk.END, values=(book["title"], book["author"], book["genre"], book["pages"]))

def filter_by_genre():
    """Фильтрация по жанру"""
    query = entry_filter_genre.get().lower().strip()

    filtered = [b for b in books if query in b["genre"].lower()]
    update_table(filtered)

def filter_by_pages():
    """Фильтрация: книги > 200 страниц"""
    filtered = [b for b in books if b["pages"] > 200]
    update_table(filtered)

def reset_filter():
    """Сброс всех фильтров"""
    update_table(books)

def clear_entries():
    """Очистка полей ввода"""
    entry_title.delete(0, tk.END)
    entry_author.delete(0, tk.END)
    entry_genre.delete(0, tk.END)
    entry_pages.delete(0, tk.END)

# --- ИНТЕРФЕЙС (GUI) ---

root = tk.Tk()
root.title("Book Tracker")
root.geometry("650x550")

# Блок ввода данных
frame_input = tk.LabelFrame(root, text="Добавить новую книгу", padx=10, pady=10)
frame_input.pack(fill="x", padx=10, pady=5)

tk.Label(frame_input, text="Название:").grid(row=0, column=0, sticky="w")
entry_title = tk.Entry(frame_input)
entry_title.grid(row=0, column=1, fill="x", expand=True, padx=5)

tk.Label(frame_input, text="Автор:").grid(row=1, column=0, sticky="w")
entry_author = tk.Entry(frame_input)
entry_author.grid(row=1, column=1, fill="x", expand=True, padx=5)

tk.Label(frame_input, text="Жанр:").grid(row=2, column=0, sticky="w")
entry_genre = tk.Entry(frame_input)
entry_genre.grid(row=2, column=1, fill="x", expand=True, padx=5)

tk.Label(frame_input, text="Страниц:").grid(row=3, column=0, sticky="w")
entry_pages = tk.Entry(frame_input)
entry_pages.grid(row=3, column=1, fill="x", expand=True, padx=5)

btn_add = tk.Button(frame_input, text="Добавить книгу", command=add_book, bg="#e1f5fe")
btn_add.grid(row=4, column=0, columnspan=2, pady=10, sticky="we")

# Блок фильтрации
frame_filter = tk


ame(root, text="Фильтры", padx=10, pady=10)
frame_filter.pack(fill="x", padx=10, pady=5)

tk.Label(frame_filter, text="Жанр:").grid(row=0, column=0)
entry_filter_genre = tk.Entry(frame_filter)
entry_filter_genre.grid(row=0, column=1, padx=5)

btn_f_genre = tk.Button(frame_filter, text="Поиск по жанру", command=filter_by_genre)
btn_f_genre.grid(row=0, column=2, padx=5)

btn_f_pages = tk.Button(frame_filter, text="Больше 200 стр.", command=filter_by_pages)
btn_f_pages.grid(row=0, column=3, padx=5)

btn_reset = tk.Button(frame_filter, text="Сбросить", command=reset_filter)
btn_reset.grid(row=0, column=4, padx=5)

# Таблица вывода
columns = ("title", "author", "genre", "pages")
tree = ttk.Treeview(root, columns=columns, show="headings")
tree.heading("title", text="Название")
tree.heading("author", text="Автор")
tree.heading("genre", text="Жанр")
tree.heading("pages", text="Стр.")

tree.column("pages", width=70, anchor="center")
tree.pack(fill="both", expand=True, padx=10, pady=10)

# Загружаем данные из файла при запуске
load_data()

root.mainloop().LabelFrame
