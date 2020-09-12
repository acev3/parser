import requests
from pathvalidate import sanitize_filename
import os

def download_txt(url, filename, folder='books/'):
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
    correct_filename = sanitize_filename(filename + '.txt')
    correct_folder = sanitize_filename(folder)
    filepath = os.path.join(correct_folder, correct_filename)
    if not os.path.exists(correct_folder):
        os.makedirs(correct_folder)
    with open(filepath, 'w') as file:
        file.write(response.text)
    return filepath

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