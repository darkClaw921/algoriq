# Путь к файлу JSON для хранения данных о бизнес-соединениях

import logging
import json
import os
# import openai
# from telebot import TeleBot, types
from dotenv import load_dotenv
import os
load_dotenv()

import sqlite3

# Настройка детального логирования
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

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

