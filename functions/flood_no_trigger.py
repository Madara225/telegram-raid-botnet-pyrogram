from rich.console import Console
from rich.prompt import Prompt

import asyncio

from functions.flood import FloodChat
from settings.function import SettingsFunction
from settings.config import color_number

console = Console()

class FloodChatNoTrigger(SettingsFunction):
    """Flood without trigger"""

    def __init__(self, sessions):
        self.sessions = sessions

        peer = int(console.input("[bold red]id> [/]"))
        reply_msg = Prompt.ask("[bold red]id msg[/]", default=None)

        if reply_msg != None:
            reply_msg = int(reply_msg)

        self.flood = FloodChat(self.sessions)
        self.flood.ask()
        self.account_count()

        asyncio.get_event_loop().run_until_complete(
            asyncio.gather(*[
                self.start_flood(session, peer, reply_msg)
                for session in self.sessions
            ])
        )

    async def start_flood(self, session, peer, reply_msg):
        await self.launch(session)
        try:
            await self.flood.flood(session, peer, reply_msg)

        except Exception as error:
            console.print(error, style="bold")


