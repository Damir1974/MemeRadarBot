
import aiohttp

KEYWORDS = [
    "ghibli", "elon", "doge", "meme", "cat", "pepe", "shib", "jeo", "pump",
    "ai", "sol", "baby", "moon", "degen", "wizard", "cult", "based", "rekt"
]

last_seen_tokens = set()

async def scan_new_memecoins():
    url = "https://api.dexscreener.com/latest/dex/pairs/solana"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()

    pairs = data.get("pairs", [])
    found = []

    for pair in pairs:
        name = pair.get("baseToken", {}).get("name", "").lower()
        symbol = pair.get("baseToken", {}).get("symbol", "").lower()
        url = pair.get("url", "")

        token_id = f"{name}|{symbol}"

        if token_id in last_seen_tokens:
            continue

        if any(keyword in name or keyword in symbol for keyword in KEYWORDS):
            last_seen_tokens.add(token_id)
            found.append(f"Найден мемкоин:\n{name.upper()} ({symbol})\n{url}")

    return "\n\n".join(found) if found else None
