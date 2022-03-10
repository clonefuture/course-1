
import requests


def get_photo_inst(id_, photo_cnt=5):
    url = f"https://graph.instagram.com/{id_}/media"
    token = 'IGQVJWcEc0NkpVa2dEMmxabjRiY3IzUktsZAEFSQlpmMFZAoa1FRQkphVER6VmRNTHlGU1ZAzNkFycXdPNWFQOVBIa2ltNUxEdUxpdk5' \
            'MZAXI3SlR5LTBqQ1VPRDZANZAkVPdGtwSVRkSUNFTkx0eU5aejMzWAZDZD'
    headers = {'Authorization': 'OAuth {}'.format(token)}
    params = {'fields': 'media_url, timestamp'}
    response = requests.get(url, headers=headers, params=params)
    res_list = response.json()['data']
    pic_list = []
    for cn, pic in enumerate(res_list, 1):
        res_dict = {
            'file_name': pic['id'] + '.jpg',
            'url': pic['media_url']
        }
        pic_list.append(res_dict)
        if cn == photo_cnt:
            break
    return pic_list


