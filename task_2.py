import requests
import tkinter as tk
from tkinter import ttk
import os


class AnimalGallery:
    def __init__(self, window):
        self.window = window
        window.title("Коты и собаки")
        window.geometry("500x450")
        window.resizable(False, False)

        tk.Label(window, text="КОТЫ И СОБАКИ", font=("Arial", 14, "bold")).pack(pady=10)

        self.cat_btn = tk.Button(window, text="Получить кота", command=self.get_cat,
                                 font=("Arial", 12), width=15)
        self.cat_btn.pack(pady=5)

        self.dog_btn = tk.Button(window, text="Получить собаку", command=self.get_dog,
                                 font=("Arial", 12), width=15)
        self.dog_btn.pack(pady=5)

        self.result = tk.Label(window, text="Нажмите кнопку", font=("Arial", 10))
        self.result.pack(pady=10)

        self.status = tk.Label(window, text="Готов", relief="sunken", anchor="w")
        self.status.pack(side="bottom", fill="x")

        if not os.path.exists("resource/images"):
            os.makedirs("resource/images")

    def get_cat(self):
        self.status.config(text="Ищем кота")
        self.window.update()

        try:
            r = requests.get("https://api.thecatapi.com/v1/images/search", timeout=10)
            if r.status_code == 200:
                url = r.json()[0]['url']
                self.save_photo(url, "cat.jpg", "Кот сохранён")
            else:
                self.result.config(text="Ошибка")
                self.status.config(text="Готов")
        except:
            self.result.config(text="Нет интернета")
            self.status.config(text="Готов")

    def get_dog(self):
        self.status.config(text="Ищем собаку")
        self.window.update()

        try:
            r = requests.get("https://dog.ceo/api/breeds/image/random", timeout=10)
            if r.status_code == 200:
                url = r.json()['message']
                self.save_photo(url, "dog.jpg", "Собака сохранена")
            else:
                self.result.config(text="Ошибка")
                self.status.config(text="Готов")
        except:
            self.result.config(text="Нет интернета")
            self.status.config(text="Готов")

    def save_photo(self, url, filename, msg):
        try:
            r = requests.get(url, timeout=10)
            file_path = f"resource/images/{filename}"
            with open(file_path, "wb") as f:
                f.write(r.content)

            self.result.config(text=msg)
            self.status.config(text="Готов")
        except:
            self.result.config(text="Ошибка")
            self.status.config(text="Готов")


if __name__ == "__main__":
    root = tk.Tk()
    app = AnimalGallery(root)
    root.mainloop()