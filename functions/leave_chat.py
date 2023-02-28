from pyrogram import Client

import asyncio

from rich.console import Console, Theme

from settings.config import color_number
from settings.function import SettingsFunction

console = Console(theme=Theme({"repr.number": color_number}))

class Leavechat(SettingsFunction):
    """Leave the chat"""

    def __init__(self, sessions):
        if console.input("[bold red]are you sure? (y/n): ") == "y":
            asyncio.get_event_loop().run_until_complete(
                asyncio.gather(*[
                    self.leavechats(session)
                    for session in sessions
                ])
            )

    async def leavechats(self, session):
        await self.launch(session)

        try:
            async for dialog in session.get_dialogs():
                await session.leave_chat(dialog.chat.id, delete=True)

        except Exception as error:
            console.print(error, style="bold")

        else:
            console.log(dialog.chat.title)