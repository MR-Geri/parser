import requests
from bs4 import BeautifulSoup
import csv


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
    print(data)
    return data


def get_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    return int(soup.find('div', class_='pagination-root-2oCjZ').find_all('span')[-2].get_text())


def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название', 'Сслыка', 'Цена', 'Место', 'Время с момента публикации'])
        for i in items:
            writer.writerow([i['name'], i['url'], i['RUB'], i['place'], i['time']])

    
def parse():
    html = get_html(URL)
    if html.status_code == 200:
        pages = get_page(html.text)
        data_set = []
        for num in range(1, pages + 1):
            print(f'Парсинг {num} страницы из {pages}...')
            data_set.extend(get_content(get_html(URL, params={'p': num}).text))
        save_file(data_set, 'file.csv')
    else:
        print('ERROR')


if __name__ == '__main__':
    parse()
