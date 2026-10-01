"""Enable Mini App: URL -> image -> gif -> title -> description."""
import asyncio
import os
import sys

from telethon import TelegramClient, events

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "telegram-bridge"))
from common import get_client  # noqa: E402

URL = "https://mahabaddy.github.io/ton-store-miniapp/miniapp/"
BOT_UNAME = "qubax_store_test_bot"
ICON = os.path.join(HERE, "icon.png")


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

    def show(m, label):
        if m is None:
            print(f"[{label}] (none)"); return None
        print(f"[{label}] {((m.message or '')[:90]).replace(chr(10),' | ')!r}")
        return m

    async def click(m, needle):
        for b in buttons(m):
            if needle.lower() in (b.text or "").lower():
                return await b.click()
        return None

    def has(m, *words):
        t = ((m.message or "") if m else "").lower()
        return any(w in t for w in words)

    await client.send_message(bf, "/mybots")
    menu = await wait(20)
    await click(menu, BOT_UNAME)
    botmenu = await wait(20)
    await click(botmenu, "Bot Settings")
    settings = await wait(20)
    await click(settings, "Configure Mini App")
    m = await wait(20)
    show(m, "miniapp-menu")
    for needle in ("Enable Mini App", "New", "Modify"):
        if await click(m, needle) is not None:
            print(f"  clicked {needle!r}")
            break
    m = await wait(20); show(m, "p1")
    if has(m, "url"):
        await client.send_message(bf, URL)
        m = await wait(20); show(m, "p2-image")
    if m is not None and has(m, "image", "photo", "picture"):
        await client.send_file(bf, ICON, force_document=True)
        m = await wait(25); show(m, "p3-gif")
    if m is not None and has(m, "gif", "animation"):
        await client.send_message(bf, "/empty")
        m = await wait(25); show(m, "p4-title")
    if m is not None and has(m, "title", "name"):
        await client.send_message(bf, "Qubax Store")
        m = await wait(20); show(m, "p5-desc")
    if m is not None and has(m, "description"):
        await client.send_message(bf, "TON testnet store demo")
        m = await wait(25); show(m, "p6-final")
    if m is not None and has(m, "success", "configured", "enabled"):
        print("MINI APP ENABLED ✓")
    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
