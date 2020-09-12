import requests
from file import download_txt
from tululu import title_parser


if __name__ == '__main__':
    url_base = 'http://tululu.org/b%s'
    for i in range(1,11):
        try:
            url = url_base % i
            response = requests.get(url)
            response.raise_for_status()
            filename = title_parser(url , i)
            if filename:
                download_txt(url, filename)
        except Exception as e:
            print(e)