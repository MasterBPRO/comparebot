import logging
import os.path
import telebot
import models
from src import *

bot = telebot.TeleBot("ТОКЕН БОТА")
logging.basicConfig(filename="compare.log", level=logging.ERROR, format='[LINE:%(lineno)d] %(levelname)-8s [%(asctime)s]  %(message)s')

if not os.path.exists("file.db"):  # Создания Базы Данных
    models.File.create_table()


@bot.message_handler(commands=["start"])
def start_bot(message):
    bot.send_message(message.chat.id, "🛸 Система активна!", reply_to_message_id=message.message_id)


@bot.message_handler(content_types=["document"])
def start_doc(message):
    chat_id = str(message.chat.id)
    file_name = message.document.file_name
    file_id = message.document.file_id
    message_id = message.message_id

    if find_file(name=file_name, chat_id=chat_id):
        print('Удаляем!')
        bot.delete_message(chat_id=chat_id, message_id=message_id)
    else:
        print('Добавляем!')
        add_file(name=file_name, file_id=file_id, chat_id=chat_id)


bot.polling(none_stop=True)
