import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import os

API_KEY = "e2b7caaa82151a83ff54031572b5cadc"
URL = "https://api.openweathermap.org/data/2.5/weather"
URL_ICON = "https://openweathermap.org/img/wn/"


def get_weather(city):
    try:
        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric",
            "lang": "ru"
        }
        r = requests.get(URL, params=params, timeout=10)

        if r.status_code == 200:
            return r.json()
        else:
            return None
    except:
        return None


def load_icon(icon_code):
    try:
        url = f"{URL_ICON}{icon_code}.png"
        r = requests.get(url, timeout=5)
        with open("temp_icon.png", "wb") as f:
            f.write(r.content)
        img = Image.open("temp_icon.png")
        img.thumbnail((100, 100))
        photo = ImageTk.PhotoImage(img)
        os.remove("temp_icon.png")
        return photo
    except:
        return None


def show_weather():
    city = entry.get().strip()

    if not city:
        messagebox.showwarning("Ошибка", "Введите город")
        return

    status.config(text="Загрузка")
    root.update()

    data = get_weather(city)

    if not data:
        messagebox.showerror("Ошибка", f"Город '{city}' не найден")
        status.config(text="Готов")
        return

    temp = data['main']['temp']
    icon_code = data['weather'][0]['icon']

    city_label.config(text=city.upper())
    temp_label.config(text=f"{temp:.1f}°C")

    icon = load_icon(icon_code)
    if icon:
        icon_label.config(image=icon)
        icon_label.image = icon

    status.config(text="Готов")


root = tk.Tk()
root.title("Погода")
root.geometry("450x450")
root.resizable(False, False)

tk.Label(root, text="ПОГОДА", font=("Arial", 16, "bold")).pack(pady=10)

f = tk.Frame(root)
f.pack(pady=5)

entry = tk.Entry(f, width=20, font=("Arial", 12))
entry.pack(side="left", padx=5)

tk.Button(f, text="Узнать", command=show_weather, width=8).pack(side="left")

city_label = tk.Label(root, text="", font=("Arial", 14, "bold"))
city_label.pack(pady=10)

icon_label = tk.Label(root)
icon_label.pack()

temp_label = tk.Label(root, text="", font=("Arial", 32, "bold"))
temp_label.pack(pady=10)

status = tk.Label(root, text="Введите город", relief="sunken", anchor="w")
status.pack(side="bottom", fill="x")

root.mainloop()