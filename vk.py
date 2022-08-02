import requests


class VkSearch:
    method_base_url = 'https://api.vk.com/method/'

    def __init__(self, user_id, access_token):
        self.user_id = user_id
        self.params = {
            'access_token': access_token,
            'v': '5.131'
        }

    def get_user_data(self):
        url = self.method_base_url + 'users.get'
        search_params = {
            'user_ids': self.user_id,
            'fields': 'city,country,bdate,sex',
            **self.params
        }
        res = requests.get(url, params=search_params)
        data = res.json()['response']
        return data

    def search_matches(self, search_data, offset=0):
        url = self.method_base_url + 'users.search'
        search_params = {
            'city': search_data['city'],
            'country': search_data['country'],
            'age_from': search_data['age_from'],
            'age_to': search_data['age_to'],
            'sex': search_data['sex'],
            'count': 1000,
            'has_photo': 1,
            'sort': 1,
            'offset': offset,
            **self.params
        }
        res = requests.get(url, params=search_params).json()
        return res['response']['items']

    def get_matched_user_photos(self, matched_user_id):
        url = self.method_base_url + 'photos.get'
        params = {
            'owner_id': matched_user_id,
            'album_id': 'profile',
            'extended': 1,
            'count': 10,
            **self.params
        }
        res = requests.get(url, params=params).json()
        photos = sorted(res['response']['items'], key=lambda x: x['likes']['count'], reverse=True)
        photos_to_show = []
        for item in photos[:3]:
            photos_to_show.append(item['sizes'][-1]['url'])
        return photos_to_show
