import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

from file import download_txt, download_image, save_comments
from tululu import title_parser

def fantasy_book(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    book_urls = soup.find_all('div', class_='bookimage')
    book_urls_list = []
    for book_url in book_urls:
        book_urls_list.append(urljoin(url, book_url.find('a')['href']))
        #print(urljoin(url, book_url.find('a')['href']))
    return  book_urls_list


if __name__ == '__main__':
    url_base = 'http://tululu.org/l55/%s/'
    book_massive = []
    for i in range(1, 5):
        print(i)
        url = url_base % i
        book_urls_list = fantasy_book(url)
        for book_url in book_urls_list:
            try:
                book_info = {}
                url = book_url
                response = requests.get(url)
                response.raise_for_status()
                filename, img_src, comments, genres, author, id_book = title_parser(url)
                if filename:
                    book_info['title'] = filename
                    book_path = download_txt(url, filename, id_book)
                    book_info['book_path'] = book_path
                if author:
                    book_info['author'] = author
                if img_src:
                    image_src = download_image(img_src)
                    book_info['img_src'] = image_src
                if comments:
                    comments_list = save_comments(filename, comments)
                    book_info['comments'] = comments_list
                if genres:
                    #print(genres)
                    book_info['genres'] = genres
                #print(book_info)
                book_massive.append(book_info)
            except Exception as e:
                print(e)
    with open("books_info.json", "a", encoding='utf-8') as my_file:
        json.dump(book_massive, my_file, ensure_ascii=False)