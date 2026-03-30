import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import os

URL_DOG = "https://dog.ceo/api/breeds/image/random"
URL_CAT = "https://api.thecatapi.com/v1/images/search"


def get_cat():
    try:
        r = requests.get(URL_CAT, timeout=10)
        if r.status_code == 200:
            data = r.json()
            return data[0]['url']
        return None
    except:
        return None


def get_dog():
    try:
        r = requests.get(URL_DOG, timeout=10)
        if r.status_code == 200:
            data = r.json()
            return data['message']
        return None
    except:
        return None


def load_image(url):
    try:
        r = requests.get(url, timeout=10)
        with open("temp_img.jpg", "wb") as f:
            f.write(r.content)
        img = Image.open("temp_img.jpg")
        img.thumbnail((400, 400))
        photo = ImageTk.PhotoImage(img)
        os.remove("temp_img.jpg")
        return photo
    except:
        return None


def show_cat():
    status.config(text="Ищем кота")
    root.update()

    url = get_cat()
    if not url:
        messagebox.showerror("Ошибка", "Не удалось загрузить кота")
        status.config(text="Готов")
        return

    img = load_image(url)
    if img:
        animal_label.config(text="КОТ")
        image_label.config(image=img)
        image_label.image = img
        status.config(text="Готов")
    else:
        messagebox.showerror("Ошибка", "Не удалось загрузить картинку")
        status.config(text="Готов")


def show_dog():
    status.config(text="Ищем собаку")
    root.update()

    url = get_dog()
    if not url:
        messagebox.showerror("Ошибка", "Не удалось загрузить собаку")
        status.config(text="Готов")
        return

    img = load_image(url)
    if img:
        animal_label.config(text="СОБАКА")
        image_label.config(image=img)
        image_label.image = img
        status.config(text="Готов")
    else:
        messagebox.showerror("Ошибка", "Не удалось загрузить картинку")
        status.config(text="Готов")


root = tk.Tk()
root.title("Коты и собаки")
root.geometry("500x550")
root.resizable(False, False)

tk.Label(root, text="КОТЫ И СОБАКИ", font=("Arial", 16, "bold")).pack(pady=10)

f = tk.Frame(root)
f.pack(pady=10)

tk.Button(f, text="Получить кота", command=show_cat,
          font=("Arial", 12), width=15, bg="#ffcc99").pack(side="left", padx=10)

tk.Button(f, text="Получить собаку", command=show_dog,
          font=("Arial", 12), width=15, bg="#99ccff").pack(side="left", padx=10)

animal_label = tk.Label(root, text="", font=("Arial", 12, "bold"))
animal_label.pack()

image_label = tk.Label(root, text="Нажмите кнопку", font=("Arial", 10))
image_label.pack(pady=10)

status = tk.Label(root, text="Готов", relief="sunken", anchor="w")
status.pack(side="bottom", fill="x")

root.mainloop()