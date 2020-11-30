import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import sys
import argparse
import requests
from pathvalidate import sanitize_filename
import os


def title_parser(url):
    response = response_check(url)
    soup = BeautifulSoup(response.text, 'lxml')
    id_book = url.split("/")[-2].strip("b")
    try:
        selector = "div#content h1"
        title_tag = soup.select_one(selector)
        title = title_tag.text.split("::")
        title_name = title[0].strip("  ")
        title_name = title_name.replace(u'\xa0', u' ')
        title_name = title_name.strip(" ")
        author = title[-1]
        author = author.replace(u'\xa0', u' ')
        author = author.strip(" ")
        selector = ".bookimage img"
        img_src = soup.select_one(selector)['src']
        selector = ".texts"
        comments = soup.select(selector)
        selector = "span.d_book a"
        genres = soup.select(selector)
        genres_list = []
        for genre in genres:
            genres_list.append(genre.text)
        title_name = title_name.split("/")[-1]
        img_src = urljoin(url, img_src)
    except Exception as e:
        return None, None, None, None, None, None
    return title_name , img_src, comments, genres_list, author, id_book


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
    response = response_check(url)
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
    response = response_check(url)
    image = response.content
    correct_filename = sanitize_filename(url.split("/")[-1])
    correct_folder = sanitize_filename(folder)
    filepath = os.path.join(correct_folder, correct_filename)
    os.makedirs(correct_folder, exist_ok=True)
    with open(filepath, 'wb') as file:
        file.write(image)
    return filepath

def save_comments(filename, text_list ,folder='comments/'):
    comments_list = []
    for comment in text_list:
        selector = ".black"
        com = comment.select_one(selector)
        text = com.text
        comments_list.append(text)
    return comments_list


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
    response = response_check(url)
    soup = BeautifulSoup(response.text, 'lxml')
    selector = ".bookimage a"
    book_urls = soup.select(selector)
    book_urls_list = []
    for book_url in book_urls:
        book_urls_list.append(urljoin(url, book_url['href']))
    return book_urls_list


def response_check(url):
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
                url = book_url
                response_check(url)
                filename, img_src, comments, genres, author, id_book = title_parser(url)
                if skip_txt:
                    book['book_path'] = None
                else:
                    if filename:
                        book['title'] = filename
                        book_path = download_txt(filename, id_book, books_folder)
                        book['book_path'] = book_path
                    if author:
                        book['author'] = author
                if skip_imgs:
                    book['image_src'] = None
                else:
                    if img_src:
                        image_src = download_image(img_src, image_folder)
                        book['img_src'] = image_src
                if comments:
                    comments_list = save_comments(filename, comments)
                    book['comments'] = comments_list
                if genres:
                    book['genres'] = genres
                books.append(book)
            except Exception as e:
                print(e)
    with open(json_filename, "a", encoding='utf-8') as my_file:
        json.dump(books, my_file, ensure_ascii=False)


if __name__ == '__main__':
    main()
