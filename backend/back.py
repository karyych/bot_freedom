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

def send_curr_options(chat_id):
    currencies = list(ticker_dict.keys())
    markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    buttons = [types.KeyboardButton(currency[:5]) for currency in currencies]
    markup.add(*buttons)
    bot.send_message(chat_id, "Выберите валюту:", reply_markup=markup)



# /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    send_curr_options(message.chat.id)
    bot.reply_to(message, "Привет! Выберите валюту:")

# Обработчик текстовых сообщений
# Далее надо будет сделат кнопку валюты и выбор валют, а такая реализация канает на акции но нужен будет словарь, 
# т.к. например CVX.US вводить не удобно, хочется вводить CVX, cvx, Chevron
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_input = message.text.lower()
    
    if user_input == 'запрос': 
        bot.send_message(message.chat.id, "Введите тикер:")
        bot.register_next_step_handler(message, handle_ticker)
    elif user_input in ticker_dict:
        currency_ticker = ticker_dict[user_input]
        # Здесь могут быть дополнительные действия, связанные с выбранной валютой
        bot.reply_to(message, f"Выбран тикер {currency_ticker}.")
    else:
        bot.reply_to(message, "Я не понимаю, что вы имеете в виду.")

def handle_ticker(message):
    ticker = message.text.upper()
    # Здесь могут быть дополнительные действия с введенным тикером
    bot.reply_to(message, f"Введен тикер: {ticker}.")


"""
# Функция, добавляющая название тикера в строку REST запроса
def handle_ticker(message):
    ticker = message.text.upper() # Может и не надо, надо чекать 
    response = send_rest_request(REST_API_URL.format(ticker))
    if response:
        data = json.loads(response)
        # Сюда надо выводить больше инфы (для этого добавляем параметры в API_REST_URL +bbp +ttp) 
        bot.reply_to(message, result)
        result = "\n".join([f"{item['c']}: {item['ltp']:.2f}" for item in data]) 
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
"""
# Запускаем бота
bot.polling()
