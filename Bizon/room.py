import json

class Room:
    def __init__(self, data):
        if len(data) == 0:
            data = {}
        else:
            data = json.loads(data)[1]['room']

        if 'title' in data:
            self.title = data['title']
        else:
            self.title = ''

        if 'date' in data:
            self.date = data['date']
        else:
            self.date = ''

        if 'hangoutsUrl' in data:
            self.hangoutsUrl = data['hangoutsUrl']
        else:
            self.hangoutsUrl = ''

        if 'online' in data:
            self.is_online = data['online']
        else:
            self.is_online = False