import webbrowser
import speech_recognition as sr
import pyttsx3 
from openai import OpenAI
from threading import Thread
import os
import pygetwindow as gw
import customtkinter as ctk
import datetime
from PIL import Image

# Инициализация клиентов с вашими API-ключами
openai_client = OpenAI(api_key="sk-proj-U0XRhea1d90JKgbzfXtLT3BlbkFJVO6bR2zz92HPdvIOhO3G")
deepseek_client = OpenAI(api_key="sk-b36871fc12f0404b95c3dd72bce66269", base_url="https://api.deepseek.com")
ver = "Beta 4.0"

# Функция для распознавания голоса
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Скажите что-нибудь...")
        audio = recognizer.listen(source)

    try:
        print("Гав AI (Гуля) думает...")
        text = recognizer.recognize_google(audio, language="ru-RU")
        print(f"Вы сказали: {text}")
        return text
    except sr.UnknownValueError:
        print("Гав AI (Гуля) не смог разобрать ваш вопрос")
        return None
    except sr.RequestError as e:
        print(f"Гав AI (Гуля) не смог получить ответ от сервиса Google Speech Recognition; {e}")
        return None    

def ask_deepseek(question):
    response = deepseek_client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "Я голосовой помощник Гав с AI 'Гуля', созданный Gulya TV App (Гуля ТВ)"},
            {"role": "user", "content": question},
        ],
        stream=False
    )
    return response.choices[0].message.content

def ask_openai(question):
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Я голосовой помощник Гав с AI 'Гуля', созданный Gulya TV App (Гуля ТВ)"},
            {"role": "user", "content": question},
        ],
        stream=False
    )
    return response.choices[0].message.content

def setup_male_voice():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    # Выбор мужского голоса (этот выбор может отличаться в зависимости от вашей системы)
    for voice in voices:
        if "male" in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    
    # Настройка скорости речи (опционально)
    engine.setProperty('rate', 150)  # Скорость речи (слова в минуту)
    
    # Настройка громкости (опционально)
    engine.setProperty('volume', 1.0)  # Громкость от 0.0 до 1.0
    
    return engine

def speak_answer(answer):
    engine = setup_male_voice()
    engine.say(answer)
    engine.runAndWait()

# Функция для поиска в Google
def search_google(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)

def close_browser():
    os.system("taskkill /f /im chrome.exe")
    speak_answer("готово")

def minimize_windows():
    for window in gw.getAllTitles():
        if window not in ['Task Manager', 'woof.exe', 'woof.exe (2)']:  # Не свертывать менеджер задач
            gw.getWindowsWithTitle(window)[0].minimize()
    speak_answer("готово")

def maximize_windows():
    for window in gw.getAllTitles():
        if window not in ['Task Manager', 'woof.exe', 'woof.exe (2)']:  # Не свертывать менеджер задач
            gw.getWindowsWithTitle(window)[0].maximize()
    speak_answer("готово")

def open_youtube():
    youtube_url = f"https://www.youtube.com/"
    webbrowser.open(youtube_url)

def close_woof():
    os.system("taskkill /f /im woof.exe")
    root.destroy()
    speak_answer("Гав остановлен.")

def what():
    speak_answer("Что?")

def time():
    now = datetime.datetime.now()
    speak_answer(f"Сейчас {now.hour} {now.minute}")

def open_chrome():
    chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
    chrome_path2 = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
    if os.path.exists(chrome_path):
        webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
        webbrowser.get('chrome').open("https://www.google.com")
    elif os.path.exists(chrome_path2):
        webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path2))
        webbrowser.get('chrome').open("https://www.google.com")
    else:
        print("Google Chrome не найден на вашем компьютере.")


def play_music(query=None):
    if query:
        url = f"https://music.yandex.ru/search?text={query}"
    else:
        url = "https://music.yandex.ru/"  # Замените на вашу волну или плейлист
    webbrowser.open(url)        


# Функция для обработки команд и отправки запросов на сервер
def process_command(command):
    command_lower = command.lower()
    if command_lower == "стоп":
        print("Гав-ассистент остановлен.")
        root.destroy()
    elif command_lower in ["гав", "дог", "пёс"]:
        what()
    elif command_lower.startswith(("гуля ")):
        # Извлекаем запрос из команды
        question = command_lower.split(" ", 1)[1]
        if question:
            if current_ai == "DeepSeek":
                answer = ask_deepseek(question)
            else:
                answer = ask_openai(question)
            speak_answer(answer)
    elif command_lower.startswith(("загугли ", "найди ")):
        # Извлекаем запрос из команды
        query = command_lower.split(" ", 1)[1]
        if query:
            search_google(query)
    elif command_lower in ["закрой браузер", "Закрой браузер"]:
        close_browser()
    elif command_lower in ["сверни окна", "Сверни окна", "сверни все окна", "Сверни все окна"]:
        minimize_windows()
    elif command_lower in ["разверни окна", "Разверни окна", "разверни все окна", "Разверни все окна"]:
        maximize_windows()
    elif command_lower in ["Пока Гав", "пока Гав", "пока гав", "пока гуля", "Пока Гуля" "пока Гуля", "Пока гуля"]:
        close_woof()
        print("Гав-ассистент остановлен.")
        root.destroy()
    elif command_lower == "смени тему":
        toggle_theme()
    elif command_lower in ['время', 'текущее время', 'сейчас времени', 'который час']:
        time()
    elif command_lower == "смени ai":
        toggle_ai()
    elif command_lower == "открой браузер":
        open_chrome()
    elif command_lower == "включи музыку":
        play_music()
    elif command_lower.startswith(("включи песню ", "включи музыку ")):
        query = command_lower.split(" ", 2)[2]
        play_music(query)    

# Функция для переключения темы
def toggle_theme():
    current_mode = ctk.get_appearance_mode()
    if current_mode == "Dark":
        set_light_theme()
    else:
        set_dark_theme()
    speak_answer("готово")

# Функция для изменения темы
def set_dark_theme():
    ctk.set_appearance_mode("Dark")

def set_light_theme():
    ctk.set_appearance_mode("Light")

# Функция для отображения/скрытия панели настроек
def toggle_settings_panel():
    if settings_frame.winfo_ismapped():
        settings_frame.pack_forget()
    else:
        settings_frame.pack(pady=10, padx=20, fill="both", expand=True)

# Функция для переключения AI
def toggle_ai():
    global current_ai
    if current_ai == "DeepSeek":
        current_ai = "OpenAI"
        speak_answer("AI изменена на OpenAI")
    else:
        current_ai = "DeepSeek"
        speak_answer("AI изменена на DeepSeek")

# Создание графического интерфейса с использованием CustomTkinter
root = ctk.CTk()
root.title("Гав")
root.geometry("720x660")
root.iconbitmap("icon.png")  # Установка иконки приложения

# Установка темы
ctk.set_appearance_mode("dark")  # Варианты: "light", "dark", "system"
ctk.set_default_color_theme("green")  # Варианты: "blue", "green", "dark-blue"

# Создание header
header_frame = ctk.CTkFrame(master=root)
header_frame.pack(pady=10, padx=20, fill="x")

logo_image = ctk.CTkImage(light_image=Image.open("icon.png"), dark_image=Image.open("icon.png"), size=(50, 50))
logo_label = ctk.CTkLabel(master=header_frame, image=logo_image, text="")
logo_label.pack(side="left", padx=10)

version_label = ctk.CTkLabel(master=header_frame, text=f"Гав {ver}", font=("Roboto", 24))
version_label.pack(side="left", padx=10)

exit_button = ctk.CTkButton(master=header_frame, text="Выход", command=root.destroy)
exit_button.pack(side="right", padx=10)

settings_button = ctk.CTkButton(master=header_frame, text="Настройки ⚙️", command=toggle_settings_panel)
settings_button.pack(side="right", padx=10)

# Раздел настроек
settings_frame = ctk.CTkFrame(master=root)

settings_label = ctk.CTkLabel(master=settings_frame, text="Настройки", font=("Roboto", 18))
settings_label.pack(pady=10, padx=10)

dark_theme_button = ctk.CTkButton(master=settings_frame, text="Темная тема", command=set_dark_theme)
dark_theme_button.pack(pady=5, padx=10)

light_theme_button = ctk.CTkButton(master=settings_frame, text="Светлая тема", command=set_light_theme)
light_theme_button.pack(pady=5, padx=10)

ai_toggle_button = ctk.CTkButton(master=settings_frame, text="Сменить AI", command=toggle_ai)
ai_toggle_button.pack(pady=5, padx=10)

woof_image = ctk.CTkImage(light_image=Image.open("woofwhite.png"), dark_image=Image.open("woofblack.png"), size=(300, 300))
woof_image_label = ctk.CTkLabel(master=root, image=woof_image, text="")
woof_image_label.pack(pady=5, padx=10)

# Функция для потока, который будет обрабатывать команды
def command_thread():
    global current_ai
    current_ai = "DeepSeek"
    activated = False
    while True:
        command = recognize_speech()
        if command:
            if isinstance(command, str):
                command_lower = command.lower()
                if command_lower in ["гав", "дог", "пёс"]:
                    activated = True
                    what()
                elif activated:
                    process_command(command)
            else:
                print("Ошибка: команда не является строкой")

# Запуск потока для обработки команд
Thread(target=command_thread).start()

# Запуск графического интерфейса
root.mainloop()