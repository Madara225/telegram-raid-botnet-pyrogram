from pyrogram import Client

import asyncio
import random

from rich.console import Console, Theme
from rich.progress import track
from rich.prompt import Prompt, Confirm

from settings.function import SettingsFunction
from settings.config import color_number

console = Console(theme=Theme({"repr.number": color_number}))

class TextProfile(SettingsFunction):
    """Change biography/nickname"""

    def __init__(self, sessions):
        super().__init__()
        self.first_name = self.settings.names
        self.sessions = sessions

        name = Confirm.ask(
            "[bold red]to take names from a config?[/]",
            choices=["y", "n"]
        )

        if not name:
            self.first_name = [console.input("[bold red]first name: [/]")]

        self.bio = console.input("[bold red]bio> [/]")
        self.last_name = console.input("[bold red]last name> [/]")

        asyncio.get_event_loop().run_until_complete(
            asyncio.gather(*[
                self.change_profile(session)
                for session in self.sessions
            ])
        )

    async def change_profile(self, session):
        await self.launch(session)

        new_name = random.choice(self.first_name)

        try:
            me = await session.get_me()

            await session.update_profile(
                first_name=new_name,
                bio=self.bio,
                last_name=self.last_name
            )

        except Exception as error:
            console.print(error, style="bold")

        else:
            console.print(
                "[bold green][+] {name} -> {new_name}[/]"
                .format(name=me.first_name, new_name=new_name)
            )
