import telegram
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler

from config import TG_TOKEN as TOKEN
from config import HEROKU_URL

import os

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def hello(update, context):
    update.message.reply_text('Hello {}. I am a bot. I am comparing models that you will upload and to make sure it is not duplicating.'.format(update.message.from_user.first_name))

def compare_models(update,context):
    chat_id = update.effective_chat.id
    message_id = update.message.message_id
    file_name = update.message.document.file_name
    file_id = update.message.document.file_id

    flag = True

    with open(r'list_models.txt', 'r') as file:
        model_list = file.readlines()
    print("model list:", model_list, ". Len:", len(model_list))

    for model in model_list:
        print("Model:", model)
        curModel = model.split(',')
        print("curModel =", curModel)
        if (curModel[1] == (file_name+'\n')): 
            print("Same model name:", curModel[1])
            context.bot.delete_message(chat_id, message_id)
            context.bot.send_message(chat_id, text="Model with name *%s* was uploading early." % curModel[1], parse_mode=telegram.ParseMode.MARKDOWN)
            flag = False
            break

    if (flag):
        model_list.append("{},{}\n".format(file_id,file_name))
        print("New model list:", model_list)
        with open(r'list_models.txt', 'w') as file:
            file.writelines("%s" % line for line in model_list)
        context.bot.send_message(chat_id, text="Model with name *%(file_name)* and id *%(file_id)* was adding.", parse_mode=telegram.ParseMode.MARKDOWN)

    print("FIle name:", file_name)

PORT = int(os.environ.get('PORT', '8443'))
updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher

if __name__ == '__main__':
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN)
    updater.bot.set_webhook(HEROKU_URL + TOKEN)

    dispatcher.add_handler(CommandHandler('hello', hello))
    check_doc_message = MessageHandler(Filters.document, compare_models)
    dispatcher.add_handler(check_doc_message)

    updater.idle()