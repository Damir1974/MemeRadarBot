import aiohttp

KEYWORDS = [
    "ghibli", "elon", "doge", "meme", "cat", "pepe", "shiba", "inu", "cz",
    "banana", "ai", "sol", "baby", "moon", "degen", "wizard", "frog"
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
        name = pair.get("baseToken", {}).get("name", "")
        symbol = pair.get("baseToken", {}).get("symbol", "")
        url = pair.get("url", "")
        token_id = f"{name}{symbol}"

        if token_id in last_seen_tokens:
            continue

        if any(keyword in name.lower() or keyword in symbol.lower() for keyword in KEYWORDS):
            last_seen_tokens.add(token_id)
            found.append(f"Найден мемкоин:\n{name.upper()} ({symbol})\n{url}")

    return "\n\n".join(found)
