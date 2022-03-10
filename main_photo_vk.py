import json
import requests
from pprint import pprint
from datetime import datetime
import time
from tqdm import tqdm
from ok import get_photo_ok
from insta import get_photo_inst


def convert_date(date):
    return datetime.fromtimestamp(date).strftime('%Y%m%d')


def save_json():
    photo_f = PhotoFromVK(token, version).get_photo(id_, album_id, photo_cnt)
    res_lst = []
    for i in photo_f:
        res_dict = {
            'file_name': str(i['file_name'])+'.jpg',
            'size': i['size']
        }
        res_lst.append(res_dict)
    with open('savefiles.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(res_lst, sort_keys=True, indent=4))


class PhotoFromVK:
    def __init__(self, token, version):
        self.params = {
            'access_token': token,
            'v': version
        }

    def get_photo(self, id_, album_id, photo_cnt=5):
        photo_list = []
        url = 'https://api.vk.com/method/photos.get'
        params = {
            'owner_id': id_,
            'count': photo_cnt,
            'album_id': album_id,
            'extended': 1
        }
        res = requests.get(url, params={**self.params, **params})
        list_items = res.json()['response']['items']
        for item in list_items:
            photo_dict = {
                'file_name': item['likes']['count'],
                'url': item['sizes'][-1]['url'],
                'size': item['sizes'][-1]['type'],
                'date': convert_date(item['date'])
            }
            photo_list.append(photo_dict)

        temp_name = []
        for dicts in photo_list:
            if dicts['file_name'] in temp_name:
                dicts['file_name'] = f"{dicts['file_name']}_{dicts['date']}"
            temp_name.append(dicts['file_name'])

        return photo_list


class ToYaDisk:
    def __init__(self, token_ya):
        self.token_ya = token_ya

    def upload(self, path_files):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'

        '''Загрузка файлов из VK'''

        if name == 'v':
            f = PhotoFromVK(token, version).get_photo(id_, album_id, photo_cnt)
            for urls in tqdm(f):
                time.sleep(1)
                url = urls['url']
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'OAuth {}'.format(self.token_ya)
                }
                params = {'path': path_files+str(urls['file_name']), 'url': url}
                response = requests.post(upload_url, headers=headers, params=params)
            save_json()

            '''Загрузка файлов из Одноклассники'''

        elif name == 'o':
            f = get_photo_ok(id_, photo_cnt)
            for urls in tqdm(f):
                time.sleep(1)
                url = urls['url']
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'OAuth {}'.format(self.token_ya)
                }
                params = {'path': path_files+str(urls['file_name']), 'url': url}
                response = requests.post(upload_url, headers=headers, params=params)

                '''Загрузка файлов из Instagram'''

        elif name == 'i':
            f = get_photo_inst(id_, photo_cnt)
            for urls in tqdm(f):
                time.sleep(1)
                url = urls['url']
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'OAuth {}'.format(self.token_ya)
                }
                params = {'path': path_files+str(urls['file_name']), 'url': url}
                response = requests.post(upload_url, headers=headers, params=params)


if __name__ == '__main__':
    name = input('''Резервное копирование из соц.сетей:
    v - В контакте
    o - Одноклассники
    i - Instagram
                 
Введите название соц.сети (v, o, i) - ''')
    if name == 'v':
        album_id = input('Укажите альбом из которого будут сохраняться фото (wall, profile) - ')
    id_ = input('Введите Id пользователя - ')
    token_ya = input('Введите token с Полигона Яндекс.Диска - ')
    photo_cnt = int(input('Введите количество фотографий для сохранения - '))
    token = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
    version = 5.131
    path_files = '/Netology/'
    ToYaDisk(token_ya).upload(path_files)

