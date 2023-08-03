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
    notes = []
    json_file = None

    def __init__(self, message: types.Message):
        self.username = message.from_user.username
        self.message = message
        self.user_dir = os.path.join(DATA_DIR, self.username)
        if not os.path.exists(self.user_dir):
            os.mkdir(self.user_dir, 777)
        now = datetime.datetime.now()
        date_string = now.strftime("%Y-%m-%d")
        self.json_file = os.path.join(DATA_DIR, self.user_dir, f'{date_string}.json')

    async def process(self):
        await self.get_notes()
        await self.add_note()
        await self.save_notes()

    async def save_notes(self, ):
        # notes_dict = [note.__dict__ for note in self.notes]

        with open(self.json_file, 'w') as f:
            json.dump(self.notes, f, indent=4, ensure_ascii=False)

    async def get_notes(self):
        if os.path.exists(self.json_file):
            with open(self.json_file, 'r') as f:
                self.notes = json.load(f)
        return self.notes

    async def add_note(self):
        new_note = await Note.create_from_message(self.message)
        dict_note = new_note.__dict__
        self.notes.append(dict_note)
        return self
