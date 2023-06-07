from pyrogram import Client

import asyncio
import time

from rich.console import Console, Theme
from rich.prompt import Prompt

from settings.function import SettingsFunction
from settings.config import color_number

console = Console(theme=Theme({"repr.number": color_number}))

class FloodMP(SettingsFunction):
    """Flood to PM"""

    def __init__(self, sessions):
        self.sessions = sessions

        self.account_count()

        self.users = console.input("[bold red]USER: [/]")
        self.text_flood = console.input("[bold red]text> [/]")
        
        self.delay = Prompt.ask("[bold red]delay[/]", default="0")

        asyncio.get_event_loop().run_until_complete(
            asyncio.gather(*[
                self.flood_pm(session)
                for session in self.sessions
            ])
        )

    async def flood_pm(self, session):
        if await self.launch(session):
            me = await session.get_me()
            count = 0

            while True:
                try:
                    await session.send_message(self.users, self.text_flood)

                    count += 1
                    console.print(
                        "\[{name}] [bold green]sent[/] COUNT: {count}"
                        .format(name=me.first_name, count=count)
                    )

                except Exception as error:
                    console.print("Not sent. Error : %s" % error, style="bold white")

                finally:
                    await asyncio.sleep(int(self.delay))