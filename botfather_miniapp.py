"""Configure Mini App attachment for the bot (URL -> title -> image)."""
import asyncio
import os
import sys
import urllib.request

from telethon import TelegramClient, events

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "telegram-bridge"))
from common import get_client  # noqa: E402

URL = "https://mahabaddy.github.io/ton-store-miniapp/miniapp/"
BOT_UNAME = "qubax_store_test_bot"
ICON = os.path.join(HERE, "icon.png")


async def main() -> None:
    if not os.path.exists(ICON):
        urllib.request.urlretrieve("https://ton.org/favicon.png", ICON)
        print("icon downloaded:", os.path.getsize(ICON), "bytes")

    client, _ = get_client()
    await client.start()
    bf = await client.get_entity("BotFather")
    inbox: asyncio.Queue = asyncio.Queue()
    client.add_event_handler(
        lambda e: inbox.put(e.message) if (e.message and (e.message.message or "").strip()) else None,
        events.NewMessage(chats=bf))
    client.add_event_handler(
        lambda e: inbox.put(e.message) if (e.message and (e.message.message or "").strip()) else None,
        events.MessageEdited(chats=bf))

    async def wait(timeout=15):
        try:
            return await asyncio.wait_for(inbox.get(), timeout)
        except asyncio.TimeoutError:
            return None

    def buttons(msg):
        try:
            return [b for row in (msg.buttons or []) for b in row]
        except Exception:
            return []

    def show(m, label):
        if m is None:
            print(f"[{label}] (none)"); return
        print(f"[{label}] {((m.message or '')[:80]).replace(chr(10),' | ')!r} btns={[b.text for b in buttons(m)][:6]}")

    async def click(m, needle):
        for b in buttons(m):
            if needle.lower() in (b.text or "").lower():
                return await b.click()
        return None

    await client.send_message(bf, "/mybots")
    menu = await wait(20)
    await click(menu, BOT_UNAME)
    botmenu = await wait(20)
    await click(botmenu, "Bot Settings")
    settings = await wait(20)
    await click(settings, "Configure Mini App")
    m = await wait(20); show(m, "miniapp-menu")
    # options: Modify/New — click the one that sets a web app
    nxt = None
    for needle in ("New", "Modify", "Edit"):
        nxt = await click(m, needle)
        if nxt is not None:
            print(f"  clicked {needle!r}")
            break
    m = await wait(20); show(m, "prompt1")
    txt = ((m.message or "") if m else "").lower()
    if "url" in txt:
        await client.send_message(bf, URL)
        m = await wait(20); show(m, "prompt2")
        txt = ((m.message or "") if m else "").lower()
    if "image" in txt or "photo" in txt or "gif" in txt:
        await client.send_file(bf, ICON)
        m = await wait(25); show(m, "prompt3")
        txt = ((m.message or "") if m else "").lower()
    # title / inline greeting prompts may follow; answer title
    if "title" in txt or "name" in txt:
        await client.send_message(bf, "Qubax Store")
        m = await wait(20); show(m, "prompt4")
        txt = ((m.message or "") if m else "").lower()
    if m is not None and "description" in txt:
        await client.send_message(bf, "TON testnet store demo")
        m = await wait(20); show(m, "prompt5")
        txt = ((m.message or "") if m else "").lower()
    if m is not None and ("success" in txt or "configured" in txt):
        print("MINI APP CONFIGURED ✓")
    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
