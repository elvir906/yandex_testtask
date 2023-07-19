import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import (InputFile, KeyboardButton, MediaGroup, Message,
                           ReplyKeyboardMarkup)
from decouple import config

from states import NextStep
from text_messages import messages

bot = Bot(token=config('TELEGRAM_TOKEN'))
dp = Dispatcher(bot, storage=MemoryStorage())

CHAT_ID = config('CHAT_ID')


@dp.message_handler(commands=['start'])
async def start(message: Message):
    btn_names = ['Селфи', 'Фото со школы', 'Пост о моём увлечении']
    keyboard_buttons = [
        [KeyboardButton(text=btn_names[i]) for i in range(len(btn_names))]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=keyboard_buttons, resize_keyboard=True
    )
    await message.answer(
        text=messages.get('start'),
        reply_markup=keyboard,
        parse_mode='Markdown'
    )


@dp.message_handler(text=['Селфи'])
async def selfi(message: Message):
    album = MediaGroup()
    photo = InputFile("media/selphy.jpg")
    album.attach_photo(
        photo=photo,
        caption='Это мой селфи'
    )
    await message.answer_media_group(media=album)


@dp.message_handler(text=['Фото со школы'])
async def school_photo(message: Message):
    album = MediaGroup()
    photo = InputFile("media/school_photo.JPG")
    album.attach_photo(
        photo=photo,
        caption='Это моё фото со школы'
    )
    await message.answer_media_group(media=album)


@dp.message_handler(text=['Пост о моём увлечении'])
async def post_about_author(message: Message):
    await message.answer(text=messages.get('about_author'))


@dp.message_handler(commands=['sources'])
async def sources(message: Message):
    await message.answer(text=messages.get('sources'))


@dp.message_handler(commands=['about_gpt'])
async def about_gpt(message: Message):
    await bot.send_audio(
        chat_id=message.from_user.id,
        audio=InputFile("media/gpt", "r"),
        performer="Elvir",
        title="About GPT"
    )


@dp.message_handler(commands=['sql_vs_nosql'])
async def sql_vs_nosql(message: Message):
    await bot.send_audio(
        chat_id=message.from_user.id,
        audio=InputFile("media/sqlvsnosql", "r"),
        performer="Elvir",
        title="SQL vs NoSQL"
    )


@dp.message_handler(commands=['first_love'])
async def first_love(message: Message):
    await bot.send_audio(
        chat_id=message.from_user.id,
        audio=InputFile("media/firstlove", "r"),
        performer="Elvir",
        title="First love"
    )


@dp.message_handler(commands=['nextstep'])
async def next_step(message: Message):
    await message.answer(text=messages.get('next_step'))
    await NextStep.step_two.set()


@dp.message_handler(state=NextStep.step_two)
async def next_step_step_two(message: Message, state: FSMContext):
    await bot.send_message(chat_id=CHAT_ID, text=message.text)
    await message.answer(text='Ваше сообщение отправлено!')
    await state.finish()


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
