import telebot
import requests
import json
from dotenv import load_dotenv
import os
from tickers_dict import ticker_dict
from telebot import types

# Токен
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Создаем экземпляр бота
bot = telebot.TeleBot(TOKEN)

# после params можно тоже делать форматирование {}, т.к. bbp отвечает только за текущую цену
REST_API_URL = 'https://tradernet.kz/securities/export?params=ltp&tickers={}'

# /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    send_curr_options(message.chat.id)
    bot.reply_to(message, "Привет! Выберите валюту:")



def send_curr_options(chat_id):
    currencies = list(ticker_dict.keys())
    markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    buttons = [types.KeyboardButton(currency[:5]) for currency in currencies]
    markup.add(*buttons)
    bot.send_message(chat_id, "Выберите валюту:", reply_markup=markup)


# Обработчик текстовых сообщений
# Далее надо будет сделат кнопку валюты и выбор валют, а такая реализация канает на акции но нужен будет словарь, 
# т.к. например CVX.US вводить не удобно, хочется вводить CVX, cvx, Chevron
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_input = message.text.lower()
    if user_input == 'запрос':
        bot.send_message(message.chat.id, "Введите тикер:")
        user_input_tic = message.text.upper()
        handle_ticker(message, user_input_tic)
    else:
        bot.reply_to(message, "Я не понимаю, что вы имеете в виду.")


# Функция, добавляющая название тикера в строку REST запроса
def handle_ticker(message, ticker):
    response = send_rest_request(REST_API_URL.format(ticker_dict[ticker]))
    if response:
        data = json.loads(response)
        # Сюда надо выводить больше инфы (для этого добавляем параметры в API_REST_URL +bbp +ttp) 
        result = "\n".join([f"{item['c']}: {item['ltp']:.2f}" for item in data]) 
        bot.reply_to(message, result)
    else:
        bot.reply_to(message, "Ошибка при выполнении запроса.")


# Функция для отправки REST запроса
def send_rest_request(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except Exception as e:
        return None

# Запускаем бота
bot.polling()
