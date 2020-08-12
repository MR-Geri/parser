import requests
from bs4 import BeautifulSoup


URL = 'http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing=8880'


def get_html(url, params=None):
    r = requests.get(url, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    # items = soup.find_all('a', class_='na-card-item')
    print(soup.split())


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text)
    else:
        print('ERROR')


if __name__ == '__main__':
    parse()
