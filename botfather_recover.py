"""Recover @qubax_store_test_bot token + set Menu Button. Edit-aware BotFather driver."""
import asyncio
import json
import os
import re
import sys

from telethon import TelegramClient, events

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "telegram-bridge"))
from common import get_client  # noqa: E402

OUT = os.path.join(HERE, "bot_credentials.json")
URL = open(os.path.join(HERE, "miniapp_url.txt"), encoding="utf-8").read().strip()
BOT_UNAME = "qubax_store_test_bot"
TOKEN_RE = re.compile(r"\b(\d{8,12}:[A-Za-z0-9_-]{30,})\b")


async def main() -> None:
    client, _ = get_client()
    await client.start()
    print("logged in:", (await client.get_me()).username)

    bf = await client.get_entity("BotFather")
    inbox: asyncio.Queue = asyncio.Queue()

    def push(msg):
        inbox.put_nowait(("msg", msg))

    client.add_event_handler(lambda e: push(e.message), events.NewMessage(chats=bf))
    client.add_event_handler(lambda e: push(e.message), events.MessageEdited(chats=bf))

    async def wait(timeout=20):
        try:
            kind, msg = await asyncio.wait_for(inbox.get(), timeout)
            return msg
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
                ans = await b.click()
                return ans, True
        return None, False

    async def wait_text_or_edit(needles=(), timeout=20):
        """Wait for next message/edit; return first non-empty text (or None)."""
        end = asyncio.get_event_loop().time() + timeout
        while asyncio.get_event_loop().time() < end:
            m = await wait(timeout=max(1, int(end - asyncio.get_event_loop().time())))
            if m is None:
                return None
            txt = (m.message or "").strip()
            if txt:
                for n in needles:
                    if n.lower() in txt.lower():
                        return m
                return m
        return None

    # ---- 1. token ----
    await client.send_message(bf, "/mybots")
    menu = await wait_text_or_edit(["choose", "bot"], 25)
    if menu is None or not buttons(menu):
        print("FAIL: no /mybots menu"); sys.exit(1)

    _, ok = await click(menu, BOT_UNAME)
    if not ok:
        print("FAIL: bot button not found"); sys.exit(1)
    botmenu = await wait_text_or_edit(["API Token", "Edit Bot"], 25)
    if botmenu is None:
        print("FAIL: no bot menu"); sys.exit(1)

    ans, ok = await click(botmenu, "API Token")
    token = None
    if ans is not None and getattr(ans, "message", None):
        m = TOKEN_RE.search(ans.message)
        if m:
            token = m.group(1)
    # token arrives as edit/new message
    for _ in range(6):
        m = await wait(8)
        if m is None:
            break
        txt = (m.message or "")
        mm = TOKEN_RE.search(txt)
        if mm:
            token = mm.group(1)
            break
        # if we accidentally see the bot menu again, re-click API Token
        if "API Token" in txt and buttons(m):
            a2, ok2 = await click(m, "API Token")
            if a2 is not None and getattr(a2, "message", None):
                mm2 = TOKEN_RE.search(a2.message)
                if mm2:
                    token = mm2.group(1)
                    break
    if not token:
        print("FAIL: token never captured"); sys.exit(2)

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump({"created": True, "username": BOT_UNAME, "token": token}, f, indent=2)
    print("TOKEN CAPTURED -> bot_credentials.json")

    # ---- 2. menu button ----
    await client.send_message(bf, "/mybots")
    menu = await wait_text_or_edit(["choose", "bot"], 25)
    _, ok = await click(menu, BOT_UNAME)
    botmenu = await wait_text_or_edit(["API Token", "Edit Bot"], 25)
    _, ok = await click(botmenu, "Bot Settings")
    settings = await wait_text_or_edit(["Menu Button", "Description"], 25)
    if settings is None:
        print("FAIL: no settings menu"); sys.exit(3)
    _, ok = await click(settings, "Menu Button")
    mb = await wait_text_or_edit(["menu button", "URL"], 25)
    print("menu-button menu:", (mb.message or "")[:100].replace("\n", " | ") if mb else "(none)")
    # flow: "Configure menu button" -> "Send me the URL"
    _, ok = await click(mb, "Configure") if mb else (None, False)
    prompt = await wait_text_or_edit(["URL", "http"], 25)
    print("url prompt:", (prompt.message or "")[:100].replace("\n", " | ") if prompt else "(none)")
    await client.send_message(bf, URL)
    confirm = await wait_text_or_edit(["success", "removed", "invalid", "error"], 25)
    print("MENU BUTTON RESULT:", (confirm.message or "")[:200].replace("\n", " | ") if confirm else "(no confirm)")

    await client.disconnect()
    print("DONE")


if __name__ == "__main__":
    asyncio.run(main())
