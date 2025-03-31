import requests

def fetch_memecoins():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {"vs_currency": "usd", "category": "memes", "order": "market_cap_desc", "per_page": 10}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    return []

def format_memecoin_list(coins):
    if not coins:
        return "Не удалось получить список мемкоинов."
    message = "🔥 Топ мемкоинов:

"
    for coin in coins:
        message += f"{coin['name']} ({coin['symbol'].upper()}): ${coin['current_price']}
"
    return message