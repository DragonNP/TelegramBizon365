import json


class InitData:
    def __init__(self, data):
        data = json.loads(data)
        if 'roomid' in data:
            self.room_id = data['roomid']
        else:
            self.room_id = ''

        if 'ssid' in data:
            self.ssid = data['ssid']
        else:
            self.ssid = ''

        if 'ssign' in data:
            self.ssign = data['ssign']
        else:
            self.ssign = ''

        if 'groupid' in data:
            self.group_id = data['groupid']
        else:
            self.group_id = ''
