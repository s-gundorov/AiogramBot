import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import os
from googletrans import Translator
import random
import requests

from config import TOKEN, THE_CAT_API_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher()
translator = Translator()

@dp.message(Command("start"))
async def start_command(message: Message):
   await message.answer("Привет! Напиши название породы кошки, и я пришлю тебе её фото и описание.")

@dp.message()
async def send_cat_info(message: Message):
   breed_name = message.text
   breed_info = get_breed_info(breed_name)
   if breed_info:
       cat_image_url = get_cat_image_by_breed(breed_info['id'])
       translation = translator.translate(breed_info['description'], dest='ru')
#      translation = breed_info['description']
       info = (
           f"Порода: {breed_info['name']}\n"
           f"Описание: {translation.text}\n"
           f"Продолжительность жизни: {breed_info['life_span']} лет"
       )
       await message.answer_photo(photo=cat_image_url, caption=info)
   else:
       await message.answer("Такая порода не найдена. Попробуйте еще раз.")


# Получить список пород:
def get_cat_breeds():
   url = "https://api.thecatapi.com/v1/breeds"
   headers = {"x-api-key": THE_CAT_API_KEY}
   response = requests.get(url, headers=headers)
   return response.json()

def get_breed_info(breed_name):
   breeds = get_cat_breeds()
   for breed in breeds:
       if breed['name'].lower() == breed_name.lower():
           return breed
   return None

# Получить картинку кошки:
def get_cat_image_by_breed(breed_id):
    url = f"https://api.thecatapi.com/v1/images/search?breed_ids={breed_id}"
    headers = {"x-api-key": THE_CAT_API_KEY}
    response = requests.get(url, headers=headers)
    data = response.json()
    return data[0]['url']


async def main():
   await dp.start_polling(bot)

if __name__ == '__main__':
   asyncio.run(main())