import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class BookTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker - Трекер прочитанных книг")
        self.root.geometry("900x600")
        
        # Список для хранения книг
        self.books = []
        self.filename = "books.json"
        
        # Загрузка данных при запуске
        self.load_books()
        
        # Создание интерфейса
        self.create_widgets()
        
        # Обновление таблицы
        self.refresh_table()
    
    def create_widgets(self):
        # Рамка для ввода данных
        input_frame = tk.LabelFrame(self.root, text="Добавление новой книги", padx=10, pady=10)
        input_frame.pack(pady=10, padx=10, fill="x")
        
        # Поля ввода
        tk.Label(input_frame, text="Название книги:").grid(row=0, column=0, sticky="e", pady=5)
        self.title_entry = tk.Entry(input_frame, width=30)
        self.title_entry.grid(row=0, column=1, pady=5, padx=5)
        
        tk.Label(input_frame, text="Автор:").grid(row=1, column=0, sticky="e", pady=5)
        self.author_entry = tk.Entry(input_frame, width=30)
        self.author_entry.grid(row=1, column=1, pady=5, padx=5)
        
        tk.Label(input_frame, text="Жанр:").grid(row=2, column=0, sticky="e", pady=5)
        self.genre_entry = tk.Entry(input_frame, width=30)
        self.genre_entry.grid(row=2, column=1, pady=5, padx=5)
        
        tk.Label(input_frame, text="Количество страниц:").grid(row=3, column=0, sticky="e", pady=5)
        self.pages_entry = tk.Entry(input_frame, width=30)
        self.pages_entry.grid(row=3, column=1, pady=5, padx=5)
        
        # Кнопка добавления
        self.add_button = tk.Button(input_frame, text="Добавить книгу", command=self.add_book, 
                                   bg="green", fg="white", font=("Arial", 10, "bold"))
        self.add_button.grid(row=4, column=0, columnspan=2, pady=10)
        
        # Рамка для фильтрации
        filter_frame = tk.LabelFrame(self.root, text="Фильтрация", padx=10, pady=10)
        filter_frame.pack(pady=10, padx=10, fill="x")
        
        # Фильтр по жанру
        tk.Label(filter_frame, text="Фильтр по жанру:").grid(row=0, column=0, sticky="e", pady=5)
        self.genre_filter = tk.Entry(filter_frame, width=20)
        self.genre_filter.grid(row=0, column=1, pady=5, padx=5)
        
        # Фильтр по страницам
        tk.Label(filter_frame, text="Страниц больше:").grid(row=1, column=0, sticky="e", pady=5)
        self.pages_filter = tk.Entry(filter_frame, width=10)
        self.pages_filter.grid(row=1, column=1, sticky="w", pady=5, padx=5)
        
        # Кнопка фильтрации
        self.filter_button = tk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter,
                                      bg="blue", fg="white")
        self.filter_button.grid(row=2, column=0, columnspan=2, pady=5)
        
        # Кнопка сброса фильтра
        self.reset_button = tk.Button(filter_frame, text="Сбросить фильтр", command=self.reset_filter,
                                     bg="orange", fg="white")
        self.reset_button.grid(row=3, column=0, columnspan=2, pady=5)
        
        # Рамка для таблицы
        table_frame = tk.Frame(self.root)
        table_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Создание таблицы
        columns = ("Название", "Автор", "Жанр", "Страницы")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        # Настройка столбцов
        self.tree.heading("Название", text="Название книги")
        self.tree.heading("Автор", text="Автор")
        self.tree.heading("Жанр", text="Жанр")
        self.tree.heading("Страницы", text="Количество страниц")
        
        self.tree.column("Название", width=250)
        self.tree.column("Автор", width=150)
        self.tree.column("Жанр", width=120)
        self.tree.column("Страницы", width=100)
        
        # Скроллбар
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Кнопка удаления
        self.delete_button = tk.Button(self.root, text="Удалить выбранную книгу", command=self.delete_book,
                                      bg="red", fg="white", font=("Arial", 10, "bold"))
        self.delete_button.pack(pady=5)
        
        # Информационная панель
        self.info_label = tk.Label(self.root, text=f"Всего книг: {len(self.books)}", font=("Arial", 10))
        self.info_label.pack(pady=5)
    
    def add_book(self):
        """Добавление новой книги"""
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_entry.get().strip()
        pages = self.pages_entry.get().strip()
        
        # Проверка на пустые поля
        if not title or not author or not genre or not pages:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return
        
        # Проверка количества страниц (должно быть числом)
        try:
            pages = int(pages)
            if pages <= 0:
                messagebox.showerror("Ошибка", "Количество страниц должно быть положительным числом!")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Количество страниц должно быть числом!")
            return
        
        # Добавление книги
        book = {
            "title": title,
            "author": author,
            "genre": genre,
            "pages": pages
        }
        
        self.books.append(book)
        self.save_books()
        self.refresh_table()
        
        # Очистка полей
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.pages_entry.delete(0, tk.END)
        
        # Обновление информационной панели
        self.info_label.config(text=f"Всего книг: {len(self.books)}")
        
        messagebox.showinfo("Успех", "Книга успешно добавлена!")
    
    def delete_book(self):
        """Удаление выбранной книги"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Ошибка", "Выберите книгу для удаления!")
            return
        
        # Получение индекса выбранной книги
        for item in selected:
            values = self.tree.item(item, "values")
            # Поиск книги в списке
            for i, book in enumerate(self.books):
                if (book["title"] == values[0] and book["author"] == values[1] and 
                    book["genre"] == values[2] and book["pages"] == int(values[3])):
                    del self.books[i]
                    break
        
        self.save_books()
        self.refresh_table()
        self.info_label.config(text=f"Всего книг: {len(self.books)}")
        messagebox.showinfo("Успех", "Книга удалена!")
    
    def apply_filter(self):
        """Применение фильтрации"""
        genre_filter = self.genre_filter.get().strip().lower()
        pages_filter = self.pages_filter.get().strip()
        
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Фильтрация книг
        filtered_books = self.books.copy()
        
        # Фильтр по жанру
        if genre_filter:
            filtered_books = [book for book in filtered_books if genre_filter in book["genre"].lower()]
        
        # Фильтр по страницам
        if pages_filter:
            try:
                pages_min = int(pages_filter)
                filtered_books = [book for book in filtered_books if book["pages"] > pages_min]
            except ValueError:
                messagebox.showerror("Ошибка", "Количество страниц должно быть числом!")
                return
        
        # Отображение отфильтрованных книг
        for book in filtered_books:
            self.tree.insert("", tk.END, values=(book["title"], book["author"], book["genre"], book["pages"]))
    
    def reset_filter(self):
        """Сброс фильтрации"""
        self.genre_filter.delete(0, tk.END)
        self.pages_filter.delete(0, tk.END)
        self.refresh_table()
    
    def refresh_table(self):
        """Обновление таблицы"""
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Отображение всех книг
        for book in self.books:
            self.tree.insert("", tk.END, values=(book["title"], book["author"], book["genre"], book["pages"]))
    
    def save_books(self):
        """Сохранение книг в JSON файл"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as file:
                json.dump(self.books, file, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {str(e)}")
    
    def load_books(self):
        """Загрузка книг из JSON файла"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as file:
                    self.books = json.load(file)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {str(e)}")
                self.books = []
        else:
            # Создание файла с примером данных
            self.books = [
                {"title": "Война и мир", "author": "Лев Толстой", "genre": "Роман", "pages": 1300},
                {"title": "Преступление и наказание", "author": "Фёдор Достоевский", "genre": "Роман", "pages": 670},
                {"title": "Мастер и Маргарита", "author": "Михаил Булгаков", "genre": "Роман", "pages": 480},
                {"title": "1984", "author": "Джордж Оруэлл", "genre": "Антиутопия", "pages": 320}
            ]
            self.save_books()

def main():
    root = tk.Tk()
    app = BookTracker(root)
    root.mainloop()

if __name__ == "__main__":
    main()
