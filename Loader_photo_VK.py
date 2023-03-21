import json
import time
import requests
import logging

my_logger = logging.getLogger(__name__)
my_logger.setLevel(logging.INFO)
my_handler = logging.FileHandler(f"{__name__}.log", mode='w')
my_formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

my_handler.setFormatter(my_formatter)
my_logger.addHandler(my_handler)

class LoaderPhotoVK: #класс загрузчика списка фотографий из api VK
    url = 'https://api.vk.com/method/'
    def __init__(self, token, id_users, version):
        self.token = token
        self.id_users = id_users
        self.version = version
    
    def loader_photo_vk(self): #  метод получения списка фотографий из профиля
        photo_loader_url = self.url + 'photos.get'
        params = {
            'access_token':self.token,
            'v': self.version,
            'owner_id':self.id_users,
            'album_id':'profile',
            'rev':True,
            'extended':True,
            'photo_sizes':True,
            'count':5
        }
        response = requests.get(photo_loader_url, params=params)
        req = response.json()
        my_logger.info(f"Received a list of VK photos for module {__name__}")
        return req

    def photo_filter(self): #метод выборки необходимых фотографий из общего списка и получение списка ссылок для загрузки
        self.photos_list = []
        for data in self.loader_photo_vk()["response"]["items"]:
             self.photo_dict = {}
             self.photo_dict["date"] = data["date"]
             self.photo_dict["likes"] = data["likes"]["user_likes"]
             self.photo_dict["url"] = data["sizes"][-1]["url"]
             self.photo_dict["size"] = data["sizes"][-1]["type"]
             self.photo_dict["name"] = self.photo_dict["likes"]
             for dict in self.photos_list:
                 if self.photo_dict["likes"] != dict["likes"]:
                     self.photo_dict["name"] = self.photo_dict["likes"]
                 else:
                     self.photo_dict["name"] = self.photo_dict["date"]
             self.photos_list.append(self.photo_dict)
        my_logger.info(f"The list of photos has been processed for module {__name__}")
        return self.photos_list




