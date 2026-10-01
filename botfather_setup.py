"""One-shot: create bot via BotFather (using the existing SunLightLord session),
set menu button -> Mini App, save bot username/token to bot_credentials.json.

Single client hold: run ONLY while the bridge listener is stopped (it is).
"""
import asyncio
import json
import os
import sys

from telethon import TelegramClient, events

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))  # telegram-bridge root for common.py
from common import get_client  # noqa: E402

OUT = os.path.join(HERE, "bot_credentials.json")


async def main() -> None:
    client, _ = get_client()
    await client.start()  # session already authorized; no prompts expected

    me = await client.get_me()
    print(f"logged in as: {me.first_name} (@{me.username}) id={me.id}")

    botfather = 93372553
    result = {"created": False}

    @client.on(events.NewMessage(chats=botfather, incoming=True))
    async def handler(event):
        text = event.message.message or ""
        result["last"] = text
        result["event"].set()

    async def wait_reply(timeout=30):
        result["event"] = asyncio.Event()
        try:
            await asyncio.wait_for(result["event"].wait(), timeout)
            return result.get("last", "")
        except asyncio.TimeoutError:
            return ""

    await client.send_message(botfather, "/mybots")
    r = await wait_reply()
    print("BF:", (r or "(timeout)").replace("\n", " | ")[:200])

    if "Create a new bot" not in r and "new bot" not in r.lower():
        print("unexpected reply; aborting")
        await client.disconnect()
        sys.exit(1)

    await client.send_message(botfather, "/newbot")
    r = await wait_reply()
    print("BF:", (r or "(timeout)").replace("\n", " | ")[:160])

    await client.send_message(botfather, "Qubax Store Test")
    r = await wait_reply()
    print("BF:", (r or "(timeout)").replace("\n", " | ")[:160])

    username = "qubax_store_test_bot"
    await client.send_message(botfather, username)
    r = await wait_reply()
    print("BF:", (r or "(timeout)").replace("\n", " | ")[:400])

    if "t.me/" in r and "token" in r.lower() or "HTTP API token" in r:
        import re
        m = re.search(r"\b(\d{8,12}:[A-Za-z0-9_-]{30,})\b", r)
        if m:
            result.update({"created": True, "username": username, "token": m.group(1)})
            with open(OUT, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2)
            print("BOT CREATED:", username)
            print("token saved to bot_credentials.json (NOT printed)")

            # Menu button -> Mini App (needs the hosted URL; set after Pages is up)
            with open(os.path.join(os.path.dirname(HERE), "miniapp_url.txt"), encoding="utf-8") as f:
                url = f.read().strip()
            await client.send_message(botfather, "/mybots")
            await wait_reply()
            await client.send_message(botfather, f"@{username}")
            await wait_reply()
            await client.send_message(botfather, "Bot Settings")
            await wait_reply()
            await client.send_message(botfather, "Menu Button")
            await wait_reply()
            await client.send_message(botfather, "Configure menu button")
            await wait_reply()
            await client.send_message(botfather, "Send Web App URL")
            await wait_reply()
            await client.send_message(botfather, url)
            r = await wait_reply()
            print("MENU BUTTON:", (r or "(timeout)").replace("\n", " | ")[:200])
        else:
            print("token regex failed")
    else:
        print("creation failed — check output above")

    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
