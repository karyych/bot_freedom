#Словарь для тикеров 

# Курсы валют >> https://tradernet.kz/securities/export?params=ltp&tickers=EUR/KZT вывод по паре 
# Курсы валют >> https://tradernet.kz/securities/export?params=ltp&tickers=RUB/KZT вывод по паре 

# URL для API запросов
REST_API_URL = 'https://tradernet.kz/securities/export?params=ltp&tickers={}'

ticker_dict = {
    # Вывод Великолепной Семёрки
    'Nvidia': {'ticker': 'NVDA.US'},
    'Microsoft': {'ticker': 'MSFT.US'},
    'Apple': {'ticker': 'AAPL.US'},
    'Alphabet': {'ticker': 'GOOGL.US'}, 
    'Amazon': {'ticker': 'AMZN.US'},
    'Meta': {'ticker': 'META.US'},
    'Tesla': {'ticker': 'TSLA.US'},

    # Остальные акции
    'Chevron': {'ticker': 'CVX.US'}, 


    # Валюты
    'USD/KZT': {'ticker': 'USD/KZT'},
    'EUR/KZT': {'ticker': 'EUR/KZT'},
    'USD/RUR': {'ticker': 'USD/RUR'},
    'EUR/RUR': {'ticker': 'EUR/RUR'},
    'RUR/KZT': {'ticker': 'RUR/KZT'},

    
}