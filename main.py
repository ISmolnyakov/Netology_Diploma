from bot_functions import *
from database import *

bot = VKBot()
creating_database()

for event in bot.longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        text = event.text.lower()
        user_id = event.user_id
        if text == 'команды':
            bot.write_msg(user_id, 'Команды для бота:\n'
                                   'Команды - вывести список команд бота\n'
                                   'Привет - поприветствовать бота\n'
                                   'Начать - начать поиск пользователя\n'
                                   'Далее - продолжить поиск\n'
                                   'Стоп - остановить бота')
        elif text == 'привет':
            bot.write_msg(user_id, f'Привет, {bot.name(user_id)}')
        elif text == 'начать':
            bot.write_msg(user_id, f'{bot.name(user_id)}, давай найдём тебе пару')
            bot.collect_users_to_db(user_id)
            bot.write_msg(event.user_id, f'Нашёл для тебя пару')
            bot.select_and_send_top_photo(user_id)
            bot.write_msg(event.user_id, f'Введите "далее" для продолжения поиска')
        elif text == 'далее':
            bot.write_msg(event.user_id, f'Ищу следующую пару')
            bot.write_msg(event.user_id, f'Нашёл ещё человека')
            bot.select_and_send_top_photo(user_id)
            bot.write_msg(event.user_id, f'Введите "далее" для продолжения поиска')
        elif text == 'стоп':
            bot.write_msg(user_id, 'Завершаю работу')
            break
        else:
            bot.write_msg(user_id, 'Я тебя не понимаю')
            bot.write_msg(user_id, 'Вот что умеет данный бот:\n'
                                   'Команды - вывести список команд бота\n'
                                   'Привет - поприветствовать бота\n'
                                   'Начать - начать поиск пользователя\n'
                                   'Стоп - остановить бота')
