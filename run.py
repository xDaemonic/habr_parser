import asyncio, datetime
from bot.create import bot, dp, scheduler
from handlers.start import start_router
from parsers import HabrParser
from storage.logger import logger

async def main():
  # scheduler.add_job(send_time_msg, 'interval', seconds=3)
  # scheduler.start()
  
  dp.include_router(start_router)
  await bot.delete_webhook(drop_pending_updates=True)
  await dp.start_polling(bot)
  
if __name__ == '__main__':
  asyncio.run(main())