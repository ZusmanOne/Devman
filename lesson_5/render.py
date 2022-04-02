from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os.path
from bs4 import BeautifulSoup
import requests
from pathlib import Path
from urllib.parse import urljoin, urlparse, urlsplit
import json
import argparse
from livereload import Server
from more_itertools import chunked
import math


parser = argparse.ArgumentParser()
parser.add_argument('--start', help='Ввелите номер страницы с какой начать скачивать', type=int)
parser.add_argument('--end', default=702, help='Введите номер конечной страницы  скачивания', type=int)
args = parser.parse_args()


# def download_description(start, end):
#     url_main = "https://tululu.org"
#     url = "https://tululu.org/l55/"
#     url_dwnld = "https://tululu.org/txt.php"
#     path_image = Path('image')
#     path_image.mkdir(parents=False, exist_ok=True)
#     path_book = Path('book')
#     path_book.mkdir(parents=False, exist_ok=True)
#     list_book = []
#     for i in range(start, end): # в цикле указываюется диапазон страниц с какой по какую скачивать
#         url_book = urljoin(url, str(i))  # урл списка книг по жанрам (по странично)
#         response_genre = requests.get(url_book)
#         soup_genre = BeautifulSoup(response_genre.text, 'lxml')
#         if not response_genre.history:
#             selector = "table.d_book"
#             parse_book_page = soup_genre.select(selector)
#             for i in parse_book_page: # цикл идет по каждой книжке на странице
#                 id_page = i.find('a').get('href')  # получем id книги
#                 id_txt = id_page.strip('/b') # От id книги отбрасывается все кроме цифр, что бы получить урл для скачки
#                 response_dwnld = requests.get(url_dwnld, {'id':id_txt})  # урл для скачки
#                 url_page = urljoin(url, id_page)  # формируется урл книги
#                 response_page = requests.get(url_page)
#                 # print(url_page,response_page.history)
#                 if not response_page.history and not response_dwnld.history:
#                     about_book = {}
#                     soup_page = BeautifulSoup(response_page.text, 'lxml')
#                     selector_title = "h1"
#                     parse_title = soup_page.select_one(selector_title).text
#                     about_book['title'] = parse_title.split('::')[0].strip()
#                     about_book['author'] = parse_title.split('::')[1].strip()
#                     # about_book['author'] = parse_title.split('::')[1].strip()
#                     select_comment = "#content span.black"  # замена нижней строчке (для id добавилась #)
#                     # parse_comment = soup_page.find(id='content').find_all('span', {'class': 'black'})
#                     parse_comment = soup_page.select(select_comment)
#                     about_book['comment'] = [i.text for i in parse_comment]
#                     select_genre = "span.d_book a"  # замена нижней строчке
#                     # parse_genre = soup_page.find('span', class_='d_book').find_all('a')
#                     parse_genre = soup_page.select(select_genre)
#                     about_book['genre'] = [i.text for i in parse_genre]
#                     parse_image = soup_page.find(class_='bookimage').find('img')['src']
#                     url_image = urljoin(url_main, parse_image)
#                     response_image = requests.get(url_image)
#                     url_parse = urlsplit(url_image)
#                     about_book['image_src'] = os.path.join(path_image, url_parse.path.split('/')[-1])
#                     about_book['alt_img'] = parse_title.split('::')[0].strip()
#                     about_book['path_book'] = os.path.join(path_book, str(id_txt) + '.' + about_book['title'] + '.txt')
#                     with open(os.path.join(path_book, str(id_txt)+'.'+about_book['title']+'.txt'), 'bw') as file:
#                         file.write(response_dwnld.content)
#                     with open(os.path.join(path_image, url_parse.path.split('/')[-1]), 'bw') as image:
#                         image.write(response_image.content)
#                     list_book.append(about_book)
#                     with open('about_book.json', 'w') as file:
#                         json.dump(list_book, file, ensure_ascii=False, indent=4)
#             print(len(list_book))
#
#
# download_description(args.start, args.end)

#
# server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
# server.serve_forever()


def on_reload():  # функция рендерит и сохраняет из book.html(его правим) в index.html
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('book.html')
    with open("about_book.json", "r") as my_file:  # достает данные из файла
        capitals_json = my_file.read()

    capitals = json.loads(capitals_json)  # преоброзон в список
    page_path = Path('pages')
    page_path.mkdir(parents=False, exist_ok=True)

    for i, chunk in enumerate(list(chunked(capitals, 10)), 1):
        """
        данный цикл разбивает файл с данными о книгах сформированный в виде списка, по группам из трех книг(так задано)
        с помощью метода chunked, затем индексируем(нумериуем с помощью numerate) кажду разбитую группу, и потом каждую
        группу записываем в отдельный index.html
        """




        page = template.render(  # создаем контекст из трех книг для шаблона(словарь)
            book=chunk,
            num=math.ceil(len(capitals)/10),


        )

        with open(os.path.join(page_path, 'index' + str(i)+'.html'), 'w', encoding='utf8') as file:
            file.write(page)
        # print(len(list(chunked(capitals, 10))))


on_reload()

#
server = Server()  # позволяет отслеживать изменения без перезагрузки сервера
server.watch('book.html', on_reload)
server.serve(root='.')


# my_list = [1,2,3,4,5,6,7,8,9,10]
# my_chunk = list(chunked(my_list,3))
# for i,chunk in enumerate(my_chunk,1):
