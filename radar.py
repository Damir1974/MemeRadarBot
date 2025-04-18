import aiohttp

KEYWORDS = [
    "ghibli", "elon", "doge", "meme", "cat", "pepe", "shiba", "inu",
    "cz", "ai", "sol", "baby", "moon", "degen", "wizard", "banana"
]

last_seen_tokens = set()

async def scan_new_memecoins():
    url = "https://api.dexscreener.com/latest/dex/pairs"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
    pairs = data.get("pairs", [])
    found = []

    for pair in pairs:
        name = pair.get("baseToken", {}).get("name", "").lower()
        symbol = pair.get("baseToken", {}).get("symbol", "").lower()
        token_id = f"{name}{symbol}"
        if token_id in last_seen_tokens:
            continue
        if any(keyword in name or keyword in symbol for keyword in KEYWORDS):
            last_seen_tokens.add(token_id)
            url = pair.get("url", "")
            found.append(f"""Найден мемкоин:
{name.upper()} ({symbol.upper()})
{url}""")
