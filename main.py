import requests
import os
from dotenv import load_dotenv
from requests.exceptions import HTTPError

load_dotenv()
VK_TOKEN = os.getenv('VK_TOKEN')
GROUP_ID = os.getenv('GROUP_ID')


# Upload FLOW:
# 1. get_wall_upload_server ==> upload_url
# 2. upload_photo ==> json: server, photo, hash
# 3. save_wall_photo

def validate_vk_response(vk_data):
    error_info = vk_data.get('error')
    if error_info:
        # print(error_info['error_code'])
        # raise HTTPError(error_info['error_code'])
        raise HTTPError(f"Error code: {error_info['error_code']}. {error_info['error_msg']}")


def call_vk_method(access_token, method_name, params=None, v=5.101):
    url = f'https://api.vk.com/method/{method_name}?v={v}&access_token={access_token}'
    response = requests.get(url, params=params)
    response.raise_for_status()
    vk_data = response.json()
    validate_vk_response(vk_data)
    return vk_data


def get_wall_upload_server(access_token, group_id):
    method_name = 'photos.getWallUploadServer'
    params = {'group_id': group_id}
    vk_data = call_vk_method(access_token, method_name, params)
    return vk_data['response']['upload_url']


def upload_photo(photo_path, url):
    with open(photo_path, 'rb') as file:
        print(file)
        # headers = {'content-type': 'multipart/form-data'}
        files = {
            'photo': file,
        }
        response = requests.post(url, files=files)
        response.raise_for_status()
        return response.json()


def save_wall_photo(access_token, params):
    method_name = 'photos.saveWallPhoto'
    vk_data = call_vk_method(access_token, method_name, params)
    return vk_data['response'][0]['id'], vk_data['response'][0]['owner_id']


def wallpost(access_token, photo_id, owner_id, group_id, message):
    method_name = 'wall.post'
    params = {
        'attachments': 'photo' + str(owner_id) + '_' + str(photo_id),
        'message': message,
        'owner_id': '-' + str(group_id),
        # 'from_group': 0,
    }
    call_vk_method(access_token, method_name, params)


def get_groups(access_token, params=None):
    """Implements groups.get method of VK API"""
    method_name = 'groups.get'
    vk_data = call_vk_method(access_token, method_name, params)
    return vk_data

def upload_image_to_group_wall(access_token, group_id, image_path, image_comment):
    """Upload image on the wall of the group.
    Image restrictions:
    * image formats: JPG, PNG, GIF;
    * max width + hight < 14000 px;
    * max aspect raitio: 1:20;
    * max image size: 50 MB.

    The flow is:
    1. Get the URI of the upload server (get_wall_upload_server)
    2. Upload image to the sever (upload photo)
    3. Save image after succesfull upload (save_wall_photo)
    4. Publish on the wall (wallpost)
    """
    logger.debug('Start uploading image {image_path} \
        to the group {group_id} wall')

    upload_uri = get_wall_upload_server(access_token, group_id)
    logger.debug(f'Upload uri: {upload_url}.\nStart uploading image')

    params = upload_photo('./images/hubble_1.jpg', upload_url)
    params['group_id'] = GROUP_ID
    logger.debug(f'Image uploaded. Start saving photo')

    photo_id, owner_id = save_wall_photo(VK_TOKEN, params)
    logger.debug(f'Image saved. Image id: {photo_id}, owner_id: {owner_id}. \
        Start posting image to the group wall')

    wallpost(access_token, photo_id, owner_id, group_id, image_comment)
    logger.debug('Image posted')


# https://oauth.vk.com/authorize?client_id=7019910&scope=photos,groups,wall,offline&response_type=token