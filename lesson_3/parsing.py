import os.path
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from pathvalidate import sanitize_filename, sanitize_filepath
from urllib.parse import urljoin, urlparse, urlsplit
from pathlib import Path


# url = "https://tululu.org/b5/"
# response = requests.get(url)
# response.raise_for_status()
# # print(response.text)
# soup = BeautifulSoup(response.text, 'lxml')
# title_tag = soup.find('h1').text
# img_tag = soup.find(class_='bookimage').find('img')['src']
# url_img = urljoin('https://tululu.org', img_tag)
# #print(title_tag.split('::')[0].strip(), title_tag.split('::')[1].strip(), sep='\n')
# print(url_img)

# https://tululu.org/shots/5.jpg

#
# def download_txt(url, filename, folder='books/'):
#     path = Path(folder)
#     path.mkdir(parents=False, exist_ok=True)
#     response = requests.get(url)
#     filename = sanitize_filename(filename +'.txt')
#     with open(os.path.join(folder, filename), 'bw') as file:
#         file.write(response.content)
#     return sanitize_filepath(os.path.join(folder, filename))
#
#
# url = 'http://tululu.org/txt.php?id=1'
# filepath = download_txt(url, 'Али\\би', folder='txt/')
# print(filepath)


