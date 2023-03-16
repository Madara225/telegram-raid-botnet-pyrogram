from pyrogram import Client

import asyncio

from rich.console import Console, Theme

from settings.function import SettingsFunction
from settings.config import color_number

console = Console(theme=Theme({"repr.number": color_number}))

class Vote(SettingsFunction):
    """Vote in poll"""

    def __init__(self, sessions):
        self.sessions = sessions

        self.account_count()

        console.print(
            "Does not work if the survey is a response to another message.",
            style="bold white"
        )
        self.link = console.input("[bold red]link> [/]")

        console.print("option number (1-10)", style="bold red")
        self.option = int(console.input(">> "))-1

        asyncio.get_event_loop().run_until_complete(
            asyncio.gather(*[
                self.voited(session)
                for session in self.sessions
            ])
        )

    async def voited(self, session):
        await self.launch(session)

        try:
            me = await session.get_me()
            peer, post_id = self.ids(self.link)

            await session.vote_poll(
                peer,
                post_id,
                self.option
            )

        except Exception as error:
            console.print(error, style="bold")

        else:
            console.print("{name} successfully".format(name=me.first_name), style="bold green")
