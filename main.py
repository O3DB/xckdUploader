import os
import time
import logging

from requests.exceptions import HTTPError

from vk import upload_image_to_group_wall
from xkcd import download_random_comic
from log import setup_logging
from config import CONFIG

logger = logging.getLogger(__name__)


def main():
    setup_logging()
    while True:
        logger.info('Start app')
        try:
            comic_info, filename = download_random_comic()
            logger.info(f'Downloaded comic: {filename}')

            upload_image_to_group_wall(
                access_token=CONFIG['VK_TOKEN'],
                group_id=CONFIG['GROUP_ID'],
                image_path=filename,
                image_comment=comic_info['alt']
                )
            logger.info('Comic uploaded to the group wall')

            os.remove(filename)
            logger.info('Image removed')
        except HTTPError:
            logger.warning('HTTP Error!')
        time.sleep(24 * 3600) #1 day sleep


if __name__ == '__main__':
    main()
