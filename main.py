import requests
from file import download_txt, download_image, save_text
from tululu import title_parser


if __name__ == '__main__':
    url_base = 'http://tululu.org/b%s'
    for i in range(1,11):
        try:
            url = url_base % i
            response = requests.get(url)
            response.raise_for_status()
            filename, img_src, comments, genres = title_parser(url , i)
            #if filename:
                #download_txt(url, filename)
            #if img_src:
                #download_image(img_src)
            #if comments:
                #save_text(filename, comments)
            if genres:
                print(genres)
        except Exception as e:
            print(e)