import logging
import telebot
import os.path
import os
from flask import Flask, request


if "TOKEN" in list(os.environ.keys()):
    # Проверка токена из Хероку
    TOKEN = os.getenv("TOKEN")
    URL = os.getenv("URL")
else:
    TOKEN = "ВАШ ТОКЕН"

bot = telebot.TeleBot(TOKEN)
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


@bot.message_handler(commands=["start"])
def start_bot(message):
    bot.send_message(message.chat.id, "Ok!", reply_to_message_id=message.message_id)


@bot.message_handler(content_types=["document"])
def start_doc(message):
    print(message)
    flag = True
    filedata = str(message.chat.id) + ".txt"
    try:
        if os.path.exists(filedata):
            with open(filedata, 'r', encoding="utf-8") as file:
                model_list = file.readlines()
        else:
            with open(filedata, 'w+', encoding="utf-8") as file:
                model_list = file.readlines()
    except:
        bot.send_message(message.chat.id, "😤Больше так не делаете!", reply_to_message_id=message.message_id)


    for model in model_list:
        # Удаления файла
        curModel = model.split(',')
        if curModel[1 ] == (message.document.file_name + '\n'):
            bot.delete_message(message.chat.id, message.message_id)
            # bot.send_message(message.chat.id, text="File with name *%s* was uploading early." % curModel[1], parse_mode="markdown")
            flag = False
            break

    if flag:
        # Добавления файла
        model_list.append("{},{}\n".format(message.document.file_id, message.document.file_name))
        try:
            with open(filedata, 'w', encoding="utf-8") as file:
                file.writelines("%s" % line for line in model_list)
        except:
            bot.send_message(message.chat.id, "😤Больше так не делаете!", reply_to_message_id=message.message_id)


        # bot.send_message(message.chat.id, text="File with name *{}* was adding.".format(message.document.file_name), parse_mode="markdown")


# Проверим, есть ли переменная окружения Хероку (как ее добавить смотрите ниже)
if "URL" in list(os.environ.keys()):
    logger = telebot.logger
    telebot.logger.setLevel(logging.INFO)
    server = Flask(__name__)
    @server.route("/bot", methods=['POST'])
    def getMessage():
        bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
        return "!", 200
    @server.route("/")
    def webhook():
        bot.remove_webhook()
        bot.set_webhook(url=URL)
        return "?", 200
    server.run(host="0.0.0.0", port=os.environ.get('PORT', 80))
else:
    # если переменной окружения HEROKU нету, значит это запуск с машины разработчика.
    # Удаляем вебхук на всякий случай, и запускаем с обычным поллингом.
    bot.remove_webhook()
    bot.polling(none_stop=True)