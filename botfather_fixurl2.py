"""Menu button fix v2: print actual buttons, click the URL-related one."""
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
        texts = [b.text for b in buttons(m)]
        print(f"[{label}] text={((m.message or '')[:70]).replace(chr(10),' | ')!r} btns={texts}")

    async def click(m, needle):
        for b in buttons(m):
            if needle.lower() in (b.text or "").lower():
                return await b.click()
        print(f"  !! no button matching {needle!r}")
        return None

    await client.send_message(bf, "/mybots")
    menu = await wait(20); show(menu, "mybots")
    await click(menu, BOT_UNAME)
    botmenu = await wait(20); show(botmenu, "botmenu")
    await click(botmenu, "Bot Settings")
    settings = await wait(20); show(settings, "settings")
    await click(settings, "Menu Button")
    mb = await wait(20); show(mb, "menu-button")

    # click anything URL-ish
    clicked = None
    for needle in ("Configure menu button", "Edit menu button", "URL", "Change"):
        clicked = await click(mb, needle)
        if clicked is not None:
            print(f"  clicked {needle!r}")
            break
    prompt = await wait(20); show(prompt, "prompt")
    if prompt and "URL" in (prompt.message or ""):
        await client.send_message(bf, URL)
        m1 = await wait(20); show(m1, "after-url")
        if m1 and "title" in (m1.message or "").lower():
            await client.send_message(bf, "Store")
            m2 = await wait(20); show(m2, "after-title")
    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
