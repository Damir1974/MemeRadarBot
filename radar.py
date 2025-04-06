import requests

def check_new_memecoins():
    try:
        response = requests.get('https://api.coingecko.com/api/v3/coins/list', timeout=10)
        if response.status_code != 200:
            return "CoinGecko API недоступен."

        data = response.json()
        memes = [coin['name'] for coin in data if 'meme' in coin['name'].lower()]
        if memes:
            return "Найдено мемкоинов: " + ", ".join(memes[:10])
        else:
            return "Мемкоины не найдены."
    except Exception as e:
        return f"Ошибка: {str(e)}"
