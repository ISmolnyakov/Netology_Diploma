import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import requests
from random import randrange
from config import *
from pprint import pprint
from operator import itemgetter

vk_group = vk_api.VkApi(token=group_token)
vk_user = vk_api.VkApi(token=user_token)
longpoll = VkLongPoll(vk_group)
#
#
def write_msg(user_id, message):
    vk_group.method("messages.send", {'user_id': user_id,
                                      'message': message,
                                      'random_id': randrange(10 ** 7)})

def select_photo(vk_id):
    params = {'access_token': user_token,
              'v': '5.131',
              'owner_id': vk_id,
              'album_id': 'profile',
              'extended': 1
              }
    response = vk_user.method('photos.get', params)
    photo_info = {}
    for i in range(response['count']):
        photo_info[response['items'][i]['likes']['count']] = {'id': response['items'][i]['id'],
                                                              'likes': response['items'][i]['likes']['count'],
                                                              'url': response['items'][i]['sizes'][-1]['url']}
    top_three_photo = list(sorted(photo_info.items(), reverse=True)[:3:])
    return top_three_photo

def find_user(user_id):
    params = {'access_token': user_token,
              'v': '5.131',
              'sex': 1,
              'age_from': 35,
              'age_to': 45,
              'city': find_city(user_id),
              'fields': 'is_closed, id, first_name, last_name',
              'status': '1' or '6',
              'count': 10}
    req = vk_user.method("users.search", params)
    try:
        list_1 = req['items']
        for person_dict in list_1:
            if not person_dict.get('is_closed'):
                first_name = person_dict.get('first_name')
                last_name = person_dict.get('last_name')
                vk_id = str(person_dict.get('id'))
                vk_link = 'vk.com/id' + str(person_dict.get('id'))
                # add_user_info(first_name, last_name, vk_id, vk_link)
                send_photo(user_id)
            else:
                continue
    except KeyError:
        write_msg(user_id, 'Ошибка получения токена')

def find_city(user_id):
    """find user city id"""
    params = {'access_token': group_token,
              'v': '5.131',
              'user_ids': user_id,
              'fields': 'city'}
    response = vk_group.method("users.get", params)
    try:
        for town in response:
            if 'city' in town:
                city = town.get('city')
                id = str(city.get('id'))
                return id
            elif 'city' not in town:
                write_msg(user_id, 'Введите название вашего города: ')
                for event in longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                        city_name = event.text
                        id_city = find_city_id_by_name(user_id, city_name)
                        if id_city != '' or id_city is not None:
                            return str(id_city)
                        else:
                            break
    except KeyError:
        write_msg(user_id, 'Ошибка получения токена')
    return city

def find_city_id_by_name(user_id, city_name):
    """find city id if not in users data"""
    params = {'access_token': user_token,
              'country_id': 1,
              'q': f'{city_name}',
              'need_all': 0,
              'count': 1000,
              'v': '5.131'}
    repl = vk_group.method('database.getCities', params)
    try:
        information_list = repl['response']
        list_cities = information_list['items']
        for i in list_cities:
            found_city_name = i.get('title')
            if found_city_name == city_name:
                found_city_id = i.get('id')
                return int(found_city_id)
    except KeyError:
        write_msg(user_id, 'Ошибка получения токена')


def send_photo(user_id):
    for i in range(len(select_photo(vk_id=))):
        photo_id = select_photo(user_id)
        vk_group.method("messages.send", {'user_id': user_id,
                                          'random_id': randrange(10 ** 7),
                                          'attachment': f"photo{vk_id}_{photo_id[i][1]['id']}"
                                          })


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        text = event.text.lower()
        user_id = event.user_id
        if text == 'привет':
            write_msg(user_id, 'Добрый день')
        elif text == 'поиски':
            find_user(user_id)
        elif text == 'фото':
            send_photo(user_id)
        else:
            write_msg(user_id, 'Я тебя не понимаю')

