import json
from const_variables import *


class UsersDB:
    logger = logging.getLogger('user_db')

    def __init__(self):
        self.db = {}
        self.logger.setLevel(GLOBAL_LOGGER_LEVEL)
        self.logger.debug('Инициализация базы данных пользователей')

        self.location = os.path.expanduser(PATH_TO_USERS_DATA_BASE)
        self.load(self.location)

    def load(self, location):
        self.logger.debug('Загрузка базы данных')

        if os.path.exists(location):
            self.__load()
        return True

    def __load(self):
        self.logger.debug('Загрузка базы данных из файлв')
        self.db = json.load(open(self.location, 'r'))

    def __check_user(self, user_id: int):
        res = str(user_id) in self.db.keys()
        self.logger.debug(f'Проверка пользователе в базе данных. результат:{res}')
        return res

    def __dump_db(self):

        self.logger.debug('Сохранение базы данных в файл')
        try:
            json.dump(self.db, open(self.location, 'w+'))
            return True
        except Exception as e:
            self.logger.error(e)
            return False

    def add_user(self, user_id):
        self.logger.debug(f'Создание пользователя. id пользователя:{user_id}')

        try:
            if self.__check_user(user_id):
                self.logger.debug(f'Пользователь уже создан. id пользователя:{user_id}')
                return False

            self.db[str(user_id)] = [False, []]
            self.__dump_db()
            return True
        except Exception as e:
            self.logger.error(f'Не удалось сохранить пользователя. id пользователя:{user_id}', e)
            return False

    def check_prime(self, user_id: int):
        self.logger.debug(
            f'Запрос на проверку подписки на бота. id пользователя:{user_id}')

        try:
            if not self.__check_user(user_id):
                self.logger.debug(f'Пользователь не найден. id пользователя:{user_id}')
                self.add_user(user_id)

            return self.db[str(user_id)][0]
        except Exception as e:
            self.logger.error(
                f'Не удалось проверить подписку. id пользователя:{user_id}', e)
            return {}

    def set_prime(self, user_id: int):
        self.logger.debug(f'Добавление подписки. id пользователя:{user_id}')

        try:
            if not self.__check_user(user_id):
                self.logger.debug(f'Пользователь не найден. id пользователя:{user_id}')
                self.add_user(user_id)

            self.db[str(user_id)][0] = True
            self.__dump_db()
            return True
        except Exception as e:
            self.logger.error(f'Не удалось добавить подписку. id пользователя:{user_id}', e)
            return False

    def add_webinar(self, user_id: int, webinar_id: str):
        self.logger.debug(f'Добавление вебинара в пользователя. id пользователя:{user_id}')

        try:
            if not self.__check_user(user_id):
                self.logger.debug(f'Пользователь не найден. id пользователя:{user_id}')
                self.add_user(user_id)
            if webinar_id in self.db[str(user_id)][1]:
                self.logger.debug(f'Вебинар уже добавлен. id пользователя:{user_id}')
                return False

            self.db[str(user_id)][1].append(webinar_id)
            self.__dump_db()
            return True
        except Exception as e:
            self.logger.error(f'Не удалось добавить вебинар'
                              f'. id пользователя:{user_id}', e)
            return False

    def get_webinars_id(self, user_id: int):
        self.logger.debug(f'Получения вебинаров пользователя. id пользователя:{user_id}')

        try:
            if not self.__check_user(user_id):
                self.logger.debug(f'Пользователь не найден. id пользователя:{user_id}')
                self.add_user(user_id)

            return self.db[str(user_id)][1]
        except Exception as e:
            self.logger.error(f'Не удалось получить вебинары. id пользователя:{user_id}', e)
            return False
