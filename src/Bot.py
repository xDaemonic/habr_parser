import telebot
from telebot import types

class TelegramBot:
    def __init__(self, token):
        self.token = token
        self.bot = telebot.TeleBot(token=self.token, parse_mode='HTML')

    def send_message_to_all(self, message):
        chat_ids = self.bot.get_chat_list()
        for chat_id in chat_ids:
            self.bot.send_message(chat_id=chat_id, text=message)
