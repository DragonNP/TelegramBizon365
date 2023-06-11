import json
from const_variables import *
from Bizon.webinar import Webinar


class Webinars:
    logger = logging.getLogger('webinars_db')

    def __init__(self):
        self.db = {}
        self.logger.setLevel(GLOBAL_LOGGER_LEVEL)
        self.logger.debug('Инициализация базы данных пользователей')

        self.location = os.path.expanduser(PATH_TO_WEBINARS_DATA_BASE)
        self.load(self.location)

    def load(self, location):
        self.logger.debug('Загрузка базы данных')

        if os.path.exists(location):
            self.__load()
        return True

    def __load(self):
        self.logger.debug('Загрузка базы данных из файлв')
        self.db = json.load(open(self.location, 'r'))

    def __dump_db(self):

        self.logger.debug('Сохранение базы данных в файл')
        try:
            json.dump(self.db, open(self.location, 'w+'))
            return True
        except Exception as e:
            self.logger.error(e)
            return False

    def check(self, webinar_id: str):
        self.logger.debug(f'Проверка вебинара')

        try:
            if webinar_id not in self.db:
                return False
            return True
        except Exception as e:
            self.logger.error(f'Не удалось проверить вебинар', e)
            return False

    def get(self, webinar_id: str):
        self.logger.debug(f'Запрос на получения вебинара')

        try:
            if not self.check(webinar_id):
                self.logger.debug('Вебинар не найден')
                return Webinar()
            webinar = Webinar()
            webinar.create_from_db(self.db[webinar_id])
            return webinar
        except Exception as e:
            self.logger.error(f'Не удалось проверить вебинар', e)
            return False

    def add_webinar(self, webinar: Webinar):
        self.logger.debug(f'Добавление вебинара')

        try:
            if webinar.id in self.db:
                self.logger.debug(f'Вебинар уже добавлен')
                return False

            self.db[webinar.id] = webinar.get_json()
            self.__dump_db()
            return True
        except Exception as e:
            self.logger.error(f'Не удалось добавить вебинар', e)
            return False