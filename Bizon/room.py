import json


class Room:
    def __init__(self, data):
        if len(data) == 0:
            data = {}
        else:
            data = json.loads(data)[1]['room']

        if 'name' in data:
            self.id = data['name']
        else:
            self.id = ''

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

        if 'author' in data:
            self.author = data['author']
        else:
            self.author = ''

        if 'files' in data:
            self.files = {}
            for file in json.loads(data['files']):
                self.files[file['title']] = file['url']
        else:
            self.author = {}

        if 'music' in data:
            self.music = []
            for curr_music in json.loads(data['music']):
                self.music.append(curr_music['url'])
        else:
            self.author = []
