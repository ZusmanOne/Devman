import os.path
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename, sanitize_filepath
from urllib.parse import urljoin, urlsplit

a = 10
payload = {'id': '2'}


def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError


def download_image():
    path = Path('image')
    path.mkdir(parents=False, exist_ok=True)
    url = "https://tululu.org"
    for i in range(1, 10):
        url_page = urljoin(url, 'b' + str(i)+'/')
        response = requests.get(url_page)
        soup = BeautifulSoup(response.text, 'lxml')
        tag_img = soup.find(class_='bookimage').find('img')['src']
        url_img = urljoin(url, tag_img)
        url_parse = urlsplit(url_img)
        response_img = requests.get(url_img)
        name_img = url_parse.path.split('/')[-1]
        with open(os.path.join(path, name_img), 'bw') as file:
            file.write(response_img.content)
        print(name_img)


def download_book():  # функция скачаивает книгу парсит названия и записывает по этому названию в файл
    main_url = "https://tululu.org/"  # сайт котоырй будем парсить
    url_title = urljoin(main_url, ('b' + str(payload['id']) + '/'))  # здесь к главному урлу добавляем конструкци bID
    response_title = requests.get(url_title)  # получаем респонс от запроса
    soup = BeautifulSoup(response_title.text, 'lxml')  # создаем суп для парсинга
    title_book_parse = soup.find('h1').text  # забираем запись стегом h1 (это имя книги)
    title = title_book_parse.split('::')[0].strip()  # убираем все лишнее и оставляем только название
    url_download = 'https://tululu.org/txt.php?'  # урл для скачивания
    path = Path('books')  # указывается путь
    path.mkdir(parents=False, exist_ok=True)  # создается папка с именем path
    payload['id'] = int(payload['id'])  # значение по ключу преобразуем в int
    response = requests.get(url_download, payload)  # получаем респонс от запроса

    if response.history:  # если запрос имеет перенаправление
        check_for_redirect(response)  # вызываем ф-ию которая в начале
    else:
        # with open(os.path.join(path, str(payload['id'])+'.' + title) + '.txt', 'bw') as file:
        #     file.write(response.content)  # записываем файл в виде директория/id_файла + название книги + расширение
        img_book_parse = soup.find(class_='bookimage').find('img')['src']
        url_img = urljoin(main_url, img_book_parse)
        print('Заголовок:',title.split('::')[0].strip(), '\n', url_img, sep='')


while int(payload['id']) <= a:  # переменная а это счетчик и количество книг которое будет скачиватсья
    try:
        download_book()
    except requests.exceptions.HTTPError:  # если отловлена такая ошибка то
        pass
    payload['id'] += 1  # увеличиваем этот счетчик вместе с id

# for i in range(1, 11):
#     url = "https://tululu.org/"
#     main_url = urljoin(url,('b'+ str(i)+ '/'))
#     response = requests.get(main_url)
#     if response.history:
#         print('редирект', response.url)
#     else:
#         print('пусто', response.url)
