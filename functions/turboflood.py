from pyrogram import Client

import asyncio
import random

from rich.console import Console, Theme

from settings.function import SettingsFunction
from settings.config import color_number

console = Console(theme=Theme({"repr.number": color_number}))

class TurboFlood(SettingsFunction):
    """Fast flood (text only)"""

    def __init__(self, sessions):
        super().__init__()
        self.sessions = sessions

        self.link = self.invitation(console.input("[bold red]link> [/]"))
        self.account_count()

        print()

        if len(self.sessions) < 15:
            console.print(
                "[bold white]Use at least 15 accounts for this feature."
            )

        asyncio.get_event_loop().run_until_complete(
            asyncio.gather(*[
                self.execute(session)
                for session in self.sessions
            ])
        )

        console.print("[bold green]stop[/]")

    async def flood_text(self, session, peer):
        try:
            await session.send_message(
                peer, 
                random.choice(self.settings.messages)
            )

        except Exception as error:
            console.print(error)

    async def execute(self, session):
        await self.launch(session)
        
        try:
            chat = await session.get_chat(self.link)
            peer = chat.id

        except Exception as error:
            console.print(f"Error : {error}", style="bold white")

        else:
            await asyncio.gather(*[
                self.flood_text(session, peer)
                for session in self.sessions
            ])