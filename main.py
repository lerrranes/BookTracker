import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# Файл для хранения данных
DATA_FILE = "movies.json"

class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library — Личная кинотека")
        self.root.geometry("750x600")
        
        self.movies = []
        self.load_data()

        # --- Форма ввода ---
        frame_form = tk.LabelFrame(root, text="Добавить новый фильм", padx=10, pady=10)
        frame_form.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_form, text="Название:").grid(row=0, column=0, sticky="w")
        self.ent_title = tk.Entry(frame_form)
        self.ent_title.grid(row=0, column=1, sticky="we", padx=5, pady=2)

        tk.Label(frame_form, text="Жанр:").grid(row=1, column=0, sticky="w")
        self.ent_genre = tk.Entry(frame_form)
        self.ent_genre.grid(row=1, column=1, sticky="we", padx=5, pady=2)

        tk.Label(frame_form, text="Год выпуска:").grid(row=2, column=0, sticky="w")
        self.ent_year = tk.Entry(frame_form)
        self.ent_year.grid(row=2, column=1, sticky="we", padx=5, pady=2)

        tk.Label(frame_form, text="Рейтинг (0-10):").grid(row=3, column=0, sticky="w")
        self.ent_rating = tk.Entry(frame_form)
        self.ent_rating.grid(row=3, column=1, sticky="we", padx=5, pady=2)

        frame_form.grid_columnconfigure(1, weight=1)

        self.btn_add = tk.Button(frame_form, text="Добавить фильм", command=self.add_movie, bg="#d1f0ff")
        self.btn_add.grid(row=4, column=0, columnspan=2, pady=10, sticky="we")

        # --- Блок фильтрации ---
        frame_filter = tk.LabelFrame(root, text="Фильтрация", padx=10, pady=10)
        frame_filter.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_filter, text="Поиск:").grid(row=0, column=0)
        self.ent_filter = tk.Entry(frame_filter, width=20)
        self.ent_filter.grid(row=0, column=1, padx=5)

        tk.Button(frame_filter, text="Фильтр по жанру", command=self.filter_genre).grid(row=0, column=2, padx=5)
        tk.Button(frame_filter, text="Фильтр по году", command=self.filter_year).grid(row=0, column=3, padx=5)
        tk.Button(frame_filter, text="Сбросить", command=self.refresh_table).grid(row=0, column=4, padx=5)

        # --- Таблица ---
        self.tree = ttk.Treeview(root, columns=("title", "genre", "year", "rating"), show="headings")
        self.tree.heading("title", text="Название")


self.tree.heading("genre", text="Жанр")
        self.tree.heading("year", text="Год")
        self.tree.heading("rating", text="Рейтинг")
        
        for col in ("year", "rating"):
            self.tree.column(col, width=80, anchor="center")
        
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.refresh_table()

    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.movies, f, ensure_ascii=False, indent=4)

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    self.movies = json.load(f)
            except: self.movies = []

    def add_movie(self):
        t = self.ent_title.get().strip()
        g = self.ent_genre.get().strip()
        y = self.ent_year.get().strip()
        r = self.ent_rating.get().strip()
        
        # Валидация: пустые поля
        if not (t and g and y and r):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return
        
        # Валидация: год и рейтинг
        try:
            y_int = int(y)
            r_float = float(r)
            if not (0 <= r_float <= 10):
                raise ValueError("Рейтинг должен быть от 0 до 10")
        except ValueError:
            messagebox.showerror("Ошибка", "Год — целое число, Рейтинг — число от 0 до 10!")
            return

        self.movies.append({"title": t, "genre": g, "year": y_int, "rating": r_float})
        self.save_data()
        self.refresh_table()
        for e in (self.ent_title, self.ent_genre, self.ent_year, self.ent_rating):
            e.delete(0, tk.END)

    def refresh_table(self, data=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        display_data = data if data is not None else self.movies
        for m in display_data:
            self.tree.insert("", tk.END, values=(m["title"], m["genre"], m["year"], m["rating"]))

    def filter_genre(self):
        query = self.ent_filter.get().lower()
        filtered = [m for m in self.movies if query in m["genre"].lower()]
        self.refresh_table(filtered)

    def filter_year(self):
        query = self.ent_filter.get()
        filtered = [m for m in self.movies if str(m["year"]) == query]
        self.refresh_table(filtered)

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibrary(root)
    root.mainloop()
