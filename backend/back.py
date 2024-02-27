import telebot
import requests
import json
from dotenv import load_dotenv
import os
from tickers_dict import ticker_dict
from telebot import types

# Загрузка токена из переменных среды
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Создание экземпляра бота
bot = telebot.TeleBot(TOKEN)



# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    markup = types.InlineKeyboardMarkup()
    
    # Добавление кнопки "Валюта"
    currency_button = types.InlineKeyboardButton("Валюта", callback_data='currency')
    markup.add(currency_button)

    # Добавление кнопки "Акции"
    stocks_button = types.InlineKeyboardButton("Акции", callback_data='stocks')
    markup.add(stocks_button)

    bot.send_message(chat_id, "Выберите категорию:", reply_markup=markup)

# Обработчик callback-запросов
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    chat_id = call.message.chat.id
    query = call.data
    
    if query == 'currency':
        send_currency_options(chat_id)
    elif query == 'stocks':
        send_stocks_options(chat_id)
    elif query.startswith('stock_'):
        handle_stock(chat_id, query.split('_')[1])
    elif query.startswith('currency_'):
        handle_currency(chat_id, query.split('_')[1])
    elif query == 'back':
        start(call.message)

# Функция для отправки кнопок с валютами
def send_currency_options(chat_id):
    currencies = ['EUR', 'KZT', 'USD', 'RUB']
    markup = types.InlineKeyboardMarkup()
    
    # Добавление кнопки "Назад"
    back_button = types.InlineKeyboardButton("Назад", callback_data='back')
    markup.add(back_button)
    
    # Добавление кнопок валют
    buttons = [types.InlineKeyboardButton(currency, callback_data=f'currency_{currency}') for currency in currencies]
    markup.add(*buttons)
    
    bot.send_message(chat_id, "Выберите валюту:", reply_markup=markup)

# Функция для отправки кнопок с акциями
def send_stocks_options(chat_id):
    stocks = list(ticker_dict.keys())
    markup = types.InlineKeyboardMarkup()
    
    # Добавление кнопки "Назад"
    back_button = types.InlineKeyboardButton("Назад", callback_data='back')
    markup.add(back_button)
    
    # Добавление кнопок акций
    buttons = [types.InlineKeyboardButton(stock, callback_data=f'stock_{stock}') for stock in stocks]
    markup.add(*buttons)
    
    bot.send_message(chat_id, "Выберите акцию:", reply_markup=markup)

# Функция для обработки выбора валюты
def handle_currency(chat_id, currency):
    ticker_info = get_ticker_info(currency)
    if ticker_info:
        bot.send_message(chat_id, ticker_info)
    else:
        bot.send_message(chat_id, "Тикер не найден в словаре.")

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
            # Форматирование данных
            result = "\n".join([f"{item['c']}: {item['ltp']:.2f}" for item in data])
            return result
    return None 

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

# Запуск бота
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



