"""Finish menu button: send title to BotFather (it's waiting for it)."""
import asyncio
import os
import sys

from telethon import TelegramClient, events

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "telegram-bridge"))
from common import get_client  # noqa: E402


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

    await client.send_message(bf, "Store")
    m = await wait(25)
    print("RESULT:", ((m.message or "") if m else "(no reply)").replace("\n", " | ")[:200])
    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
