#Импорты
import json
import random
import requests
from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from googletrans import Translator
#Вспомогательные переменные + создание бота
bot = TeleBot(token='6640912353:AAE3CL9xHESDIEcIFedNtYcYU5wUMkgmxXg', parse_mode='html')
translator = Translator()
Act_API = 'http://www.boredapi.com/api/activity/'
png = ['100', '101', '102', '103', '200',
       '201', '202', '203', '204', '206',
       '207', '300', '301', '302', '303',
       '304', '305', '307', '308', '400',
       '401', '402', '403', '404', '405',
       '406', '407', '408', '409', '410',
       '411', '412', '413', '414', '415',
       '416', '417', '418', '420', '421',
       '422', '423', '424', '425', '426',
       '428', '429', '431', '444', '450',
       '451', '497', '498', '499', '500',
       '501', '502', '503', '504', '506',
       '507', '508', '509', '510', '511',
       '521', '522', '523', '525', '530', '599']

#Оброботчик команды старт
@bot.message_handler(commands=['start'])
def starting(message):

    keyboard = ReplyKeyboardMarkup(row_width=1)
    but1 = KeyboardButton(text='Главное меню')
    keyboard.add(but1)

    bot.send_message(message.chat.id,
                     f'Привет, {message.from_user.first_name},\n'
                     f'Я телеграм бот, чтобы начать работу, нажми на кнопку <b>"Главное меню"</b>\n'
                     f'Сначала рекомендую прочитать <b>"о боте"</b>',
                     reply_markup=keyboard)
    bot.register_next_step_handler(message, main_menu)

#Главное меню
def main_menu(message):

    if message.text == 'Главное меню':
        keyboard = ReplyKeyboardMarkup(row_width=2)
        but1 = KeyboardButton(text='О боте')
        but2 = KeyboardButton(text='Чем заняться, когда скучно?')
        but3 = KeyboardButton(text='Посмотреть на котика')
        but4 = KeyboardButton(text='Цитата Стейтема')
        but5 = KeyboardButton(text='Коктейль')
        but6 = KeyboardButton(text='Контакты')
        keyboard.add(but1, but2, but3, but4, but5, but6)

        bot.send_message(message.chat.id, text='Добро пожаловать в главное меню, выберете действие',
                     reply_markup=keyboard)
        bot.register_next_step_handler(message, main_menu_func)
    else:
        bot.send_message(message.chat.id, 'Что то пошло не так, нажмите на конпку <b>"Главное меню"</b>')

        bot.register_next_step_handler(message, main_menu)

#Обработчик кнопок
def main_menu_func(message):
    if message.text == 'Чем заняться, когда скучно?':

        res = requests.get(f'http://www.boredapi.com/api/activity/')
        data = json.loads(res.text)

        text = translator.translate(f'Action: {data["activity"]}\n'
                                    f'Type:{data["type"]}\n'
                                    f'Participants: {data["participants"]}',
                                    dest='ru').text
        bot.send_message(message.chat.id, text=text)

        keyboard = ReplyKeyboardMarkup(row_width=1)
        but1 = KeyboardButton(text='Главное меню')
        keyboard.add(but1)
        bot.send_message(message.chat.id, text='Перейти в главное меню?', reply_markup=keyboard)

        bot.register_next_step_handler(message, main_menu)

    elif message.text == 'Посмотреть на котика':

        bot.send_message(message.chat.id, f'Вот вам миленький котик')

        bot.send_photo(message.chat.id, f'https://http.cat/status/{random.choice(png)}')

        keyboard = ReplyKeyboardMarkup(row_width=1)
        but1 = KeyboardButton(text='Главное меню')
        keyboard.add(but1)
        bot.send_message(message.chat.id, text='Перейти в главное меню?', reply_markup=keyboard)

        bot.register_next_step_handler(message, main_menu)

    elif message.text == 'Цитата Стейтема':

        with open('Statem.txt', 'r', encoding='utf-8') as f:
            quotes = f.readlines()
            rnum = random.randint(1, 35)
            selected_quote = quotes[rnum-1]
            bot.send_message(message.chat.id, text=selected_quote.strip())

        keyboard = ReplyKeyboardMarkup(row_width=1)
        but1 = KeyboardButton(text='Главное меню')
        keyboard.add(but1)
        bot.send_message(message.chat.id, text='Перейти в главное меню?', reply_markup=keyboard)

        bot.register_next_step_handler(message, main_menu)

    elif message.text == 'Коктейль':

        bot.send_message(message.chat.id, text=f'Напишите ингредиент')

        bot.register_next_step_handler(message, cocktail)

    elif message.text == 'О боте':

        text = (f'Ещё раз привет, я телеграм бот, который поможет тебе понять настроение '
                f'(ты модешь почитать смешные цитаты).\n'
                f'Ещё я помогу тебе справиться с прокрастинацией или помочь найти хобби '
                f'(просто нажми на кнопку <b>"Чем заняться, когда скучно?"</b>)\n'
                f'Так же ты можешь посмотреть на миленьких котиков '
                f'(кнопочка <b>"Посмотреть на котика"</b>) PS Это ты)))\n'
                f'А если ты хочешь провести весело время с друзьями, но при этом вы хотите что-нибдь выпить, '
                f'нажми на кнопку <b>"Коктейль"</b> (к содалению нужно написать только 1 ингредиент) '
                f'<b>ВАЖНАЯ ИНФОРМАЦИЯ</b> создатель этого бота <b>не призывает</b> вас к употреблению алкоголя!!!! '
                f'<b>Срого 18+</b>\n\n'
                f'После каждого действия нужно аереходить в Главное меню'
                f'с помощью кнопки <b>"Главное меню"</b>\n\n'
                f'P.S. Зарание извиняюсь за грамматические и пунктационные ошибки,'
                f' потому что этот текст пишется в 04:49 утра')

        bot.send_message(message.chat.id, text=text)

        keyboard = ReplyKeyboardMarkup(row_width=1)
        but1 = KeyboardButton(text='Главное меню')
        keyboard.add(but1)
        bot.send_message(message.chat.id, text='Перейти в главное меню?', reply_markup=keyboard)

        bot.register_next_step_handler(message, main_menu)

    elif message.text == 'Контакты':
        bot.send_message(message.chat.id, text=f'Это мои социальные сети:\n'
                                               f'<b>Инстаграм:</b> https://instagram.com/sodesensitized?igshid=OGQ5ZDc2ODk2ZA==&utm_source=qr\n'
                                               f'<b>Телеграм: @sodesensitized</b>\n'
                                               f'<b>ВК: https://vk.com/gameworlduhd</b>\n'
                                               f'<b>ТГ канал: https://t.me/realodman</b>\n'
                                               f'<b>Телефон: +79630280421</b>')

        keyboard = ReplyKeyboardMarkup(row_width=1)
        but1 = KeyboardButton(text='Главное меню')
        keyboard.add(but1)
        bot.send_message(message.chat.id, text='Перейти в главное меню?', reply_markup=keyboard)

        bot.register_next_step_handler(message, main_menu)

    else:
        bot.send_message(message.chat. id, text='Что-то пошло не так')

        keyboard = ReplyKeyboardMarkup(row_width=1)
        but1 = KeyboardButton(text='Главное меню')
        keyboard.add(but1)
        bot.send_message(message.chat.id, text='Перейти в главное меню?', reply_markup=keyboard)

        bot.register_next_step_handler(message, main_menu)

#Функция для получение коктейля
def cocktail(message):
    name = translator.translate(message.text).text
    api_url = 'https://api.api-ninjas.com/v1/cocktail?name={}'.format(name)
    response = requests.get(api_url, headers={'X-Api-Key': 'oMVgtgNVbdxFSaVyCb48iA==MT3VKWF3lvWu9Dfu'})
    if response.status_code == requests.codes.ok:
        data = json.loads(response.text)
        for cocktail in data:
            a = translator.translate("; ".join(cocktail["ingredients"]), dest='ru').text
            b = translator.translate(cocktail['instructions'], dest='ru').text
            c = translator.translate(cocktail['name'], dest='ru').text
            text = (f'<b>Название:</b> {c}\n'
                    f'<b>ингредиенты: </b>{a}\n'
                    f'<b>Инструкция: </b>{b}')
            bot.send_message(message.chat.id, text=text)

    else:
        bot.send_message(message.chat.id, text=f'Что то пошло не так, {response.status_code, response.text}')

    keyboard = ReplyKeyboardMarkup(row_width=1)
    but1 = KeyboardButton(text='Главное меню')
    keyboard.add(but1)
    bot.send_message(message.chat.id, text='Перейти в главное меню?', reply_markup=keyboard)

    bot.register_next_step_handler(message, main_menu)


def test_action():
    translator = Translator()
    res = requests.get(f'http://www.boredapi.com/api/activity/')
    return res.json()


#Бот работает всегда
bot.polling(none_stop=True)
