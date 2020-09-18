import requests
from pathvalidate import sanitize_filename
import os

def download_txt(url, filename, id_book, folder='books/'):
    """Функция для скачивания текстовых файлов.
    Args:
        url (str): Cсылка на текст, который хочется скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.
    Returns:
        str: Путь до файла, куда сохранён текст.
    """
    # TODO: Здесь ваша реализация

    url = "http://tululu.org/txt.php?id=%s" % id_book
    response = requests.get(url)
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
    # TODO: Здесь ваша реализация
    response = requests.get(url)
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
        com = comment.find("span", class_="black")
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
    return comments_list


"""
# Примеры использования
url = 'http://tululu.org/txt.php?id=1'

filepath = download_txt(url, 'Алиби')
print(filepath)  # Выведется books/Алиби.txt

filepath = download_txt(url, 'Али/би', folder='books/')
print(filepath)  # Выведется books/Алиби.txt

filepath = download_txt(url, 'Али\\би', folder='txt/')
print(filepath)  # Выведется txt/Алиби.txt
"""