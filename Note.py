import asyncio
import os
from datetime import datetime

import requests
from aiogram import types
from bs4 import BeautifulSoup
from config import DATA_DIR


class Note:
    title: str = None
    body: str = None
    image: str = None
    user: str = None
    private: bool = True
    timestamp: int = None

    def __init__(self, title='', body='', image='', user='', date=0):
        self.title = title
        self.body = body
        self.image = image
        self.user = user
        self.created_at = date
        return

    @classmethod
    async def create_from_message(cls, message: types.Message):
        title = await cls.get_title(message)
        body = message.text if message.text else ''
        image = await cls.load_image(message)
        user = message.from_user.username
        date = int(message.date.timestamp())
        return cls(
            title=title,
            body=body,
            image=image,
            user=user,
            date=date
        )

    @classmethod
    async def get_title(cls, message: types.Message) -> str:
        title = 'Without title'
        if len(message.photo) > 0:
            title = message.md_text
        for entity in message.entities:
            if entity.type == 'url':
                title = await asyncio.ensure_future(cls.get_title_from_url(message.text[entity.offset: entity.length]))
                # await cls.get_title_from_url(message.text[entity.offset: entity.length])
        return title

    @classmethod
    async def get_title_from_url(cls, url):
        response = requests.get(url)
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        og_title_tag = soup.find('meta', property='og:title')
        if og_title_tag:
            return og_title_tag.get('content')
        else:
            return 'Untitled'

    @classmethod
    async def load_image(cls, message: types.Message):
        fullname = ''
        if message.photo:
            now = datetime.now()
            dir_name = os.path.join(DATA_DIR, message.from_user.username, now.strftime("%Y-%m"))
            file_name = now.strftime('%Y%m%d_%H%M%S_%f')
            fullname = f'{dir_name}/{file_name}.jpg'
            await message.photo[-1].download(
                destination_file=fullname,
                make_dirs=True)
        return fullname
