import telebot, os
from dotenv import load_dotenv
from src.models import User, defineModel

load_dotenv()
defineModel()

bot = telebot.TeleBot(os.environ['BOT_API_TOKEN'])

@bot.message_handler(commands=['start'])
def send_welcome(message):
  user = message.from_user
  if not User.where_id(user.id).exists():
    user_model = User.create(**user.to_dict())
    
  user_model = User.find(user.id)
  bot.reply_to(message, user_model.to_json())


@bot.message_handler(func=lambda message: True)
def echo_all(message):
  user = message.from_user
  if not User.where_id(user.id).exists():
    User.create(**user.to_dict())
    
  bot.reply_to(message, user.to_json())

bot.infinity_polling()