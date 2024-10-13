import requests
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from translate import Translator

API_bot = "7520814526:AAHMs-Nue9wFTQ9HKxjLv1Ke7AuqcQDDG_I"
API_key = '6a52cb4ca030efcef8f113b0d34c7d21'

bot = Bot(token=API_bot)
dp = Dispatcher(bot, storage=MemoryStorage())


start_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Узнать погоду')],
    ], resize_keyboard=True
)

@dp.message_handler(commands=['start'])
async def srarter(message):
    await message.answer("Рады Вас видеть", reply_markup=start_menu)


@dp.message_handler(text='Узнать погоду')
async def inform(message):
    await message.answer("Скажи мне название города, чтобы узнать текущую погоду.")

@dp.message_handler(content_types=['text'])
async def inform_weather_message(message):
    city_name = message.text
    url = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_key}", timeout=1240
        )
    weather_data = url.json()
    temp = round((weather_data['main']['temp']-273.15), 2)
    description = weather_data['weather'][0]['description']
    translator = Translator(from_lang='English', to_lang='Russian')
    description_tr = translator.translate(description)
    if temp is not None:
        await message.answer(f"Сейчас в городе {city_name}: {description_tr}. Температура: {temp} °C")
    else:
        await message.answer("Не удалось найти данные о погоде для этого города. Попробуйте другой.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)