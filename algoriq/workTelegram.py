import logging
from aiogram import Bot, Dispatcher, types

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from hubSpotWork import create_hubspot_lead
API_TOKEN = 'YOUR_API_TOKEN'

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
# dp.middleware.setup(LoggingMiddleware())

# Хранилище состояний пользователей
states = {}


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Привет! Этот бот поможет вам изучать что-то интересное. Нажмите 'Начать', чтобы начать.")
    states[message.chat.id] = "start"


@dp.message_handler(lambda message: states.get(message.chat.id) == "start")
async def handle_start_button(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Начать", callback_data="watch_circle"))
    await message.answer("Нажмите кнопку 'Начать', чтобы продолжить.", reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == "watch_circle")
async def watch_circle(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_video(callback_query.message.chat.id, video=open('circle_video.mp4', 'rb'))
    states[callback_query.message.chat.id] = "watch_explainer"


@dp.message_handler(lambda message: states.get(message.chat.id) == "watch_explainer")
async def handle_watch_explainer(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Смотреть", callback_data="watch_explainer_video"))
    await message.answer("Нажмите кнопку 'Смотреть', чтобы продолжить.", reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == "watch_explainer_video")
async def watch_explainer_video(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_video(callback_query.message.chat.id, video=open('explainer_video.mp4', 'rb'))
    states[callback_query.message.chat.id] = "watch_example"


@dp.message_handler(lambda message: states.get(message.chat.id) == "watch_example")
async def handle_watch_example(message: types.Message):
    await message.answer("Теперь я покажу вам пример из Гайда:")
    await message.answer_video(video=open('example_video.mp4', 'rb'))
    states[message.chat.id] = "provide_email"


@dp.message_handler(lambda message: states.get(message.chat.id) == "provide_email")
async def handle_provide_email(message: types.Message):
    await message.answer("Пожалуйста, введите ваш email:")
    states[message.chat.id] = "awaiting_email"


@dp.message_handler(lambda message: states.get(message.chat.id) == "awaiting_email")
async def handle_email_response(message: types.Message):
    email = message.text.strip()
    create_hubspot_lead(email)
    await message.answer("Спасибо за ваш email! Ваш лид успешно создан в HubSpot.")
    
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(text="🔄 Дать фидбек по продукту", callback_data="feedback"),
        InlineKeyboardButton(text="☎️ Связаться с нами", callback_data="contact_us"),
        InlineKeyboardButton(text="🎓 Информация и обучение", callback_data="info_and_training")
    )
    await message.answer("Ссылка на наш продукт: [Название продукта](http://example.com)", reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == "feedback")
async def handle_feedback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.message.chat.id, "Вы выбрали '🔄 Дать фидбек по продукту'.")


@dp.callback_query_handler(lambda c: c.data == "contact_us")
async def handle_contact_us(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.message.chat.id, "Вы выбрали '☎️ Связаться с нами'.")


@dp.callback_query_handler(lambda c: c.data == "info_and_training")
async def handle_info_and_training(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.message.chat.id, "Вы выбрали '🎓 Информация и обучение'.")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    dp.loop.run_until_complete(dp.start_polling())
