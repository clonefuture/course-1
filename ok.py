import requests
import json
from pprint import pprint
import hashlib


# photo_cnt = 5
# id_ = '80970210435'

def get_photo_ok(id_, photo_cnt=5):
    mystring = f"application_key=CHLDBDKGDIHBABABAcount={photo_cnt}fid={id_}format=jsonmethod=photos.getPhotos66df98387b0dd7bd735ce201c585d28d"
    hash_object = hashlib.md5(mystring.encode())
    sig = hash_object.hexdigest()
    get_lst = []
    url_ = 'https://api.ok.ru/fb.do'
    params = dict(
        application_key='CHLDBDKGDIHBABABA',
        format='json', method='photos.getPhotos',
        fid=id_,
        sig=sig,
        access_token='tkn1c5qvr8NLFaynpkInomuGgF9UujuYSNuUb94lPqTtuSS9QuRnuxuI4fP5Jt6ecogODb',
        count=photo_cnt
    )
    res = requests.get(url_, params=params)
    lst_pic = res.json()['photos']
    for pic in lst_pic:
        get_dict = {
            'file_name': pic['id'] + '.jpg',
            'url': pic['pic640x480']
        }
        get_lst.append(get_dict)
    return get_lst



