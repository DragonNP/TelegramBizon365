from const_variables import *
import logging
import telegram
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
    MessageHandler,
    Filters, CallbackQueryHandler,
)
from Bizon.webinar import Webinar
from Bizon import bizon

from database.users import UsersDB
from database.webinars import Webinars

logger = logging.getLogger('main')
logger.setLevel(GLOBAL_LOGGER_LEVEL)

users = UsersDB()
webinars = Webinars()


def reformat_webinar(webinar: Webinar, prime=False, user_id: str = ''):
    text = f'*{webinar.title}*\n\n'
    if prime:
        text += f'''*Автор:* {webinar.author}
*Дата начала:* {webinar.date}
*Cсылка:* {webinar.url}'''
    else:
        text += 'Доступ к полной информации о вебинаре вы можете купить у техподдержки:' \
                f' телеграм t.me/dragon\_np или почта dragonnp@yandex.ru, не забудьте указать данный код: {user_id}'
    return text


def get_keyboard_my_webinars():
    keyboard = [['Добавленные вебинары']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    return reply_markup


def get_keyboard_webinar(id, prime=False, files=True, music=True):
    keyboard = []
    if prime:
        if files:
            keyboard.append([InlineKeyboardButton('Показать файлы', callback_data='show_files_' + id)])
        if music:
            keyboard.append([InlineKeyboardButton('Показать музыку', callback_data='show_music_' + id)])

    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


def send_start_msg(update: Update, _: CallbackContext) -> None:
    user_id = update.message.from_user.id

    logger.info(f'Новое сообщение: /start или /help. пользователь:{user_id}')

    users.add_user(user_id)

    update.message.reply_text(
        'Извлекатель ссылкок с сервиса bizon365.\nВ бесплатной версии бота вы можете только посмотреть основную информацию о вебинаре, в полной версии вы получаете полный доступ к боту. Техподдержка: телеграм t.me/dragon_np почта: dragonnp@yandex.ru',
        disable_web_page_preview=True,
        reply_markup=get_keyboard_my_webinars())


def extract(update: Update, _: CallbackContext):
    user_id = update.message.from_user.id
    url = update.message.text

    url_id = str(url.split('/')[4])
    if len(url.split('/')) > 5:
        url_number = str(url.split('/')[5]).split('?')[0]
    else:
        url_number = ''
    webinar_id = url_id + ':' + url_number

    logger.info(f'Извлечение данных вебирана. пользователь:{user_id}')

    if not webinars.check(webinar_id):
        webinar: Webinar = bizon.Bizon().get_webinar(url)
        webinars.add_webinar(webinar)
    else:
        webinar: Webinar = webinars.get(webinar_id)

    prime = users.check_prime(user_id)

    text = reformat_webinar(webinar, prime, user_id=user_id)
    users.add_webinar(user_id, webinar.id)
    update.message.reply_text(text,
                              parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True,
                              reply_markup=get_keyboard_webinar(webinar_id, prime=prime))


def send_my_webs(update: Update, _: CallbackContext):
    user_id = update.message.from_user.id

    logger.info(f'Отправка всех добавленных вебинаров. пользователь:{user_id}')
    prime = users.check_prime(user_id)

    webs_id = users.get_webinars_id(user_id)

    if len(webs_id) == 0:
        update.message.reply_text('У вас еще нет добавленных вебинаров. Отправте ссылку, чтобы добавить вебинар.',
                                  parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True,
                                  reply_markup=get_keyboard_my_webinars())

    for id in webs_id:
        webinar = webinars.get(id)
        text = reformat_webinar(webinar, prime, user_id=user_id)
        update.message.reply_text(text,
                                  parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True,
                                  reply_markup=get_keyboard_webinar(id, prime))


def show_files(update: Update, _: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    original_text = query.message.text
    user_id = query.from_user.id

    add_music_btn = True
    if 'Музыка' in original_text:
        add_music_btn = False

    logger.debug(f'Отправка файлов вебинара. пользователь:{user_id}')

    webinar = webinars.get(query.data.replace('show_files_', ''))

    text = reformat_webinar(webinar, prime=True, user_id=user_id) + '\n\n'
    text += 'Файлы:\n'
    for name in webinar.files:
        text += f'   - [{name}]({webinar.files[name]})\n'

    if not add_music_btn:
        text += '\n'
        text += 'Музыка:\n'
        music = webinar.music
        for url in music:
            text += f'   - {url}\n'

    query.edit_message_text(text=text,
                            parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True,
                            reply_markup=get_keyboard_webinar(webinar.id, prime=True, files=False,
                                                              music=add_music_btn))


def show_music(update: Update, _: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    original_text = query.message.text
    user_id = query.from_user.id

    add_files_btn = True
    if 'Файлы' in original_text:
        add_files_btn = False

    logger.debug(f'Отправка музыки вебинара. пользователь:{user_id}')

    webinar = webinars.get(query.data.replace('show_music_', ''))

    text = reformat_webinar(webinar, prime=True, user_id=user_id) + '\n\n'
    if not add_files_btn:
        text += 'Файлы:\n'
        for name in webinar.files:
            text += f'   - [{name}]({webinar.files[name]})\n'
        text += '\n'

    text += 'Музыка:\n'
    for url in webinar.music:
        text += f'   - {url}\n'

    query.edit_message_text(text=text,
                            parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True,
                            reply_markup=get_keyboard_webinar(webinar.id, prime=True, files=add_files_btn,
                                                              music=False))


def route_callback(update: Update, context: CallbackContext):
    query = update.callback_query

    if 'show_files' in query.data:
        return show_files(update, context)
    elif 'show_music' in query.data:
        return show_music(update, context)


def add_prime(update: Update, context: CallbackContext):
    user_id = ''.join(context.args)

    res = users.set_prime(int(user_id))

    if res:
        return update.message.reply_text('Успешно! Теперь пользователь имеет полный доступ к боту',
                                         parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True,
                                         reply_markup=get_keyboard_my_webinars())

    return update.message.reply_text('Произошла непредвиденная ошибка',
                                     parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True,
                                     reply_markup=get_keyboard_my_webinars())


def error_callback(update: Update, context: CallbackContext):
    error: Exception = context.error

    logger.error(error)
    update.message.reply_text(
        'Произошла ошибка, возможно вебинар не найден.\n'
        'Пожалуйста, свяжитесь со мной через телеграм t.me/dragon\_np или через почту dragonnp@yandex.ru',
        parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True,
        reply_markup=get_keyboard_my_webinars())


def main() -> None:
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Create the Updater and pass it your bot token.
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', send_start_msg))
    dispatcher.add_handler(CommandHandler('help', send_start_msg))
    dispatcher.add_handler(CommandHandler('add_prime', add_prime))
    dispatcher.add_handler(MessageHandler(Filters.text('Добавленные вебинары'), send_my_webs))
    # dispatcher.add_handler(MessageHandler(Filters.text('Купить полный доступ'), buy_full_access))
    dispatcher.add_handler(MessageHandler(Filters.text, extract))
    dispatcher.add_handler(CallbackQueryHandler(route_callback))
    dispatcher.add_error_handler(error_callback)

    # Start the Bot
    updater.start_polling()

    logger.info('Бот работает')
    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
