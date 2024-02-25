import telebot

TOKEN = '6738973994:AAEucnyuxwgdbSQWGsIqpkyUXqW5r-aMai0'

# Экземпляр бота
bot = telebot.TeleBot(TOKEN)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот. Как дела?")

# Всё остальное просто возвращаем обратно
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

# Запуск
bot.polling()
