import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

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
        img_src = soup.find('div', class_='bookimage').find('img')['src']
        comments = soup.find_all('div', class_="texts")
        genres = soup.find('span', class_='d_book').find_all('a')
        genres_list = []
        print(title_name)
        for genre in genres:
            genres_list.append(genre.text)
        #print(title_name)
        title_name = title_name.split("/")[-1]
        #print(urljoin(url, img_src))
        img_src_1 = urljoin(url,img_src)
        #print(comments)
    except Exception as e:
        return None
    return str(id_book) + ". " + title_name , img_src_1, comments, genres_list