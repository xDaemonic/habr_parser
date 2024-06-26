from storage.logger import logger
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from models import User
from bot.messages import welcome

start_router = Router()


@start_router.message(CommandStart())
async def cmd_start(message: Message):
  new_user = { 
    'user_id': message.from_user.id, 
    'user_name': message.from_user.username, 
    'user_nickname': message.from_user.first_name 
  }
  
  user = User.firstOrCreate(new_user)
  await message.answer(welcome(user.getAttribute('user_nickname')))
  
@start_router.message()
async def cmd(message: Message):
  await message.answer(message.text[::-1])