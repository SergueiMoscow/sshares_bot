import datetime
import json
import os

from Note import Note
from config import DATA_DIR
from aiogram import types


class Shares:
    message = None
    username = None
    user_dir = None
    items = []
    item_type = None
    json_file = None

    def __init__(self, message: types.Message):
        self.username = message.from_user.username
        self.message = message
        self.user_dir = os.path.join(DATA_DIR, self.username)
        if not os.path.exists(self.user_dir):
            os.mkdir(self.user_dir, 777)

    async def get_item_type(self):
        new_item = await Note.create_from_message(self.message)
        now = datetime.datetime.now()
        date_string = now.strftime("%Y-%m-%d")

        if new_item.image != '':
            self.item_type = 'img'
        elif self.message.entities:
            self.item_type = 'url'
        else:
            self.item_type = 'unknown'
            return self.item_type
        self.json_file = os.path.join(DATA_DIR, self.user_dir, f'{date_string}_{self.item_type}.json')
        return self.item_type

    async def process(self):
        if await self.get_item_type() == 'unknown':
            return 'unknown'
        await self.get_items()
        await self.add_item()
        await self.save_items()
        return self.item_type

    async def get_items(self):
        if os.path.exists(self.json_file):
            with open(self.json_file, 'r') as f:
                self.items = json.load(f)
        return self.items

    async def add_item(self):
        new_note = await Note.create_from_message(self.message)
        dict_note = new_note.__dict__
        self.items.append(dict_note)
        return self

    async def save_items(self, ):
        # notes_dict = [note.__dict__ for note in self.items]

        with open(self.json_file, 'w') as f:
            json.dump(self.items, f, indent=4, ensure_ascii=False)

