from aiogram.types import ContentType

from Note import Note
from Shares import Shares
from secret import token
import logging
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = token
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(content_types=ContentType.ANY)
async def receive(message: types.Message):
    """
    This handler will be called when user sends any message
    """
    print(f'type: {type(message)}, message: {message}')
    shares = Shares(message)
    response_type = await shares.process()
    if response_type == 'img':
        reply_message = 'Image uploaded'
    elif response_type == 'url':
        reply_message = 'note saved'
    else:
        reply_message = 'Unknown message type'
    await message.reply(reply_message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
