import requests
import json
from Bizon.initData import InitData
from Bizon.room import Room


class Bizon:
    def get_room(self, url):
        url = url.split('?')[0]

        sid = self.get_sid(url)

        init_data: InitData = self.load_init_data(url, sid)
        sid_special = self.get_sid_for_link(sid, init_data)
        room: Room = self.get_ws5_bizon(init_data, sid_special)

        return room

    def get_sid(self, url):
        if url[len(url) - 1] != '/':
            url += '/'

        url_authorize = url + "authorize?_csrf="
        body = {"username": "test",
                "email": "dsf@ya.ru",
                "phone": "+71234567890",
                "custom1": "test",
                "referer": "test",
                "param1": "test",
                "param2": "test",
                "param3": "test",
                "cu1": "test",
                "sup": "test"}

        x = requests.post(url_authorize, data=body, headers={'host': 'start.bizon365.ru'})

        if x.text != '{}':
            print('get_sid, error!!')

        for key in x.cookies.keys():
            if key == 'sid':
                return x.cookies[key]

    def load_init_data(self, url, sid, ):
        url_load_init_data = url + "/loadInitData"

        x = requests.post(url_load_init_data, data={'ssid': sid},
                          headers={'host': 'start.bizon365.ru', 'cookie': f'sid={sid}'})
        return InitData(x.text)

    def get_sid_for_link(self, sid, init_data: InitData):
        url = f'''https://ws5.bizon365.ru/socket.io/?ssid={init_data.ssid}&ssign={init_data.ssign}&roomid={init_data.room_id}&group={init_data.group_id}&transport=polling'''

        x = requests.get(url, headers={'host': 'ws5.bizon365.ru'})
        result = x.text

        i = 0
        while result[i] != '{':
            i += 1

        if 'sid' in json.loads(result[i:]):
            return json.loads(result[i:])['sid']
        print('get_sid_for_link, ошибка')

    def get_ws5_bizon(self, init_data: InitData, sid):
        url = f"https://ws5.bizon365.ru/socket.io/?ssid={init_data.ssid}&ssign={init_data.ssign}&roomid={init_data.room_id}&group={init_data.group_id}&sid={sid}&transport=polling"
        x = requests.get(url, headers={'host': 'ws5.bizon365.ru'})

        result = x.text
        i = 0
        while result[i] != '[':
            i += 1
            if i >= len(result):
                break
        result = result[i:]
        return Room(result)
