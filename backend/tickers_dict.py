#Словарь для тикеров 

# Курсы валют >> https://tradernet.kz/securities/export?params=ltp&tickers=EUR/KZT вывод по паре 
# Курсы валют >> https://tradernet.kz/securities/export?params=ltp&tickers=RUB/KZT вывод по паре 

# URL для API запросов
REST_API_URL = 'https://tradernet.kz/securities/export?params=ltp&tickers={}'

ticker_dict = {
    'Nvidia': {'ticker': 'NVDA.US'},
    'Microsoft': {'ticker': 'MSFT.US'},
    'Apple': {'ticker': 'AAPL.US'},
    'Alphabet': {'ticker': 'GOOGL.US'}, 
    'Amazon': {'ticker': 'AMZN.US'},
    'Meta': {'ticker': 'META.US'},
    'Tesla': {'ticker': 'TSLA.US'},

    'Chevron': {'ticker': 'CVX.US'}, 
    'USD/KZT': {'ticker': 'USD/KZT'},

    
}