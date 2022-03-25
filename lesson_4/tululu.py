import os.path

from bs4 import BeautifulSoup
import requests
from pathlib import Path
from urllib.parse import urljoin, urlparse, urlsplit
import json


# def parse_book_category():
#     category_url = "https://tululu.org/l55/"
#     response = requests.get(category_url)
#     for i in range(1,11):
#         url_book = urljoin(category_url, str(i))
#         response = requests.get(url_book)
#         soup = BeautifulSoup(response.text, 'lxml')
#         find_book = soup.find_all('table', class_='d_book')
#         for book in find_book:
#             id_book = book.find('a').get('href')
#             url_book = urljoin(category_url, id_book)
#             print(url_book)


def download_description():
    url_main = "https://tululu.org"
    url = "https://tululu.org/l55/"
    url_dwnld = "https://tululu.org/txt.php"
    path_image = Path('image')
    path_image.mkdir(parents=False, exist_ok=True)
    path_book = Path('book')
    path_book.mkdir(parents=False, exist_ok=True)
    for i in range(1, 2):
        url_book = urljoin(url, str(i)) # урл списка книг по жанрам (по странично)
        print(url_book)
        response_genre = requests.get(url_book)
        soup_genre = BeautifulSoup(response_genre.text, 'lxml')
        list_book = []
        if not response_genre.history:
            parse_book_page = soup_genre.find_all('table', class_='d_book')
            for i in parse_book_page:
                id_page = i.find('a').get('href')
                id_txt = id_page.strip('/b')
                response_dwnld = requests.get(url_dwnld, {'id':id_txt})
                url_page = urljoin(url, id_page)
                response_page = requests.get(url_page)
                if not response_page.history and not response_dwnld.history:
                    about_book = {}
                    soup_page = BeautifulSoup(response_page.text, 'lxml')
                    parse_title = soup_page.find('h1').text
                    about_book['title'] = parse_title.split('::')[0].strip()
                    about_book['author'] = parse_title.split('::')[1].strip()
                    parse_comment = soup_page.find(id='content').find_all('span', {'class': 'black'})
                    about_book['comment'] = [i.text for i in parse_comment]
                    parse_genre = soup_page.find('span', class_='d_book').find_all('a')
                    about_book['genre'] = [i.text for i in parse_genre]
                    parse_image = soup_page.find(class_='bookimage').find('img')['src']
                    url_image = urljoin(url_main,parse_image)
                    response_image = requests.get(url_image)
                    url_parse = urlsplit(url_image)
                    about_book['image_src'] = os.path.join(path_image, url_parse.path.split('/')[-1])
                    with open(os.path.join(path_book, str(id_txt)+'.'+about_book['title']+'.txt'), 'bw') as file:
                        file.write(response_dwnld.content)
                    with open(os.path.join(path_image, url_parse.path.split('/')[-1]), 'bw') as image:
                        image.write(response_image.content)

                    list_book.append(about_book)

        with open('about_book.json', 'w') as file:
            json.dump(list_book, file, ensure_ascii=False, indent=4)
    return list_book

# https://tululu.org/txt.php?id=239
# def download_txt():
#     path = Path('books')
#     path.mkdir(parents=False, exist_ok=True)
#     url = "https://tululu.org/txt.php"
#     url_main = "https://tululu.org/"
#     for i in range(1,10):
#         response_dwnld = requests.get(url, {'id':str(i)})
#         url_book = urljoin(url_main, 'b'+str(i)+'/')
#         response_book = requests.get(url_book)
#         if not response_dwnld.history and not response_book.history:
#             soup = BeautifulSoup(response_book.text, 'lxml')
#             parse_title = soup.find('h1').text
#             title = str(i)+'.' + parse_title.split('::')[0].strip() + '.txt'
#             with open(os.path.join(path, title), 'bw') as file:
#                 file.write(response_dwnld.content)


download_description()
