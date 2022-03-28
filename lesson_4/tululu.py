import os.path
from bs4 import BeautifulSoup
import requests
from pathlib import Path
from urllib.parse import urljoin, urlparse, urlsplit
import json
import argparse

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

parser = argparse.ArgumentParser()
parser.add_argument('--start', help='Ввелите номер страницы с какой начать скачивать', type=int)
parser.add_argument('--end', default=702, help='Введите номер конечной страницы  скачивания', type=int)
args = parser.parse_args()


def download_description(start, end):
    url_main = "https://tululu.org"
    url = "https://tululu.org/l55/"
    url_dwnld = "https://tululu.org/txt.php"
    path_image = Path('image')
    path_image.mkdir(parents=False, exist_ok=True)
    path_book = Path('book')
    path_book.mkdir(parents=False, exist_ok=True)
    for i in range(start, end): # в цикле указываюется диапазон страниц с какой по какую скачивать
        url_book = urljoin(url, str(i))  # урл списка книг по жанрам (по странично)
        response_genre = requests.get(url_book)
        soup_genre = BeautifulSoup(response_genre.text, 'lxml')
        list_book = []
        if not response_genre.history:
            selector = "table.d_book"
            parse_book_page = soup_genre.select(selector)
            for i in parse_book_page: # цикл идет по каждой книжке на странице
                id_page = i.find('a').get('href')  # получем id книги
                id_txt = id_page.strip('/b') # От id книги отбрасывается все кроме цифр, что бы получить урл для скачки
                response_dwnld = requests.get(url_dwnld, {'id':id_txt})  # урл для скачки
                url_page = urljoin(url, id_page)  # формируется урл книги
                response_page = requests.get(url_page)
                if not response_page.history:
                    about_book = {}
                    soup_page = BeautifulSoup(response_page.text, 'lxml')
                    selector_title = "h1"
                    parse_title = soup_page.select_one(selector_title).text
                    about_book['title'] = parse_title.split('::')[0].strip()
                    # about_book['author'] = parse_title.split('::')[1].strip()
                    select_comment = "#content span.black"  # замена нижней строчке (для id добавилась #)
                    # parse_comment = soup_page.find(id='content').find_all('span', {'class': 'black'})
                    parse_comment = soup_page.select(select_comment)
                    about_book['comment'] = [i.text for i in parse_comment]
                    select_genre = "span.d_book a"  # замена нижней строчке
                    # parse_genre = soup_page.find('span', class_='d_book').find_all('a')
                    parse_genre = soup_page.select(select_genre)
                    about_book['genre'] = [i.text for i in parse_genre]
                    parse_image = soup_page.find(class_='bookimage').find('img')['src']
                    url_image = urljoin(url_main, parse_image)
                    response_image = requests.get(url_image)
                    url_parse = urlsplit(url_image)
                    about_book['image_src'] = os.path.join(path_image, url_parse.path.split('/')[-1])
                    list_book.append(about_book)
                    print(url_page, response_dwnld.history)
                    if not response_dwnld.history:
                        with open(os.path.join(path_book, str(id_txt)+'.'+about_book['title']+'.txt'), 'bw') as file:
                            file.write(response_dwnld.content)
                        with open(os.path.join(path_image, url_parse.path.split('/')[-1]), 'bw') as image:
                            image.write(response_image.content)



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
# #                 file.write(response_dwnld.content)
# dfdf


download_description(args.start, args.end)
