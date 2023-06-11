from const_variables import *
import logging
from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
    MessageHandler,
    Filters,
)
from datetime import datetime
from Bizon import bizon

from database import UsersDB

logger = logging.getLogger('main')
logger.setLevel(GLOBAL_LOGGER_LEVEL)

users = UsersDB()


def send_start_msg(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    logger.info(f'Новое сообщение: /start или /help. пользователь:{user_id}')

    users.add_user(user_id)

    update.message.reply_text('Извлекатель ссылкок с сервиса bizon365\n'
                              'Техподдержка: телеграм t.me/dragon_np почта: dragonnp@yandex.ru',
                              disable_web_page_preview=True)


def extract(update: Update, _: CallbackContext):
    url = update.message.text
    room = bizon.Bizon().get_room(url)

    text = f'''
{room.title}\n
Дата начала: {datetime.strptime(room.date, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%H:%M %m.%d.%y')}
В эфире: {'да' if room.is_online else 'нет'}
Cсылка: {room.hangoutsUrl}
'''

    update.message.reply_text(text, disable_web_page_preview=True)


def error_callback(update: Update, context: CallbackContext):
    error: Exception = context.error

    logger.error(error)
    update.message.reply_text(
        'Произошла ошибка, возможно вебинар не найден. Пожалуйста, свяжитесь со мной через телеграм t.me/dragon_np или через почту dragonnp@yandex.ru')


def main() -> None:
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Create the Updater and pass it your bot token.
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', send_start_msg))
    dispatcher.add_handler(CommandHandler('help', send_start_msg))
    dispatcher.add_handler(MessageHandler(Filters.text, extract))
    dispatcher.add_error_handler(error_callback)

    # Start the Bot
    updater.start_polling()

    logger.info('Бот работает')
    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
