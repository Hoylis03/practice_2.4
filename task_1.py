import tkinter as tk
from tkinter import ttk, messagebox
import requests
import os

API_KEY = 'e2b7caaa82151a83ff54031572b5cadc'
URL = 'https://api.openweathermap.org/data/2.5/weather'

VALID_ICONS = {
    '01d', '02d', '03d', '04d', '09d', '10d', '11d', '13d', '50d',
    '01n', '02n', '03n', '04n', '09n', '10n', '11n', '13n', '50n'
}


def get_weather():
    city = entry_city.get().strip()
    if not city:
        temp_label.config(text='Введите город')
        icon_label.config(image="")
        return

    try:
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric',
            'lang': 'ru'
        }
        r = requests.get(URL, params=params, timeout=10)

        if r.status_code == 200:
            data = r.json()
            temp = data['main']['temp']
            icon_code = data['weather'][0]['icon']

            temp_label.config(text=f'{temp:.1f}°C')

            if icon_code in VALID_ICONS:
                icon_path = f"resource/icons/{icon_code}.png"
                if os.path.exists(icon_path):
                    icon_img = tk.PhotoImage(file=icon_path)
                    icon_label.config(image=icon_img)
                    icon_label.image = icon_img
                else:
                    icon_label.config(image="")
            else:
                icon_label.config(image="")
        elif r.status_code == 404:
            messagebox.showerror("Ошибка", f"Город '{city}' не найден")
            temp_label.config(text="")
            icon_label.config(image="")
        else:
            messagebox.showerror("Ошибка", "Ошибка загрузки данных")
            temp_label.config(text="")
            icon_label.config(image="")

    except:
        messagebox.showerror("Ошибка", "Нет интернета")
        temp_label.config(text="")
        icon_label.config(image="")


if not os.path.exists("resource/icons"):
    os.makedirs("resource/icons")

root = tk.Tk()
root.title("Погода")
root.geometry("500x450")
root.resizable(False, False)

tk.Label(root, text="ПОГОДА", font=("Arial", 16, "bold")).pack(pady=10)

f = tk.Frame(root)
f.pack(pady=5)

entry_city = ttk.Entry(f, width=20, font=("Arial", 12))
entry_city.pack(side="left", padx=5)

tk.Button(f, text="Узнать", command=get_weather, width=8).pack(side="left")

temp_label = tk.Label(root, text="", font=("Arial", 28, "bold"))
temp_label.pack(pady=20)

icon_label = tk.Label(root, text="", font=("Arial", 20))
icon_label.pack(pady=10)

status = tk.Label(root, text="Введите город", relief="sunken", anchor="w")
status.pack(side="bottom", fill="x")

root.mainloop()