import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import requests

# Константы
DATA_FILE = "history.json"
# Чтобы получить бесплатный ключ, нужно зайти на https://www.exchangerate-api.com/
API_KEY = "ВАШ_КЛЮЧ_API" 

class CurrencyConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Конвертер валют")
        self.root.geometry("500x550")
        
        self.history = []
        self.load_history()

        # --- Интерфейс ---
        # Поле ввода суммы
        tk.Label(root, text="Сумма:").pack(pady=5)
        self.entry_amount = tk.Entry(root)
        self.entry_amount.pack(pady=5)

        # Выбор валют
        self.currencies = ["USD", "EUR", "RUB", "GBP", "BYN", "KZT"]
        
        tk.Label(root, text="Из:").pack()
        self.combo_from = ttk.Combobox(root, values=self.currencies, state="readonly")
        self.combo_from.current(0)
        self.combo_from.pack()

        tk.Label(root, text="В:").pack()
        self.combo_to = ttk.Combobox(root, values=self.currencies, state="readonly")
        self.combo_to.current(2)
        self.combo_to.pack()

        # Кнопка конвертации
        self.btn_calc = tk.Button(root, text="Конвертировать", command=self.convert, bg="#d1ffd1")
        self.btn_calc.pack(pady=10)

        # Результат
        self.label_res = tk.Label(root, text="Результат: ", font=("Arial", 12, "bold"))
        self.label_res.pack(pady=10)

        # Таблица истории
        tk.Label(root, text="История конвертаций:").pack()
        self.tree = ttk.Treeview(root, columns=("date", "from", "to", "res"), show="headings", height=8)
        self.tree.heading("date", text="Дата")
        self.tree.heading("from", text="Из")
        self.tree.heading("to", text="В")
        self.tree.heading("res", text="Итог")
        self.tree.column("date", width=100)
        self.tree.pack(fill="x", padx=10)

        self.update_table()

    def convert(self):
        amount = self.entry_amount.get()
        base = self.combo_from.get()
        target = self.combo_to.get()

        if not amount:
            messagebox.showwarning("Ошибка", "Введите сумму")
            return

        try:
            # Запрос к внешнему API
            url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{base}/{target}/{amount}"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
result = round(data['conversion_result'], 2)
                
                res_text = f"{amount} {base} = {result} {target}"
                self.label_res.config(text=f"Результат: {res_text}")

                # Сохранение в историю
                from datetime import datetime
                record = {
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "from": f"{amount} {base}",
                    "to": target,
                    "res": str(result)
                }
                self.history.append(record)
                self.save_history()
                self.update_table()
            else:
                messagebox.showerror("Ошибка API", f"Статус код: {response.status_code}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Проверьте соединение: {e}")

    def save_history(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def load_history(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    self.history = json.load(f)
            except: self.history = []

    def update_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for r in self.history[::-1]: # Последние сверху
            self.tree.insert("", 0, values=(r["date"], r["from"], r["to"], r["res"]))

if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverter(root)
    root.mainloop() # Исправлено: просто mainloop без лишних вызовов
