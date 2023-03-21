import requests
import logging

my_logger = logging.getLogger(__name__)
my_logger.setLevel(logging.INFO)
my_handler = logging.FileHandler(f"{__name__}.log", mode='w')
my_formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

my_handler.setFormatter(my_formatter)
my_logger.addHandler(my_handler)

class LoaderYD:
    def __init__(self, token_YD):
        self.token_YD = token_YD
    
    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token_YD)
        }
    
    def _put_upload_field(self, name_field):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources"
        headers = self.get_headers()
        params = {"path": name_field, "fields":name_field}
        response = requests.put(upload_url, headers=headers, params=params)
        return name_field

    def upload_file_to_disk(self, name_field, name_file, photo_url):
        url_load = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        params  = {'url':photo_url,
            'path':f"/{self._put_upload_field(name_field)}/{name_file}.jpg"
            }
        my_logger.info(f"A new folder {name_field} on Yandex. Disk has been created for module {__name__}")
        response = requests.post(url_load, params=params, headers=headers )
        response.raise_for_status()
        if response.status_code == 202:
            my_logger.info(f"A new photo load in folder {name_field} on Yandex. Disk ")]
        

