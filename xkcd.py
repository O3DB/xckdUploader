import random
import requests

from tools import download_image


def get_last_comic_num():
    url = 'http://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()['num']


#TODO: хранить информацию о загруженных комиксах и исключать при генерации номера
#TODO: не сохраняя комикс загружать в ВК
def generate_comic_num():
    max_num = get_last_comic_num()
    return random.randint(1, max_num)


def get_comic_info(comic_num):
    url = f"http://xkcd.com/{comic_num}/info.0.json"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def download_random_comic():
    url = 'http://xkcd.com/'
    comic_num = generate_comic_num()

    comic_info = get_comic_info(comic_num)
    img_url = comic_info['img']
    filename = img_url.split('/')[-1]

    download_image(url=img_url, filename=filename, path='./')
    return comic_info, filename
