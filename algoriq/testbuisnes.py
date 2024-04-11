import logging
import json
import os
# import openai
from telebot import TeleBot, types
from dotenv import load_dotenv
import os
load_dotenv()

import sqlite3

# Настройка детального логирования
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Токены API
TELEGRAM_TOKEN = os.getenv('API_TOKEN')
# OPENAI_API_KEY = 'ВСТАВЬ_СВОЙ_ТОКЕН_OPENAI'

# Инициализация OpenAI API
# openai.api_key = OPENAI_API_KEY

# Инициализация бота Telegram 
bot = TeleBot(TELEGRAM_TOKEN)

# Создание таблицы для хранения истории сообщений
def create_table():
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS chat_history
    (user_id INTEGER, business_connection_id TEXT, message_role TEXT, message_content TEXT)''')
    conn.commit()
    conn.close()

# Сохранение сообщения в базу данных
def save_message(user_id, business_connection_id, message_role, message_content):
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute("INSERT INTO chat_history (user_id, business_connection_id, message_role, message_content) VALUES (?, ?, ?, ?)",
    (user_id, business_connection_id, message_role, message_content))
    conn.commit()
    conn.close()

# Получение истории сообщений для определенного пользователя и бизнес-соединения 
def get_chat_history(user_id, business_connection_id):
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute("SELECT message_role, message_content FROM chat_history WHERE user_id=? AND business_connection_id=? ORDER BY rowid",
    (user_id, business_connection_id))
    chat_history = c.fetchall()
    conn.close()
    return chat_history

# Путь к файлу JSON для хранения данных о бизнес-соединениях
json_db_path = 'business_connections.json'

# Загрузка данных о бизнес-соединениях
def load_business_connections():
    if os.path.exists(json_db_path):
        with open(json_db_path, 'r') as file:
            return json.load(file)
    else:
        logging.warning("Business connections file not found. Creating a new one.")
    return {}

# Сохранение данных о бизнес-соединениях 
def save_business_connections(business_connections):
    logging.debug(f"Saving business connections: {business_connections}")
    try:
        with open(json_db_path, 'w') as file:
            json.dump(business_connections, file, indent=2)
    except Exception as e:
        logging.error(f"Error saving business connections: {e}")

# Обновление бизнес-соединения
def update_business_connection(business_connection):
    business_connection_id = business_connection.id
    user_chat_id = business_connection.user_chat_id
    can_reply = business_connection.can_reply
    is_enabled = business_connection.is_enabled
    date = business_connection.date

    logging.debug(f"Updating business connection: {business_connection_id}")
    business_connections = load_business_connections()
    business_connections[business_connection_id] = {
        'user_chat_id': user_chat_id,
        'can_reply': can_reply,
        'is_enabled': is_enabled,
        'date': date
    }
    save_business_connections(business_connections)

# Получение бизнес-соединения 
def get_business_connection(business_connection_id):
    business_connections = load_business_connections()
    return business_connections.get(business_connection_id)

# Обработчик бизнес-соединений
@bot.business_connection_handler(func=lambda business_connection: True)
def handle_business_connection(business_connection):
    update_business_connection(business_connection)
    logging.info(f"Business connection updated: {business_connection.id}")

@bot.business_message_handler(func=lambda message: True, content_types=['text', 'photo', 'video'])
def handle_business_message(message):
    user_id = message.chat.id
    print(message.text)
    business_connection_id = message.business_connection_id
    logging.info(f"Received business message from {user_id}: {message.text}")

    # Обновляем информацию о бизнес-соединении 
    business_connection = get_business_connection(business_connection_id)
    if business_connection:
        business_connection['can_reply'] = True
        business_connection['is_enabled'] = True
        save_business_connections(load_business_connections())

    # Если это первое сообщение, создаем новое бизнес-соединение
    else:
        business_connection = {
        'user_chat_id': message.chat.id,
        'can_reply': True,
        'is_enabled': True,
        'date': message.date
        }
        business_connections = load_business_connections()
        business_connections[business_connection_id] = business_connection
        save_business_connections(business_connections)

    if business_connection and business_connection.get('is_enabled') and business_connection.get('can_reply'):
        try:
    # Сохранение входящего сообщения в базу данных
            save_message(user_id, business_connection_id, 'user', message.text)

    # Получение истории сообщений из базы данных
            chat_history = get_chat_history(user_id, business_connection_id)
            messages = [
            {"role": "system", "content": "Привет! Ты - ИИ-помощник для бизнеса в Telegram. Отвечай на вопросы пользователей, основываясь на контексте переписки."},
            *[{"role": role, "content": content} for role, content in chat_history] 
            ]

            # response = openai.ChatCompletion.create(
            # model="gpt-3.5-turbo",
            # messages=messages,
            # max_tokens=1000, 
            # temperature=0.8,
            # )
            # message_text = response.choices[0].message.content

            # Сохранение ответа бота в базу данных 
            # save_message(user_id, business_connection_id, 'assistant', message_text)

            bot.send_message(message.chat.id, 'message_text', reply_to_message_id=message.id, business_connection_id=business_connection_id)
            logging.info("Response sent to business chat")
        except Exception as e:
            logging.error(f"Error generating or sending response to business chat: {e}")
    else:
        logging.warning(f"Business connection not found or not enabled: {business_connection_id}") 

# Обработчик личных сообщений 
@bot.message_handler(content_types=['text'])
def handle_private_message(message):
    logging.debug("Handling private message")
    try:
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": message.text}
        ],
        max_tokens=50,
        temperature=0.7,
        )
        message_text = response.choices[0].message.content
        bot.reply_to(message, message_text)
    except Exception as e:
        logging.error(f"Error generating or sending response to private chat: {e}")

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    logging.debug("Handling /start command")
    bot.reply_to(message, "Привет! Я ваш бот.")

if __name__ == "__main__":
    create_table() # Создание таблицы для хранения истории сообщений
    logging.info("Starting the bot") 
    bot.infinity_polling()