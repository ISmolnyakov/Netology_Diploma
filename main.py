from bot_functions import *
# from bot_functions2 import *
from database import creating_database

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
            min_age = bot.minimum_age(user_id)
            max_age = bot.maximum_age(user_id)
            bot.search(user_id, min_age, max_age)
            bot.write_msg(event.user_id, f'Введите "далее" для продолжения поиска')
        elif text == 'далее':
            bot.write_msg(event.user_id, f'Ищу следующую пару')
            bot.search(user_id, min_age, max_age)
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
