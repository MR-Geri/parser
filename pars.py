import datetime
import requests
from bs4 import BeautifulSoup
import csv
from multiprocessing import Process
import json


URL = 'https://www.avito.ru/lipetsk/mebel_i_interer/myagkaya_mebel-ASgBAgICAURaqgI?q=диван'
host = 'https://www.avito.ru/'


def get_html(url, params=None):
    try:
        return requests.get(url, params=params)
    except:
        print('ERROR')


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='snippet-horizontal')
    data = []
    for i in items:
        data.append({
            'name': i.find('a', class_='snippet-link').get_text(strip=True),
            'url': host + i.find('a', class_='snippet-link').get('href'),
            'RUB': i.find('div', class_='snippet-price-row').get_text(strip=True)[:-3],
            'place': i.find('div', class_='item-address-georeferences').get_text(strip=True),
            'time': i.find('div', class_='snippet-date-row').get_text(strip=True)
        })
    return data


def get_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    return int(soup.find('div', class_='pagination-root-2oCjZ').find_all('span')[-2].get_text())


def multiprocess(beginning, end):
    data = []
    for num in range(beginning, end + 1):
        data.extend(get_content(get_html(URL, params={'p': num}).text))
    try:
        d = json.load(open('data.json'))
    except:
        d = []
        print('Была ошибка в считывании информации')
    d.extend(data)
    try:
        with open("data.json", "w") as write_file:
            json.dump(d, write_file)
    except:
        print('Была ошибка в записи информации')


def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название', 'Сслыка', 'Цена', 'Место', 'Время с момента публикации'])
        for i in items:
            writer.writerow([i['name'], i['url'], i['RUB'], i['place'], i['time']])

    
def parse_process(process=5):
    html = get_html(URL)
    if html.status_code == 200:
        pages = get_page(html.text)
        data_process = []
        last = 0
        print(f'Начало {process} парсинга')
        for num in range(0, pages, process):
            data_process.append(Process(target=multiprocess, args=(num + 1, num + process)))
            last = num
        if pages % process != 0:
            process = Process(target=multiprocess, args=(last + 1, pages))
            data_process.append(process)
            process.start()
        for i in data_process:
            i.join()
        d = json.load(open('data.json'))
        save_file(d, f'file_{process}_process.csv')
        print(f'Конец {process} парсинга')
    else:
        print(f'{html.status_code} ERROR')


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        pages = get_page(html.text)
        data_set = []
        for num in range(1, pages + 1):
            print(f'Парсинг {num} страницы из {pages}...')
            data_set.extend(get_content(get_html(URL, params={'p': num}).text))
        save_file(data_set, 'file_1_process.csv')
    else:
        print(f'{html.status_code} ERROR')


if __name__ == '__main__':
    date = datetime.datetime.now()
    parse_process()
    print(datetime.datetime.now() - date)
    date = datetime.datetime.now()
    parse()
    print(datetime.datetime.now() - date)
