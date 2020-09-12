import requests
from bs4 import BeautifulSoup

def title_parser(url , id_book):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    try:
        title_tag = soup.find('div', id='content').find('h1')
        title = title_tag.text.split("::")
        title_name = title[0].strip("  ")
        title_name = title_name.replace(u'\xa0', u' ')
        title_name = title_name.strip(" ")
    except Exception as e:
        return None
    return str(id_book) + ". " + title_name