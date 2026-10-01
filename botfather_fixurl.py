"""Update menu button URL to /miniapp/ (the real app path)."""
import asyncio
import os
import sys

from telethon import TelegramClient, events

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "telegram-bridge"))
from common import get_client  # noqa: E402

URL = "https://mahabaddy.github.io/ton-store-miniapp/miniapp/"
BOT_UNAME = "qubax_store_test_bot"


async def main() -> None:
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

    async def wait(timeout=20):
        try:
            return await asyncio.wait_for(inbox.get(), timeout)
        except asyncio.TimeoutError:
            return None

    def buttons(msg):
        try:
            return [b for row in (msg.buttons or []) for b in row]
        except Exception:
            return []

    async def click(msg, needle):
        for b in buttons(msg):
            if needle.lower() in (b.text or "").lower():
                return await b.click(), True
        return None, False

    await client.send_message(bf, "/mybots")
    menu = await wait(25)
    _, ok = await click(menu, BOT_UNAME)
    botmenu = await wait(25)
    _, ok = await click(botmenu, "Bot Settings")
    settings = await wait(25)
    _, ok = await click(settings, "Menu Button")
    mb = await wait(25)
    _, ok = await click(mb, "Configure")
    prompt = await wait(25)
    print("url prompt ok:", bool(prompt))
    await client.send_message(bf, URL)
    m1 = await wait(25)
    print("after URL:", ((m1.message or "") if m1 else "(none)").replace("\n", " | ")[:120])
    await client.send_message(bf, "Store")
    m2 = await wait(25)
    print("FINAL:", ((m2.message or "") if m2 else "(none)").replace("\n", " | ")[:200])
    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
