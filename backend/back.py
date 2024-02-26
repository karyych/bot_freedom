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


# Старт бота /start
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    markup = types.InlineKeyboardMarkup()
    
    # Кнопка "Валюта"
    currency_button = types.InlineKeyboardButton("Валюта", callback_data='currency')
    markup.add(currency_button)

    # Кнопка "Акции"
    stocks_button = types.InlineKeyboardButton("Акции", callback_data='stocks')
    markup.add(stocks_button)

    bot.send_message(chat_id, "Выберите категорию:", reply_markup=markup)
   
   


# Обработчик по условию выбора кнопки 
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    chat_id = call.message.chat.id
    if call.data == 'currency':
        send_currency_options(chat_id)
    elif call.data == 'stocks':
        send_stocks_options(chat_id)
    elif call.data.startswith('stock_'):
        stock = call.data.split('_')[1]
        handle_stock(chat_id, stock)
    elif call.data == 'back':
        start(chat_id)



# Функция для создания кнопок по валютам и кнопки в откат
def send_currency_options(chat_id):
    currencies = ['EUR', 'KZT', 'USD', 'RUB']
    markup = types.InlineKeyboardMarkup()
    # кнопка "BACK"
    back_button = types.InlineKeyboardButton("Назад", callback_data='back')
    markup.add(back_button)
    # кнопки валют
    buttons = [types.InlineKeyboardButton(currency, callback_data=f'currency_{currency}') for currency in currencies]
    markup.add(*buttons)
    bot.send_message(chat_id, "Выберите валюту:", reply_markup=markup)

#функция для отправки опций по акциям 
def send_stocks_options(chat_id):
    stocks = list(ticker_dict.keys())
    markup = types.InlineKeyboardMarkup()
    # кнопка <<back>>
    back_button = types.InlineKeyboardButton("Назад", callback_data='back')
    markup.add(back_button)
    # кнопки <<акций>>
    buttons = [types.InlineKeyboardButton(stock, callback_data=f'stock_{stock}') for stock in stocks]
    markup.add(*buttons)
    bot.send_message(chat_id, "Выберите акцию:", reply_markup=markup)

# Функция для обработки выбора валюты
def handle_currency(message, currency):
    ticker_info = get_ticker_info(currency)
    if ticker_info:
        bot.reply_to(message, ticker_info)
    else:
        bot.reply_to(message, "Тикер не найден в словаре.")


# Функция для обработки выбора акции
def handle_stock(chat_id, stock):
    ticker_info = get_ticker_info(stock)
    if ticker_info:
        bot.send_message(chat_id, ticker_info)
    else:
        bot.send_message(chat_id, "Тикер не найден в словаре.")

# Функция для получения информации о тикере
def get_ticker_info(ticker):
    if ticker in ticker_dict:
        api_url = ticker_dict[ticker]['api']
        response = send_rest_request(api_url.format(ticker_dict[ticker]['ticker']))
        if response:
            data = json.loads(response)
            # Форматирование данных по вашему усмотрению
            result = "\n".join([f"{item['c']}: {item['ltp']:.2f}" for item in data]) 
            return result
    return None 

# Функция для проверки статуса и отправки REST запроса
def send_rest_request(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except Exception as e:
        return None

# Обработчик для Inline кнопок 
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == 'back':
        send_stocks_options(call.message.chat.id)
    elif call.data.startswith('currency_'):
        currency = call.data.split('_')[1]
        handle_currency(call, currency)
    elif call.data.startswith('stocks_'):
        stock = call.data.split('_')[1]
        handle_stock(call, stock)


# Запускаем бота
bot.polling(none_stop=True)

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



