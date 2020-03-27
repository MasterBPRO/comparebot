from models import *


def find_file(name, file_id, chat_id):
    """
    Функция для поиска файла в Базе Данных
    :param name: Имя файла
    :param file_id: ID файла, который генерирует Телеграм
    :param chat_id: ID чата с которого пришёл файл
    :return: Возвращает True если файл найден, в противном случае возвращает False
    """
    try:
        File.get(File.name == name and File.file_id == file_id and File.chat_id == chat_id)
        return True

    except Exception:
        return False


def add_file(name, file_id, chat_id):
    """
    Функция для добавления файла в Базу Данных
    :param name: Имя файла
    :param file_id: ID файла, который генерирует Телеграм
    :param chat_id: ID чата с которого пришёл файл
    :return:
    """
    try:
        file = File(name=name, file_id=file_id, chat_id=chat_id)
        file.save()
        return True

    except Exception:
        return False


def del_file(name, file_id, chat_id):
    """
    Функция для удаления файла из Базы Данных
    :param name: Имя файла
    :param file_id: ID файла, который генерирует Телеграм
    :param chat_id: ID чата с которого пришёл файл
    :return:
    """
    try:
        data = File.get(File.name == name and File.file_id == file_id and File.chat_id == chat_id)
        data.delete_instance()
        return True

    except Exception:
        return False