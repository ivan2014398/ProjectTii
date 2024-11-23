from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import asyncio, logging
from tts import text_to_audio
from dotenv import load_dotenv
import os

load_dotenv()

logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher(bot=bot)

start_kb = InlineKeyboardBuilder(markup=[
    [InlineKeyboardButton(text='Речь в текст', callback_data='SR')],
    [InlineKeyboardButton(text='Текст в речь', callback_data='TTS')]
])
# builder = InlineKeyboardBuilder(markup=start_kb)

class FSMTTS(StatesGroup):
    type_text = State()

@dp.message(CommandStart)
async def start(message: types.Message):
    await message.answer('Привет!\n\nЯ бот, который умеет переводить речь в текст и наоборот.', reply_markup=start_kb.as_markup())


@dp.callback_query(lambda c: c.data=='TTS')
async def text_to_speech_button(callback: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback.from_user.id, 'Напиши текст')
    await state.set_state(FSMTTS.type_text)


@dp.message(FSMTTS.type_text)
async def gettin_text(message: types.Message, state: FSMContext):
    text = message.text
    audio, lang = text_to_audio(text)
    voiceFile = InputFile('output_audio.mp3')
    await bot.send_voice(message.from_user.id, voice=voiceFile, caption="hey")
    await state.clear()
    


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())