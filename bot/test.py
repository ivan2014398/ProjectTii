from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from gtts import gTTS
import os

# Замените на ваш токен
TOKEN = '6263842022:AAErfWvrrJ2q1g0eEsypTUnv4b4ph5j-KQs'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['voice'])
async def send_voice_message(message: types.Message):
    text = "Пример текста для преобразования в голос"
    # Создаем аудио с использованием gTTS и сохраняем во временный файл
    tts = gTTS(text=text, lang='ru')
    tts.save("output_audio.ogg")
    
    # Отправляем аудиофайл как голосовое сообщение
    with open("output_audio.ogg", "rb") as audio:
        await bot.send_voice(chat_id=message.chat.id, voice=audio, caption="Вот ваше голосовое сообщение!")
    
    # Удаляем временный файл после отправки
    os.remove("output_audio.ogg")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
