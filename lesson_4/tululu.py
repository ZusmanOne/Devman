from bs4 import BeautifulSoup
import requests
from pathlib import Path
from urllib.parse import urljoin, urlparse
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
    url = "https://tululu.org/l55/"
    for i in range(1, 2):
        url_book = urljoin(url, str(i))
        response_genre = requests.get(url_book)
        soup_genre = BeautifulSoup(response_genre.text, 'lxml')
        list_book = []
        if not response_genre.history:
            parse_book_page = soup_genre.find_all('table', class_='d_book')
            for i in parse_book_page:
                id_page = i.find('a').get('href')
                url_page = urljoin(url, id_page)
                response_page = requests.get(url_page)
                if not response_page.history:
                    about_book = {}
                    soup_page = BeautifulSoup(response_page.text, 'lxml')
                    parse_title = soup_page.find('h1').text
                    about_book['title'] = parse_title.split('::')[0].strip()
                    about_book['author'] = parse_title.split('::')[1].strip()
                    parse_comment = soup_page.find(id='content').find_all('span', {'class': 'black'})
                    about_book['comment'] = [i.text for i in parse_comment]
                    parse_genre = soup_page.find('span', class_='d_book').find_all('a')
                    about_book['genre'] = [i.text for i in parse_genre]
                    list_book.append(about_book)

        with open('about_book.json', 'w') as file:
            json.dump(list_book, file, ensure_ascii=False, indent=4)
    return list_book


download_description()
https://tululu.org/txt.php?id=239