import logging
# from aiogram import Bot, Dispatcher, types
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from telebot import types   
from pprint import pprint
# from helper import *
# from aiogram.enums.parse_mode import ParseMode
# from aiogram.fsm.storage.memory import MemoryStorage

# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from hubSpotWork import create_hubspot_lead
import textMess
from dotenv import load_dotenv
import os
load_dotenv()

API_TOKEN = os.environ.get('API_TOKEN')
print(API_TOKEN)
# Инициализация бота и диспетчера
# bot = Bot(token=API_TOKEN)
bot = telebot.TeleBot(API_TOKEN, parse_mode='Markdown')
# print(bot)
# dp = Dispatcher(storage=MemoryStorage())

# dp.middleware.setup(LoggingMiddleware())

# Хранилище состояний пользователей
states = {}


# Обработчик бизнес-соединений
# @bot.business_connection_handler(func=lambda business_connection: True)
# def handle_business_connection(business_connection):
#     update_business_connection(business_connection)
#     logging.info(f"Business connection updated: {business_connection.id}")

# @bot.business_message_handler(func=lambda message: True, content_types=['text', 'photo', 'video'])
# def handle_business_message(message):

# @bot.message_handler(lambda message: states.get(message.chat.id) == "start")
@bot.message_handler(commands=['start'])
def handle_start_button(message: types.Message):

    keyboard = InlineKeyboardMarkup()
    
    keyboard.add(InlineKeyboardButton(text="Смотреть обучение", callback_data="watch_circle"))
    # keyboard = ReplyKeyboardMarkup()
    # keyboard.add(KeyboardButton('Смотреть обучение'))
        # InlineKeyboardButton(text="🔄 Дать фидбек по продукту", callback_data="feedback"),)
    chatID=message.chat.id

    # bot.send_message(chatID, textMess.startText, reply_markup=keyboard, business_connection_id=business_connection_id)
    bot.send_message(chatID, textMess.startText, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda c: c.data == "watch_circle")
def watch_circle(callback_query: types.CallbackQuery):
    # bot.send_video_note(callback_query.message.chat.id, video_note=open('circle_video.mp4', 'rb'))
    bot.send_video_note(callback_query.message.chat.id, data=open('video1.mp4', 'rb'))
    bot.send_video_note(callback_query.message.chat.id, data=open('video2.mp4', 'rb'))
    bot.send_video_note(callback_query.message.chat.id, data=open('video3.mp4', 'rb'))
    states[callback_query.message.chat.id] = "watch_explainer"
    bot.answer_callback_query(callback_query.id)
    handle_watch_explainer(callback_query.message) 

@bot.message_handler(func=lambda message: states.get(message.chat.id) == "watch_explainer")
def handle_watch_explainer(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="«Далее»", callback_data="watch_explainer_video"))
    chatID=message.chat.id
    bot.send_message(chatID,"Нажмите кнопку «Далее», чтобы продолжить.", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda c: c.data == "watch_explainer_video")
def watch_explainer_video(callback_query: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Пример результата", callback_data="watch_example"))
    keyboard.add(InlineKeyboardButton(text="Получить доступ", callback_data="provide_email"))
    # bot.send_video(callback_query.message.chat.id, video=open('explainer_video.mp4', 'rb'))
    bot.send_video(callback_query.message.chat.id, video=open('test.mp4', 'rb'), reply_markup=keyboard)
    bot.answer_callback_query(callback_query.id)
    states[callback_query.message.chat.id] = "watch_example"
    
    # handle_watch_example(callback_query.message)



@bot.callback_query_handler(func=lambda c: c.data == "watch_example")
def handle_watch_example(message: types.CallbackQuery):
    chatID=message.message.chat.id
    bot.send_message(chatID,textMess.textVideoGuide)
    # bot.answer_video(video=open('example_video.mp4', 'rb'))
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Получить доступ", callback_data="provide_email"))
    bot.send_video(chatID, video=open('test.mp4', 'rb'),reply_markup=keyboard)
    states[chatID] = "urls_message"
    bot.answer_callback_query(message.id)
    # handle_provide_email(message)




@bot.callback_query_handler(func=lambda c: c.data == "urls_message")
def handle_provide_email(message: types.CallbackQuery):
    # chatID=message.chat.id
    chatID=message.message.chat.id
    bot.answer_callback_query(message.id)
    # print('email', message.text)
    bot.send_message(chatID,textMess.urlMessage)
    states[chatID] = "provide_email"
    handle_awaiting_email(message) 


@bot.callback_query_handler(func=lambda c: c.data == "provide_email")
def handle_awaiting_email(message: types.CallbackQuery):
    chatID=message.message.chat.id
    bot.answer_callback_query(message.id)
    bot.send_message(chatID,textMess.emailText)
    states[chatID] = "awaiting_email"
    # handle_email_response(message) 


@bot.message_handler(func=lambda message: states.get(message.chat.id) == "awaiting_email")
def handle_email_response(message: types.Message):
    chatID=message.chat.id
    email = message.text.strip()
    # create_hubspot_lead(email)
    # bot.send_message(chatID,"Спасибо за ваш email! Ваш лид успешно создан в HubSpot.")

    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(text="🔄 Дать фидбек по продукту", callback_data="feedback"),
        InlineKeyboardButton(text="☎️ Связаться с нами", callback_data="contact_us"),
        InlineKeyboardButton(text="🎓 Информация и обучение", callback_data="info_and_training")
        # InlineKeyboardButton(text="🔄 Дать фидбек по продукту", url='https://t.me/m/9BaYmNnXZjc1'),
        # InlineKeyboardButton(text="☎️ Связаться с нами", url=''
        # InlineKeyboardButton(text="🎓 Информация и обучение", callback_data="info_and_training")
    )
    #message.send_message(chatID,"Ссылка на наш продукт: [Название продукта](http://example.com)", reply_markup=keyboard)
    bot.send_message(chatID,textMess.endText, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda c: c.data == "feedback")
def handle_feedback(callback_query: types.CallbackQuery):
    bot.answer_callback_query(callback_query.id)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(text="🔝 Предложить улучшение работы AlgoriQ", url='https://t.me/m/9BaYmNnXZjc1'))
    keyboard.add(
        InlineKeyboardButton(text="⚙️ Предложить улучшение использования", url='https://t.me/m/_-0QzNy2NzBl',))
    keyboard.add(
        InlineKeyboardButton(text="🚨 Сообщить об ошибке", url='https://t.me/m/DS1FAx5DZmJl',))
    bot.send_message(callback_query.message.chat.id, "Вы выбрали '🔄 Дать фидбек по продукту'.", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda c: c.data == "contact_us")
def handle_contact_us(callback_query: types.CallbackQuery):
    bot.answer_callback_query(callback_query.id)
    bot.send_message(callback_query.message.chat.id, """Рады будем пообщаться, ответить на твои вопросы и обсудить как сделать AlgoriQ лучше!

Напиши, что ты хочешь обсудить и в каком формате? Мы можем початиться тут в боте или созвониться в Zoom/Google.Meet.""")


@bot.callback_query_handler(func=lambda c: c.data == "feedback1")
def handle_contact_us(callback_query: types.CallbackQuery):
    bot.answer_callback_query(callback_query.id)
    bot.send_message(callback_query.message.chat.id, """Супер, нам очень ценны твое мнение и предложения!
Напиши сообщением ниже или запиши аудио о том, что ты хочешь улучшить.

Если у тебя есть время коротко созвониться и лично рассказать нам о своем опыте и предложении, то напиши свои доступные окна и лучше пообщаться лично!""")
@bot.callback_query_handler(func=lambda c: c.data == "feedback2")
def handle_contact_us(callback_query: types.CallbackQuery):
    bot.answer_callback_query(callback_query.id)
    bot.send_message(callback_query.message.chat.id, """Мы делаем продукт для профи, поэтому твои требования и опыт для нас главный ориентир в развитии продукта.
Напиши сообщением ниже или запиши аудио о том, что ты хочешь улучшить.

Если у тебя есть время коротко созвониться и лично рассказать нам о своем опыте и предложении, то напиши свои доступные окна и лучше пообщаться лично!""")
@bot.callback_query_handler(func=lambda c: c.data == "feedback3")
def handle_contact_us(callback_query: types.CallbackQuery):
    bot.answer_callback_query(callback_query.id)
    bot.send_message(callback_query.message.chat.id, """Это первая версия продукта, поэтому, к сожалению, ошибки возможны.
Очень ценно, что ты не поленился и забил, а сообщаешь нам об этом, без тебя мы бы о них вряд ли узнали бы 🫶🏼

Напиши подробно или запиши аудио о том, что случилось (или не случилось) 🙌️️️️️️""")


@bot.callback_query_handler(func=lambda c: c.data == "info_and_training")
def handle_info_and_training(callback_query: types.CallbackQuery):
    bot.answer_callback_query(callback_query.id)
    bot.send_message(callback_query.message.chat.id, textMess.urlMessage)

@bot.message_handler()
def handle_start_button(message):
    # def handle_start_button(message: types.Message):
    pprint(message.__dict__)
    print('message: ', message.text)
    сhatID=message.chat.id
    # keyboard = InlineKeyboardMarkup()
    # keyboard.add(InlineKeyboardButton(text="Смотреть обучение", callback_data="watch_circle"))
    # chatID=message.chat.id
    bot.send_message(сhatID, textMess.startText,)

if __name__ == '__main__':
    print('[OK]')
    logging.basicConfig(level=logging.INFO)
    # dp.loop.run_until_complete(dp.start_polling())
    # print(f'[OK]')
    bot.infinity_polling()