import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from gtts import gTTS
import os
from googletrans import Translator
import keyboard as kb
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import Message, FSInputFile, CallbackQuery


from config import TOKEN
import random

bot = Bot(token=TOKEN)
dp = Dispatcher()
translator = Translator()

@dp.message(CommandStart())
async def start(message: Message):
#   await message.answer(f'Привет, {message.from_user.first_name}', reply_markup=kb.inline_keyboard_test)
#   await message.answer(f'Привет, {message.from_user.first_name}', reply_markup=await kb.test_keyboard())
    await message.answer(f'Привет, {message.from_user.first_name} !', reply_markup=kb.inline_keyboard_test)

@dp.callback_query(F.data == 'news')
async def news(callback: CallbackQuery):
    await callback.answer("Новости подгружаются", show_alert=True)
#   await callback.message.answer('Вот свежие новости!')
    await callback.message.edit_text('Вот еще новости!', reply_markup=await kb.test_keyboard())

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer("Этот бот умеет выполнять команды:\n/start \n/help")

@dp.message(F.text == "что такое ИИ?")
async def aitext(message: Message):
    await message.answer('Искусственный интеллект — это свойство искусственных интеллектуальных систем выполнять творческие функции, которые традиционно считаются прерогативой человека; наука и технология создания интеллектуальных машин, особенно интеллектуальных компьютерных программ')

@dp.message(F.photo)
async def react_photo(message: Message):
#    await message.answer('Спасибо за фото!')
    list = ['Ого, какая фотка!', 'Непонятно, что это такое', 'Спасибо за фото!']
    rand_answ = random.choice(list)
    await message.answer(rand_answ)
    await bot.download(message.photo[-1],destination=f'tmp/{message.photo[-1].file_id}.jpg')

@dp.message(Command('photo'))
async def photo(message: Message):
    photos = ['https://pisoft.ru/images/disc_ps6.jpg', 'https://pisoft.ru/images/aprok/aprok_cd_sm.png', 'https://pisoft.ru/images/prok/prokat_cd10_sm.png']
    rand_photo = random.choice(photos)
#    random_photo = random.choice(photos)
    await message.answer_photo(photo=rand_photo, caption='Это супер крутая картинка')

@dp.message(Command('video'))
async def video(message: Message):
    await bot.send_chat_action(message.chat.id, 'upload_video')
    video = FSInputFile('test.mp4')
    await bot.send_video(message.chat.id, video)

@dp.message(Command('audio'))
async def audio(message: Message):
    audio = FSInputFile('sound.mp3')
    await bot.send_audio(message.chat.id, audio)

# Озвучка текста:
@dp.message(Command('training'))
async def training(message: Message):
   training_list = [
       "Тренировка 1:\n1. Скручивания: 3 подхода по 15 повторений\n2. Велосипед: 3 подхода по 20 повторений (каждая сторона)\n3. Планка: 3 подхода по 30 секунд",
       "Тренировка 2:\n1. Подъемы ног: 3 подхода по 15 повторений\n2. Русский твист: 3 подхода по 20 повторений (каждая сторона)\n3. Планка с поднятой ногой: 3 подхода по 20 секунд (каждая нога)",
       "Тренировка 3:\n1. Скручивания с поднятыми ногами: 3 подхода по 15 повторений\n2. Горизонтальные ножницы: 3 подхода по 20 повторений\n3. Боковая планка: 3 подхода по 20 секунд (каждая сторона)"
   ]
   rand_tr = random.choice(training_list)
   await message.answer(f"Это ваша мини-тренировка на сегодня\n {rand_tr}")

   tts = gTTS(text=rand_tr, lang='ru')
   tts.save("training.ogg")
   audio = FSInputFile('training.ogg')
   await bot.send_voice(chat_id=message.chat.id, voice=audio)
   os.remove("training.ogg")

# Озвучка аудио-сообщения:
@dp.message(Command('voice'))
async def voice(message: Message):
    voice = FSInputFile("sample.ogg")
    await message.answer_voice(voice)

# Отправка документа:
@dp.message(Command('doc'))
async def doc(message: Message):
	doc = FSInputFile("ProkatDat1_1.txt")
	await bot.send_document(message.chat.id, doc)

# Реакция на ключевую фразу:
async def start(message: Message):
    if (message.text.lower() == 'test' or message.text.lower() == 'тест'):
        await message.answer('Тестируем')

# Эхо:
#@dp.message()
#async def start(message: Message):
#    await message.send_copy(chat_id=message.chat.id)

@dp.message()
async def translate_message(message: Message):
    if message.text:
        translation = translator.translate(message.text, dest='ru')
        await message.answer(translation.text)

async def test_keyboard():
    keyboard = InlineKeyboardBuilder()
    for key in test:
        keyboard.add(KeyboardButton(text=key))
    return keyboard.adjust(2).as_markup()


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
