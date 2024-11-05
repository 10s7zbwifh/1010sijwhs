import whois
import requests
import asyncio
import pystyle
from pystyle import *
from termcolor import colored
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
token = "1723179534:hqst0L4e"
def clear():
    os.system("clear")

def banner():
    ascii_banner = """ ██▀███  
▓██ ▒ ██▒
▓██ ░▄█ ▒
▒██▀▀█▄  
░██▓ ▒██▒
░ ▒▓ ░▒▓░
  ░▒ ░ ▒░
  ░░   ░ 
   ░"""
    Write.Print(Center.XCenter(ascii_banner), Colors.green_to_white, interval=0.0000006)

def information_ip(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}?fields=status,message,country,regionName,city,org,lat,lon,query")
        data = response.json()
        
        lat = data.get("lat")
        lon = data.get("lon")
        map_link = f"https://www.google.com/maps?q={lat},{lon}"
        
        information = f"""IP-адрес: {ip}
Организация: {data.get("org")}
Страна: {data.get("country")}
Регион: {data.get("regionName")}
Город: {data.get("city")}
Координаты: {map_link}
        """
        Write.Print(information, Colors.green_to_white, interval=0.0000006)
        Write.Print("\nНажмите Enter чтобы вернуться к меню", Colors.green_to_white, interval=0.0000006)
        enter = input()
        main()
        
    except Exception as e:
        Write.Print(f"Ошибка: {e}", Colors.green_to_white, interval=0.0000006)

def search(request):
    if not token:
        Write.Print("Ошибка: Токен не задан", Colors.red_to_white, interval=0.0000006)
        return

    data = {
        "token": token,
        "request": request,
        "limit": 100,
        "lang": "ru"
    }

    url = "https://leakosintapi.com/"
    
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()

        if response.status_code == 501:
            raise ValueError("Ошибка 501: Неправильный формат запроса. Данные должны быть отправлены в формате JSON.")

        result = response.json()
        response_message = ""

        if 'List' in result:
            for db_name, db_info in result['List'].items():
                response_message += "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
                response_message += f"База: {db_name}\n"

                for entry in db_info['Data']:
                    if isinstance(entry, dict):
                        response_message += "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
                        response_message += f"Полное имя: {entry.get('FullName', 'Не указано')}\n"

                        if "VK" in db_name:
                            gender = entry.get('Gender')
                            response_message += f"Пол: {'Мужской' if gender == '1' else 'Женский' if gender == '2' else 'Не указано'}\n"
                            response_message += f"VK ID: {entry.get('VkID', 'Не указано')}\n"

                        response_message += f"Город: {entry.get('City', 'Не указано')}\n"
                        response_message += f"Страна: {entry.get('Country', 'Не указано')}\n"
                        response_message += f"Дата рождения: {entry.get('BDay', 'Не указано')}\n"
                        response_message += f"Адрес: {entry.get('Address', 'Не указано')}\n"
                        response_message += f"Количество подписчиков: {entry.get('Followers', 'Не указано')}\n"
                        response_message += f"Школа: {entry.get('School', 'Не указано')}\n"
                        response_message += f"Класс: {entry.get('Class', 'Не указано')}\n"
                        response_message += f"Ссылка на аватар: {entry.get('Avatar', 'Не указано')}\n"
                        response_message += f"URL: {entry.get('Url', 'Не указано')}\n"
                        response_message += "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"

        if not response_message:
            response_message = f"По вашему запросу не найдено результатов.\n\nЗапрос: {request}"
        
        Write.Print(response_message, Colors.green_to_white, interval=0.0000006)
        Write.Print("\n\n\nНажмите Enter чтобы вернуться к меню", Colors.green_to_white, interval=0.0000006)
        input()
        main()

    except requests.exceptions.HTTPError as http_err:
        Write.Print(Center.XCenter(f"HTTP ошибка: {http_err}"), Colors.red_to_white, interval=0.0000006)
    except Exception as e:
        Write.Print(Center.XCenter(f"Ошибка: {str(e)}"), Colors.red_to_white, interval=0.0000006)

def main():
    clear()
    banner()
    Write.Print(Center.XCenter("\n\n\n【1】 Универсальный поиск\n【2】 Информация о IP-адрес"), Colors.green_to_white, interval=0.0000006)
    Write.Print("\nВыберите опцию: ", Colors.green_to_white, interval=0.0000006)
    
    
    choice = input()
    if choice == "1":
        Write.Print("\nВведите запрос: ", Colors.green_to_white, interval=0.0000006)
        request = input("")
        clear()
        search(request)
    elif choice == "2":
        Write.Print("\nВведите IP: ", Colors.green_to_white, interval=0.0000006)
        ip = input("")
        information_ip(ip)
        
    
if __name__ == "__main__":
    main()
