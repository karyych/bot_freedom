import telebot
import requests
import json

# Токен
TOKEN = '6738973994:AAEucnyuxwgdbSQWGsIqpkyUXqW5r-aMai0'

# Создаем экземпляр бота
bot = telebot.TeleBot(TOKEN)

# после params можно тоже вделать форматирование {}, т.к. bbp отвечает только за текущую цену
REST_API_URL = 'https://tradernet.kz/securities/export?params=bbp&tickers={}'


# /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот. Как дела?")


# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text.lower() == 'запрос': # Далее надо будет сделат кнопку валюты и выбор валют, а такая реализация канает на акции
        bot.send_message(message.chat.id, "Введите тикер:")
        bot.register_next_step_handler(message, handle_ticker)
    else:
        bot.reply_to(message, "Я не понимаю, что вы имеете в виду.")


# Функция, добавляющая название тикера в строку REST запроса
def handle_ticker(message):
    ticker = message.text.upper() # Может и не надо, надо чекать 
    response = send_rest_request(REST_API_URL.format(ticker))
    if response:
        data = json.loads(response)
        result = "\n".join([f"{item['c']}: {item['bbp']:.2f}" for item in data])
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
