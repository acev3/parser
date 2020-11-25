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
    response = requests.get(url, verify=False)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    id_book = url.split("/")[-2].strip("b")
    try:
        #title_tag = soup.find('div', id='content').find('h1')
        selector = "div#content h1"
        title_tag= soup.select_one(selector)
        title = title_tag.text.split("::")
        title_name = title[0].strip("  ")
        title_name = title_name.replace(u'\xa0', u' ')
        title_name = title_name.strip(" ")
        author = title[-1]
        author = author.replace(u'\xa0', u' ')
        author = author.strip(" ")
        #img_src = soup.find('div', class_='bookimage').find('img')['src']
        selector = ".bookimage img"
        img_src = soup.select_one(selector)['src']
        #comments = soup.find_all('div', class_="texts")
        selector = ".texts"
        comments = soup.select(selector)
        #genres = soup.find('span', class_='d_book').find_all('a')
        selector = "span.d_book a"
        genres = soup.select(selector)
        genres_list = []
        #print(title_name)
        for genre in genres:
            genres_list.append(genre.text)
        #print(title_name)
        title_name = title_name.split("/")[-1]
        #print(urljoin(url, img_src))
        img_src_1 = urljoin(url,img_src)
        #print(comments)
        #print(genres_list)
    except Exception as e:
        return None, None, None, None, None, None
    return title_name , img_src_1, comments, genres_list, author , id_book


def download_txt(url, filename, id_book, folder='books/'):
    """Функция для скачивания текстовых файлов.
    Args:
        url (str): Cсылка на текст, который хочется скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.
    Returns:
        str: Путь до файла, куда сохранён текст.
    """
    url = "http://tululu.org/txt.php?id=%s" % id_book
    response = requests.get(url, verify=False)
    response.raise_for_status()
    correct_filename = sanitize_filename(filename + '.txt')
    correct_folder = sanitize_filename(folder)
    filepath = os.path.join(correct_folder, correct_filename)
    if not os.path.exists(correct_folder):
        os.makedirs(correct_folder)
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
    response = requests.get(url, verify=False)
    response.raise_for_status()
    image = response.content
    correct_filename = sanitize_filename(url.split("/")[-1])
    correct_folder = sanitize_filename(folder)
    filepath = os.path.join(correct_folder, correct_filename)
    if not os.path.exists(correct_folder):
        os.mkdir(correct_folder)
    with open(filepath, 'wb') as file:
        file.write(image)
    return filepath

def save_comments(filename, text_list ,folder='comments/'):
    comments_list = []
    for comment in text_list:
        selector = ".black"
        com = comment.select_one(selector)
        #com = comment.find("span", class_="black")
        text = com.text
        comments_list.append(text)
        #correct_filename = sanitize_filename(filename.split("/")[-1])
        #correct_folder = sanitize_filename(folder)
        #filepath = os.path.join(correct_folder, correct_filename)
        #if not os.path.exists(correct_folder):
            #os.mkdir(correct_folder)
        #with open(filepath, 'a') as file:
            #file.write(text+"\n")
    #return filepath
    #print(comments_list)
    return comments_list


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-sp', '--start_page', default=1, type=int)
    parser.add_argument('-ep', '--end_page', default=702 ,type=int)
    return parser

def fantasy_book(url):
    response = requests.get(url, verify=False)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    #book_urls = soup.find_all('div', class_='bookimage')
    selector = ".bookimage a"
    book_urls = soup.select(selector)
    book_urls_list = []
    for book_url in book_urls:
        book_urls_list.append(urljoin(url, book_url['href']))
        #print(urljoin(url, book_url.find('a')['href']))
    return  book_urls_list


def main():
    url_base = 'http://tululu.org/l55/%s/'
    book_massive = []
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    start_page = namespace.start_page
    end_page = namespace.end_page
    for i in range(start_page, end_page):
        url = url_base % i
        book_urls = fantasy_book(url)
        for book_url in book_urls:
            print(book_url)
            try:
                book_info = {}
                url = book_url
                response = requests.get(url, verify=False)
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
                    # print(genres)
                    book_info['genres'] = genres
                # print(book_info)
                book_massive.append(book_info)
            except Exception as e:
                print(e)
    with open("books_info.json", "a", encoding='utf-8') as my_file:
        json.dump(book_massive, my_file, ensure_ascii=False)


if __name__ == '__main__':
    main()
