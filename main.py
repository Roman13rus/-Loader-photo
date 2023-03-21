import requests
import json
from Loader_photo_VK import LoaderPhotoVK
from Load_photo_YD import LoaderYD
import logging
import time
from progress.bar import IncrementalBar


my_logger = logging.getLogger(__name__)
my_logger.setLevel(logging.INFO)
my_handler = logging.FileHandler(f"{__name__}.log", mode='w')
my_formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

my_handler.setFormatter(my_formatter)
my_logger.addHandler(my_handler)

if __name__ == '__main__':
    try:
        with open('token.txt', 'r') as file_object:
            token = file_object.read().strip()
        id_users = input('Введите id пользователя Вконтакте: ')
        vk = LoaderPhotoVK(token, id_users,'5.131')
        token_YD = input('Введитие ваш токен Яндекс Диска: ')
        yd = LoaderYD(token_YD)
        result = []
        mylist_photo = vk.photo_filter()
        bar = IncrementalBar('Countdown', max = len(mylist_photo))
        for photo in mylist_photo:
            name_file = photo['name']
            photo_url = photo["url"]
            yd.upload_file_to_disk(yd._put_upload_field('My_Photo_VK'), name_file, photo_url)
            photo_result = {"file_name":f"{photo['name']}.jpg",
                            "size":photo["size"]}
            result.append(photo_result)
            bar.next()
            time.sleep(1)
        bar.finish()
        with open('result.json', 'w') as f:
            json.dump(result, f, ensure_ascii = False, indent=2)
        my_logger.info(f"Successful result: load {len(result)} photo.")
    except KeyError as err:
        my_logger.error("(KeyError) The VK user ID was entered incorrectly", exc_info=True)
    except HTTPError as err:
        my_logger.error("(HTTPError) An incorrect Yandex Disk token has been entered", exc_info=True)

