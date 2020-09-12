import requests


if __name__ == '__main__':
    url_base = 'http://tululu.org/txt.php?id=%s'
    for i in range(1,11):
        try:
            url = url_base % i
            response = requests.get(url)
            response.raise_for_status()
            if not response.history:
                filename = 'books/id%s.txt' % i
                with open(filename, 'w') as file:
                    file.write(response.text)
        except Exception as e:
            print(e)