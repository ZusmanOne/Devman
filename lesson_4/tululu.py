from bs4 import BeautifulSoup
import requests
from pathlib import Path
from urllib.parse import urljoin, urlparse

#
def parse_book_category():
    category_url = "https://tululu.org/l55/"
    response = requests.get(category_url)
    for i in range(1,11):
        url_book = urljoin(category_url, str(i))
        response = requests.get(url_book)
        soup = BeautifulSoup(response.text, 'lxml')
        find_book = soup.find_all('table', class_='d_book')
        for book in find_book:
            id_book = book.find('a').get('href')
            url_book = urljoin(category_url, id_book)
            print(url_book)


parse_book_category()

# url = urlparse("https://tululu.org/l55/3/")
# print(url)