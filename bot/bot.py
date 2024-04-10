import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import handlers
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config.config import settings
from middleware import DbSessionMiddleware
from config.database import db_session
from schedulers import send_message_users


logging.basicConfig(
    level=logging.INFO,
)


async def main():
    bot = Bot(token="7171494016:AAHt3Xr5v7g8T4-VN_ElB67kCBGOs2mayis")
    storage = RedisStorage.from_url('redis://localhost:6379/0', state_ttl=60*10)
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(send_message_users, 'interval', seconds=60*60, kwargs={'bot': bot})
    scheduler.start()
    dp = Dispatcher(storage=storage)
    dp.include_routers(handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, scheduler=scheduler)


if __name__ == "__main__":
    asyncio.run(main())


