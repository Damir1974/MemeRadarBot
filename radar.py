import requests

def check_new_memecoins():
    try:
        response = requests.get('https://api.coingecko.com/api/v3/coins/list')
        data = response.json()
        memes = [coin['name'] for coin in data if 'meme' in coin['name'].lower()]
        if memes:
            return "Найдено мемкоинов: " + ", ".join(memes[:10])
        else:
            return "Мемкоины не найдены."
    except:
        return "Ошибка при получении данных."