from datetime import datetime

from Bizon.room import Room


class Webinar:
    def __init__(self):
        self.id = ''
        self.title = ''
        self.date = ''
        self.url = ''
        self.is_online = False
        self.author = ''
        self.files = {}
        self.music = []

    def create(self, room: Room):
        self.id = room.id
        self.title = room.title
        self.date = datetime.strptime(room.date, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%H:%M %m.%d.%y')
        self.url = room.hangoutsUrl
        self.author = room.author
        self.files = room.files
        self.music = room.music

    def create_from_db(self, web):
        self.id = web['id']
        self.title = web['title']
        self.date = web['date']
        self.url = web['url']
        self.author = web['author']
        self.files = web['files']
        self.music = web['music']

    def get_json(self):
        res = {
            'id': self.id,
            'title': self.title,
            'date': self.date,
            'url': self.url,
            'author': self.author,
            'files': self.files,
            'music': self.music,
        }
        return res
