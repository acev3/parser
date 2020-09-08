import requests


if __name__ == '__main__':
    url = 'http://tululu.org/txt.php?id=32168'
    response = requests.get(url)
    response.raise_for_status()
    filename = 'books/id32168.txt'
    with open(filename, 'w') as file:
        file.write(response.text)