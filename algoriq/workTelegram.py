import logging
# from aiogram import Bot, Dispatcher, types
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from telebot import types   
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



# @bot.message_handler(lambda message: states.get(message.chat.id) == "start")
@bot.message_handler(commands=['start'])
def handle_start_button(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Начать", callback_data="watch_circle"))
    chatID=message.chat.id
    
    bot.send_message(chatID, textMess.startText, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda c: c.data == "watch_circle")
def watch_circle(callback_query: types.CallbackQuery):
    bot.answer_callback_query(callback_query.id)
    # bot.send_video_note(callback_query.message.chat.id, video_note=open('circle_video.mp4', 'rb'))
    bot.send_video_note(callback_query.message.chat.id, data=open('test.mp4', 'rb'))
    states[callback_query.message.chat.id] = "watch_explainer"
    handle_watch_explainer(callback_query.message) 

@bot.message_handler(func=lambda message: states.get(message.chat.id) == "watch_explainer")
def handle_watch_explainer(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Смотреть", callback_data="watch_explainer_video"))
    chatID=message.chat.id
    bot.send_message(chatID,"Нажмите кнопку 'Смотреть', чтобы продолжить.", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda c: c.data == "watch_explainer_video")
def watch_explainer_video(callback_query: types.CallbackQuery):
    bot.answer_callback_query(callback_query.id)
    # bot.send_video(callback_query.message.chat.id, video=open('explainer_video.mp4', 'rb'))
    bot.send_video(callback_query.message.chat.id, video=open('test.mp4', 'rb'))
    states[callback_query.message.chat.id] = "watch_example"
    handle_watch_example(callback_query.message)


@bot.message_handler(func=lambda message: states.get(message.chat.id) == "watch_example")
def handle_watch_example(message: types.Message):
    chatID=message.chat.id
    bot.send_message(chatID,textMess.textVideoGuide)
    # bot.answer_video(video=open('example_video.mp4', 'rb'))
    bot.send_video(chatID, video=open('test.mp4', 'rb'))
    states[message.chat.id] = "urls_message"
    handle_provide_email(message)


@bot.message_handler(func=lambda message: states.get(message.chat.id) == "urls_message")
def handle_provide_email(message: types.Message):
    chatID=message.chat.id
    # print('email', message.text)
    bot.send_message(chatID,textMess.urlMessage)
    states[message.chat.id] = "provide_email"
    handle_awaiting_email(message) 


@bot.message_handler(func=lambda message: states.get(message.chat.id) == "provide_email")
def handle_awaiting_email(message: types.Message):
    chatID=message.chat.id
    bot.send_message(chatID,textMess.emailText)
    states[message.chat.id] = "awaiting_email"
    # handle_email_response(message) 


@bot.message_handler(func=lambda message: states.get(message.chat.id) == "awaiting_email")
def handle_email_response(message: types.Message):
    chatID=message.chat.id
    email = message.text.strip()
    # create_hubspot_lead(email)
    bot.send_message(chatID,"Спасибо за ваш email! Ваш лид успешно создан в HubSpot.")

    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(text="🔄 Дать фидбек по продукту", callback_data="feedback"),
        InlineKeyboardButton(text="☎️ Связаться с нами", callback_data="contact_us"),
        InlineKeyboardButton(text="🎓 Информация и обучение", callback_data="info_and_training")
    )
    #message.send_message(chatID,"Ссылка на наш продукт: [Название продукта](http://example.com)", reply_markup=keyboard)
    bot.send_message(chatID,textMess.endText, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda c: c.data == "feedback")
def handle_feedback(callback_query: types.CallbackQuery):
     bot.answer_callback_query(callback_query.id)
     bot.send_message(callback_query.message.chat.id, "Вы выбрали '🔄 Дать фидбек по продукту'.")


@bot.callback_query_handler(func=lambda c: c.data == "contact_us")
def handle_contact_us(callback_query: types.CallbackQuery):
     bot.answer_callback_query(callback_query.id)
     bot.send_message(callback_query.message.chat.id, "Вы выбрали '☎️ Связаться с нами'.")


@bot.callback_query_handler(func=lambda c: c.data == "info_and_training")
def handle_info_and_training(callback_query: types.CallbackQuery):
     bot.answer_callback_query(callback_query.id)
     bot.send_message(callback_query.message.chat.id, "Вы выбрали '🎓 Информация и обучение'.")

if __name__ == '__main__':
    print('[OK]')
    logging.basicConfig(level=logging.INFO)
    # dp.loop.run_until_complete(dp.start_polling())
    # print(f'[OK]')
    bot.infinity_polling()