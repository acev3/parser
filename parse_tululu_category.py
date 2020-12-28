import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import sys
import argparse
import requests
from pathvalidate import sanitize_filename
import os

def parse_title(url, response):
    soup = BeautifulSoup(response.text, 'lxml')
    book_id = url.split("/")[-2].strip("b")
    title_tag = soup.select_one("div#content h1")
    title, author = title_tag.text.split("::")
    title = title.strip().replace(u'\xa0', u' ').strip().split("/")[-1]
    author = author.replace(u'\xa0', u' ').strip()
    img_src = soup.select_one(".bookimage img")['src']
    comments = soup.select(".texts")
    genres = soup.select("span.d_book a")
    genres = [genre.text for genre in genres]
    img_src = urljoin(url, img_src)
    return title, img_src, comments, genres, author, book_id

def download_txt(filename, book_id, folder='books/'):
    """Функция для скачивания текстовых файлов.
    Args:
        url (str): Cсылка на текст, который хочется скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.
    Returns:
        str: Путь до файла, куда сохранён текст.
    """
    url = "https://tululu.org/txt.php?id=%s" % book_id
    response = check_response(requests.get(url, verify=False, allow_redirects=False))
    correct_filename = sanitize_filename(book_id + filename + '.txt')
    filepath = os.path.join(folder, correct_filename)
    os.makedirs(folder, exist_ok=True)
    with open(filepath, 'w') as file:
        file.write(response.text)
    return filepath

def download_image(url, book_id, folder='images/'):
    """Функция для скачивания текстовых файлов.
    Args:
        url (str): Cсылка на текст, который хочется скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.
    Returns:
        str: Путь до файла, куда сохранён текст.
    """
    response = check_response(requests.get(url, verify=False, allow_redirects=False))
    image = response.content
    correct_filename = sanitize_filename(book_id + url.split("/")[-1])
    filepath = os.path.join(folder, correct_filename)
    os.makedirs(folder, exist_ok=True)
    with open(filepath, 'wb') as file:
        file.write(image)
    return filepath

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-sp', '--start_page', default=1, type=int)
    parser.add_argument('-ep', '--end_page', default=702, type=int)
    parser.add_argument('-df', '--dest_folder', type=str, default="")
    parser.add_argument('-si', '--skip_imgs', action='store_const', const=True)
    parser.add_argument('-st', '--skip_txt', action='store_const', const=True)
    parser.add_argument('-jp', '--json_path', type=str, default="books_info.json")
    return parser

def get_books_urls(url):
    response = check_response(requests.get(url, verify=False, allow_redirects=False))
    soup = BeautifulSoup(response.text, 'lxml')
    selector = ".bookimage a"
    book_urls = soup.select(selector)
    return [urljoin(url, book_url['href']) for book_url in book_urls]

def check_response(response):
    response.raise_for_status()
    if response.history:
        raise requests.HTTPError('Redirect')
    return response

def main():
    url_base = 'https://tululu.org/l55/%s/'
    books = []
    parser = create_parser()
    namespace = parser.parse_args()
    json_filename = os.path.join(namespace.dest_folder, namespace.json_path)
    books_folder = os.path.join(namespace.dest_folder, "books")
    image_folder = os.path.join(namespace.dest_folder, "images")
    for page in range(namespace.start_page, namespace.end_page):
        url = url_base % page
        book_urls = get_books_urls(url)
        for book_url in book_urls:
            try:
                book = {}
                response = check_response(requests.get(book_url, verify=False, allow_redirects=False))
                filename, img_src, comments, genres, author, book_id = parse_title(book_url, response)
                book['book_path'] = None
                if not namespace.skip_txt:
                    if filename:
                        book['title'] = filename
                        book_path = download_txt(filename, book_id, books_folder)
                        book['book_path'] = book_path
                    if author:
                        book['author'] = author
                book['image_src'] = None
                if not namespace.skip_imgs:
                    if img_src:
                        image_src = download_image(img_src, book_id, image_folder)
                        book['img_src'] = image_src
                if comments:
                    comments_list = [comment.select_one(".black") for comment in comments]
                    book['comments'] = comments_list
                if genres:
                    book['genres'] = genres
                books.append(book)
            except TimeoutError as e:
                print(e)
            except TypeError as e:
                print(e)
            except ValueError as e:
                print(e)
    with open(json_filename, "a", encoding='utf-8') as my_file:
        json.dump(books, my_file, ensure_ascii=False)


if __name__ == '__main__':
    main()
