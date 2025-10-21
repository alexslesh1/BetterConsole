import platform
import getpass  
from colorama import Fore, Back, Style, init
import psutil
import uuid
import subprocess
import json

import json
import os
from pathlib import Path

def load_config():
    home_dir = Path.home()
    data_dir = home_dir / ".better_console" / "data"
    config_file = data_dir / "config.json"
    
    
    default_config = {
        "colors": {
            "title": ["RED", "YELLOW", "BLUE", "RED", "YELLOW"],
            "text": "BLUE",
            "cpu_low": "GREEN",
            "cpu_high": "RED"
        },
        "image": [
            "⢀⣤⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⣤⡀",
            "⢺⣿⡟⠻⣿⣷⣤⣀⣤⣤⣦⣶⣶⣶⣤⣤⣄⣠⣶⣿⠿⠛⣿⣷  ",
            "⠸⣿⡇⠀⣠⣿⣿⡿⠿⠛⠛⢛⠛⠟⠛⠻⠿⣿⣿⣧⡀⢀⣿⡇  ",
            "⠀⣿⣧⣾⡿⠛⠁⠀⣀⡀⠀⠁⠈⠀⢀⠀⠀⠀⠙⢿⣿⣾⣿⠁  ",
            "⠀⢸⣿⡟⠑⢿⣦⣴⡿⠃⠀⠀⠀⠀⠻⣷⣤⣾⠏⠀⠻⣿⣿   ",
            "⠀⣿⣿⠁⠀⢀⣿⡿⢷⣦⠀⠀⠀⠀⢠⣾⠿⣷⣄⠀⠀⣹⣿⡇  ",
            "⠀⣿⣿⠀⠀⠼⠟⠁⠈⠋⠠⣤⣤⡤⠘⠋⠀⠙⠛⠀⠀⢹⣿⡇  ",
            "⠀⣿⣿⡄⠀⠀⠀⠀⣦⣀⢀⣸⣿⡁⢀⣠⡄⠀⡁⠔⡀⣾⣿⠇  ",
            "⠀⠘⣿⣷⣅⠀⠀⠀⠘⣿⠟⠋⠉⠛⢿⡟⠀⠠⠴⣅⣾⣿⠟   ",
            "⠀⠀⠈⢿⣿⣦⣄⢀⠀⣸⠀⠀⠀⠀⠀⠠⣰⣶⣶⣿⣿⠋    ",
            "⠀⠀⠀⠀⠈⠛⢿⣿⣷⣶⣶⣶⣦⣶⣶⣾⣿⣿⠿⠋      ",
            "⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠛⠛⠛⠋⠉⠁⠀"
        ]
    }
    
    try:
        if not config_file.exists():
            data_dir.mkdir(parents=True, exist_ok=True)
            
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, ensure_ascii=False, indent=2)
            
            return default_config
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
            
    except Exception as e:
        print(f"Ошибка при работе с конфигурацией: {e}")
        print("Используются настройки по умолчанию")
        return default_config

config = load_config()

def get_color(color_name):
    color_map = {
        "RED": Fore.RED,
        "YELLOW": Fore.YELLOW,
        "BLUE": Fore.BLUE,
        "GREEN": Fore.GREEN,
        "MAGENTA": Fore.MAGENTA,
        "CYAN": Fore.CYAN,
        "WHITE": Fore.WHITE,
        "BLACK": Fore.BLACK
    }
    return color_map.get(color_name, Fore.WHITE)

text_color = get_color(config["colors"]["text"])
cpu_low_color = get_color(config["colors"]["cpu_low"])
cpu_high_color = get_color(config["colors"]["cpu_high"])

re = Style.RESET_ALL

def battery_print():
    try:
        battery = psutil.sensors_battery()
        if battery is not None:
            battery_percent = battery.percent
            return f'{battery_percent}%'
        else:
            return 'Не доступно'
    except:
        return 'Ошибка'

def get_processor_name():
    try:
        result = subprocess.run(['sysctl', '-n', 'machdep.cpu.brand_string'], 
                              capture_output=True, text=True, check=True)
        processor_name = result.stdout.strip()
        
        if not processor_name or processor_name == "Apple processor":
            result = subprocess.run(['sysctl', '-n', 'hw.model'], 
                                  capture_output=True, text=True, check=True)
            processor_name = result.stdout.strip()
        
        cpu_percent = psutil.cpu_percent(interval=1)
        return {
            'Название': processor_name,
            'Загрузка': cpu_percent,
            'Загрузка_строка': f'{cpu_percent}%'
        }
    except:
        processor_name = platform.processor()
        cpu_percent = psutil.cpu_percent(interval=1)
        return {
            'Название': processor_name,
            'Загрузка': cpu_percent,
            'Загрузка_строка': f'{cpu_percent}%'
        }

def get_memory_usage():
    memory = psutil.virtual_memory()
    return {
        'Всего': f'{memory.total / (1024**3):.2f} ГБ',
        'Используется': f'{memory.used / (1024**3):.2f} ГБ',
        'Свободно': f'{memory.available / (1024**3):.2f} ГБ',
        'Процент использования': f'{memory.percent}%'
    }

def platform_info():
    try:
        system_info = {
            'Система': platform.system(),
            'Платформа': platform.platform(),
            'Пользователь': getpass.getuser()  
        }
        return system_info
    except Exception as e:
        return f"Ошибка: {e}"

def output_info():
    version_info = platform_info()
    memory_info = get_memory_usage()
    cpu_info = get_processor_name()
    battery_info = battery_print()

    image_lines = config["image"]

    colors = [Back.BLUE, Back.CYAN, Back.WHITE, Back.BLACK, 
              Back.MAGENTA, Back.YELLOW, Back.GREEN, Back.RED]
    
    color_squares = ""
    for color in colors:
        color_squares += f"{color}  {Style.RESET_ALL}"

    if isinstance(version_info, str) and 'ошибка' in version_info.lower():
        text_lines = ['error']
    else:
        color = cpu_low_color if cpu_info["Загрузка"] < 50 else cpu_high_color
        
        title_text = "Better Console"
        colored_title = ""
        title_colors = config["colors"]["title"]
        for i, char in enumerate(title_text):
            if char != " ":  
                color_name = title_colors[i % len(title_colors)]
                colored_title += f"{get_color(color_name)}{char}"
            else:
                colored_title += " "
        
        text_lines = [
            f'{colored_title}{re}',
            f'{text_color}--------------{re}',
            f'{text_color}Пользователь: {re}{version_info["Пользователь"]}',
            f'{text_color}Платформа: {re}{version_info["Платформа"]}',
            f'{text_color}Процессор: {re}{cpu_info["Название"]}',
            f'{text_color}Загрузка CPU: {re}{color}{cpu_info["Загрузка_строка"]}{re}',
            f'{text_color}Память: {re}{memory_info["Используется"]}{text_color} / {re}{memory_info["Всего"]}',
            f'{text_color}Заряд Батареи: {re}{battery_info}',
            f'',
            color_squares,
        ]
    
    max_lines = max(len(image_lines), len(text_lines))
    
    for i in range(max_lines):
        image_part = image_lines[i] if i < len(image_lines) else ""
        text_part = text_lines[i] if i < len(text_lines) else ""
        
        print(f"{image_part}    {text_part}")

if __name__ == '__main__':
    output_info()