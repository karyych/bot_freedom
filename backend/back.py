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
#REST_API_URL = 'https://tradernet.kz/securities/export?params=ltp&tickers={}'

# /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    
    # Кнопка "Валюта"
    currency_button = types.InlineKeyboardButton("Валюта", callback_data='currency')
    markup.add(currency_button)

    # Кнопка "Акции"
    stocks_button = types.InlineKeyboardButton("Акции", callback_data='stocks')
    markup.add(stocks_button)

    bot.send_message(message.chat.id, "Выберите категорию:", reply_markup=markup)


#обработчик на условие при выборе кнопки
@bot.message_handler(func=lambda call: True)
def handle_message(call):
    if call.data == 'currency':
        send_currency_options(call.message.chat.id)
    elif call.data == 'stocks':
        send_stocks_options(call.message.chat.id)
    elif call.data == 'back':
        start(call.message)
  
def send_currency_options(chat_id):
    currencies = ['EUR', 'KZT', 'USD', 'RUB']
    markup = types.InlineKeyboardMarkup()
    #кнопка "BACK"
    back_button = types.InlineKeyboardButton("назад", callback_data='back')
    markup.add(back_button)
    #кнопки валют 
    buttons = [types.InlineKeyboardButton(currency, callback_data=currency) for currency in currencies]
    markup.add(*buttons)
    bot.send_message(chat_id, "Выберите валюту:", reply_markup=markup)

#функция для отправки опций по акциям 
def send_stocks_options(chat_id):
    currencies = list(ticker_dict.keys())
    markup = types.ReplyKeyboardMarkup()
    #кнопка <<back>>
    back_button = types.InlineKeyboardButton("Назад", callback_data='back')
    markup.add(back_button)
    #кнопки <<акций>>
    buttons = [types.InlineKeyboardButton(currency, callback_data=currency) for currency in currencies]
    markup.add(*buttons)
    bot.send_message(chat_id, "Выберите акцию:", reply_markup=markup)




@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == 'back':
        if call.data == 'currency':
            send_currency_options(call.message.chat.id)
        elif call.data == 'stocks':
            send_stocks_options(call.message.chat.id)



"""
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
"""
"""
@bot.message_handler(func=lambda message: message.text.isalpha())
def handle_ticker_input(message):
    user_input_tic = message.text
    ticker_info = ticker_dict.get(user_input_tic)
    if ticker_info:
        handle_ticker(message, ticker_info)
    else:
        bot.send_message(message.chat.id, "Тикер не найден в словаре.")
"""
"""
# Функция, добавляющая название тикера в строку REST запроса
def handle_ticker(message, ticker):
    response = send_rest_request(REST_API_URL.format(ticker_info['ticker']))
    if response:
        data = json.loads(response)
        # Сюда надо выводить больше инфы (для этого добавляем параметры в API_REST_URL +bbp +ttp) 
        result = "\n".join([f"{item['c']}: {item['ltp']:.2f}" for item in data]) 
        bot.reply_to(message, result)
    else:
        bot.reply_to(message, "Ошибка при выполнении запроса.")
""" 
"""
def handle_ticker(message, ticker_info):
    response = send_rest_request(ticker_info['api'].format(ticker_info['ticker'].upper()))
    if response:
        data = json.loads(response)
        result = "\n".join([f"{item['c']}: {item['ltp']:.2f}" for item in data])
        bot.reply_to(message, result)
    else:
        bot.reply_to(message, "Ошибка при выполнении запроса.")
"""
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
