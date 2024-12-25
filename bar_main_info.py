import time
import random

import requests  #для работы с запросами через реквест происходит обращение на сайт и уже от туда вытягиваются все даннве
from bs4 import BeautifulSoup #библиотека разбивает html страницу, делает из нее объекты с которыми мы дальше и будем работать
import csv # создает csv файл

CSV = 'all_main_info_about_bar.csv'
HOST = 'https://www.restoclub.ru'
HEADERS ={
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
} #обновляем заголовки, чтобы сайт не понял, что мы скрипт
URLS = []

def get_html(url, params= ''): #создаем функцию которая возвращает значения из хтмл вводится туда в первую очередь url, параметры это то, как функция будет искать нужные данные
    r = requests.get(url, headers = HEADERS, params = params)
    return r

def get_content(html,url): #полусение конкретной информации в зависимости от того, какие параметры мы ввели в предыдущую функцию и что нам вернули
    soup = BeautifulSoup(html, 'html.parser') #создаем объект c входными данными
    items = soup.find_all('div', class_='DesktopLayout_DesktopLayoutContainer__oJYp_ container')
    information_about_bars = []


    # выносим все эдементы из аппента ибо я замаялась исправлять ошибки
    for item in items:
        title = item.find('div', class_='d-flex align-items-start gap-24')
        phone = item.find('div', class_='Phone_PhoneWrapper__HHihF')
        address =  item.find('div', class_='InfoItem_InfoItem__GpKN4')
        metro = item.find('span', class_='Subway_SubwayName__dLFOK')
        rating = item.find('div', class_= 'color-white fs-24 fw-700 lh-24')
        if url >= 2:
            avg_bill = item.find('span', class_='AverageBill_AverageBillTitle__udcrI d-flex')
        else:
            avg_bill= item.find('span', class_='AverageBill_AverageBillTitlePrice__2pz67 text-decoration-underline ml-4 cursor-pointer')
        time_work = item.find('span', class_='WorkingHours_WorkingHoursLink__nnN24')
        file_menu = item.find('div', class_='FileMenu_FileMenuList__d0XTq')
        comments = item.find('button', class_ = 'Button_Button__OH_rT RatingOverallCompact_CountButton__GfQkH Button_ButtonVariantLink__5A_tD Button_ButtonSizeMedium__DAxjh Button_ButtonThemeClear___EFgO')

        information_about_bars.append(
            {
                'title': title.get_text().replace('Клуб', '').replace('8.8211 отзыв', '') if title else 'неизвесно',
                'phone': phone.get_text().replace('Показать', '') if phone else 'неизвесно',
                'address': address.find('span').get_text(strip=True) if address else 'неизвесно',
                'metro': metro.get_text(strip=True) if metro else 'неизвесно',
                'rating': rating.get_text(strip=True) if rating else 'неизвесно',
                'avg_bill': avg_bill.get_text(strip=True) if avg_bill else 'неизвесно',
                'time_work': time_work.get_text(strip=True) if time_work else 'неизвесно',
                'file_menu': HOST + file_menu.find('a').get('href') if file_menu else 'неизвесно',
                'comments': comments.get_text(strip=True).replace(' отзыв', '').replace('ов', '').replace('а', '') if comments else 'неизвесно',
            }
        )


    return information_about_bars

def save_document(items, path):
    with open(path, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter= ';')
        for item in items:
            writer.writerow([item['title'],item['address'],item['metro'],item['phone'],item['avg_bill'],item['rating'],item['comments'],item['file_menu'],item['time_work'],])

def read_from_document():
    with open('links_to_bar_info.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        next(reader) # 'Это чтоб заголовок пропускать, а то получается у первого ошибка из-за того, что ему передают текст, а не ссылку
        for row in reader:
            URLS.append(row)

def parser():
    read_from_document()
    information_about_bars = []
    for url in range(len(URLS)):
        try:
            html = get_html(URLS[url][0])
            if html.status_code == 200:
                print(url)
                print(f'Пошла жара. Сысыслка номер: {URLS[url][0]}')
                information_about_bars.extend(get_content(html.text,url ))
                save_document(information_about_bars, CSV)
            else:
                print('Ерроре')
        except Exception as e:
            print(f'У меня нет времени на ошибки. Я должен работать {URLS[url]}: {e}')
            continue
        time.sleep(random.uniform(1, 3))
    print(information_about_bars)
    print('Парсинг закончен')



parser()