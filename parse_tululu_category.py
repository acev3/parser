import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import sys
import argparse
import requests
from pathvalidate import sanitize_filename
import os


def parse_title(url):
    response = check_response(url)
    soup = BeautifulSoup(response.text, 'lxml')
    id_book = url.split("/")[-2].strip("b")
    title_name = None
    img_src = None
    comments = None
    genres_list = None
    author = None
    id_book = None
    selector = "div#content h1"
    title_tag = soup.select_one(selector)
    title = title_tag.text.split("::")
    title_name = title[0].strip()
    title_name = title_name.replace(u'\xa0', u' ')
    title_name = title_name.strip()
    author = title[-1]
    author = author.replace(u'\xa0', u' ')
    author = author.strip()
    selector = ".bookimage img"
    img_src = soup.select_one(selector)['src']
    selector = ".texts"
    comments = soup.select(selector)
    selector = "span.d_book a"
    genres = soup.select(selector)
    genres_list = [genre.text for genre in genres]
    title_name = title_name.split("/")[-1]
    img_src = urljoin(url, img_src)
    return title_name, img_src, comments, genres_list, author, id_book


def download_txt(filename, id_book, folder='books/'):
    """Функция для скачивания текстовых файлов.
    Args:
        url (str): Cсылка на текст, который хочется скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.
    Returns:
        str: Путь до файла, куда сохранён текст.
    """
    url = "https://tululu.org/txt.php?id=%s" % id_book
    response = check_response(url)
    correct_filename = sanitize_filename(filename + '.txt')
    correct_folder = sanitize_filename(folder)
    filepath = os.path.join(correct_folder, correct_filename)
    os.makedirs(correct_folder, exist_ok=True)
    with open(filepath, 'w') as file:
        file.write(response.text)
    return filepath

def download_image(url, folder='images/'):
    """Функция для скачивания текстовых файлов.
    Args:
        url (str): Cсылка на текст, который хочется скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.
    Returns:
        str: Путь до файла, куда сохранён текст.
    """
    response = check_response(url)
    image = response.content
    correct_filename = sanitize_filename(url.split("/")[-1])
    correct_folder = sanitize_filename(folder)
    filepath = os.path.join(correct_folder, correct_filename)
    os.makedirs(correct_folder, exist_ok=True)
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
    response = check_response(url)
    soup = BeautifulSoup(response.text, 'lxml')
    selector = ".bookimage a"
    book_urls = soup.select(selector)
    book_urls_list = []
    for book_url in book_urls:
        book_urls_list.append(urljoin(url, book_url['href']))
    return book_urls_list


def check_response(url):
    response = requests.get(url, verify=False, allow_redirects=False)
    response.raise_for_status()
    if response.status_code == 301:
        raise requests.HTTPError('Redirect')
    return response

def main():
    url_base = 'https://tululu.org/l55/%s/'
    books = []
    parser = create_parser()
    namespace = parser.parse_args()
    start_page = namespace.start_page
    end_page = namespace.end_page
    dest_folder = namespace.dest_folder
    skip_imgs = namespace.skip_imgs
    skip_txt = namespace.skip_txt
    json_path = namespace.json_path
    json_filename = os.path.join(dest_folder, json_path)
    books_folder = os.path.join(dest_folder, "books")
    image_folder = os.path.join(dest_folder, "images")
    for page in range(start_page, end_page):
        url = url_base % page
        book_urls = get_books_urls(url)
        for book_url in book_urls:
            try:
                book = {}
                check_response(book_url)
                filename, img_src, comments, genres, author, id_book = parse_title(book_url)
                book['book_path'] = None
                if not skip_txt:
                    if filename:
                        book['title'] = filename
                        book_path = download_txt(filename, id_book, books_folder)
                        book['book_path'] = book_path
                    if author:
                        book['author'] = author
                book['image_src'] = None
                if not skip_imgs:
                    if img_src:
                        image_src = download_image(img_src, image_folder)
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
