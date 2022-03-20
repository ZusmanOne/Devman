import os.path
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename, sanitize_filepath
from urllib.parse import urljoin


def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError


a = 10
payload = {'id': '1'}


def download_book():
    main_url = "https://tululu.org/"
    url_title = urljoin(main_url, ('b' + str(payload['id']) + '/'))
    response_title = requests.get(url_title)
    soup = BeautifulSoup(response_title.text, 'lxml')
    title_book_parse = soup.find('h1').text
    title = title_book_parse.split('::')[0].strip()
    url_download = 'https://tululu.org/txt.php?'
    path = Path('books')
    path.mkdir(parents=False, exist_ok=True)
    payload['id'] = int(payload['id'])
    response = requests.get(url_download, payload)
    if response.history:
        check_for_redirect(response)
    else:
        with open(os.path.join(path, str(payload['id'])+'.' + title) + '.txt', 'bw') as file:
            file.write(response.content)


while int(payload['id']) <= a:
    try:
        download_book()
    except requests.exceptions.HTTPError:
        print('Не скачана')
    payload['id'] += 1

# for i in range(1, 11):
#     url = "https://tululu.org/"
#     main_url = urljoin(url,('b'+ str(i)+ '/'))
#     response = requests.get(main_url)
#     if response.history:
#         print('редирект', response.url)
#     else:
#         print('пусто', response.url)
