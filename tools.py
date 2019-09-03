import os
from os import walk
import requests
import logging


logger = logging.getLogger(__name__)


# def fetch_image(url, verify=True):
#     response = requests.get(url, verify=verify)
#     response.raise_for_status()
#     extension = check_url_is_image(response.url)
#     return response.content, extension


def check_url_is_image(url, extensions=['jpg', 'jpeg', 'png', 'bmp', 'tif', 'svg']):
    extension = url.split('.')[-1]
    if extension not in extensions:
        raise ValueError('Object is not an image')
    return extension


def save_image(content, file_path):
    with open(file_path, 'wb') as file:
        file.write(content)


def download_image(url, path='images', filename='image', verify=True):
    extension = check_url_is_image(url)
    response = requests.get(url, verify=verify)
    response.raise_for_status()

    os.makedirs(path, exist_ok=True)
    filename = filename + '.' + extension
    file_path = os.path.join(path, filename)
    save_image(response.content, file_path)


def scan_for_files_in_folder(foldername, recursion=False):
    files = []
    for (dirpath, dirnames, filenames) in walk(foldername):
        for filename in filenames:
            files.append(os.path.join(dirpath, filename))
    return files

if __name__ == '__main__':
    download_image('https://imgs.xkcd.com/comics/earth_temperature_timeline.png')
