import requests  #для работы с запросами через реквест происходит обращение на сайт и уже от туда вытягиваются все даннве
from bs4 import BeautifulSoup #библиотека разбивает html страницу, делает из нее объекты с которыми мы дальше и будем работать
import csv # создает csv файл

CSV = 'links_to_bar_info.csv'
HOST = 'https://www.restoclub.ru' # домен, который мы парсим
URL = 'https://www.restoclub.ru/msk/search/bar-moskvy' #точный адрес страницы
HEADERS ={
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
} #обновляем заголовки, чтобы сайт не понял, что мы скрипт

def get_html(url, params= ''): #создаем функцию которая возвращает значения из хтмл вводится туда в первую очередь url, параметры это то, как функция будет искать нужные данные
    r = requests.get(url, headers = HEADERS, params = params)
    return r

def get_content(html, page): #полусение конкретной информации в зависимости от того, какие параметры мы ввели в предыдущую функцию и что нам вернули
    soup = BeautifulSoup(html, 'html.parser') #создаем объект c входными данными
    if page >= 5:
        items = soup.find_all('div', class_='search-place-card')  # минус 3 часа моей жизни
    else:
        items = soup.find_all('div', class_='search-place-card _premium _platinum')  # а у них всего лишь разные классы ахах
    links_to_bar_info = []

    for item in items:
        links_to_bar_info.append(
            {
                'link_bar': HOST + item.find('div', class_='search-place-title__name').find('a').get('data-href')
            }
        )

    return links_to_bar_info

def save_document(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter= ';')
        writer.writerow(['Ссылка на страницу со всей инфой'])
        for item in items:
            writer.writerow([item['link_bar']])


def parser():
    PAGENATION = input('Укажите количество страниц для парсинга: ')
    PAGENATION = int(PAGENATION.strip())
    html = get_html(URL)
    if html.status_code == 200:
        links_to_bar_info = []
        for page in range(1, PAGENATION + 1):
            print(f'пошел парсинг. Страница: {page}' )
            url = URL + f'/{page}'
            html = get_html(url)
            links_to_bar_info.extend(get_content(html.text, page))
            print(links_to_bar_info)
        print(links_to_bar_info)
        print('Парсинг закончен')
    else:
        print('Error')

    save_document(links_to_bar_info, CSV)

parser()