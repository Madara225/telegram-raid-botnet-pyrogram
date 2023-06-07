from pyrogram import Client

import asyncio, random

from rich.console import Console, Theme
from rich.progress import track
from rich.prompt import Confirm

from settings.function import SettingsFunction
from settings.config import color_number, emoji

console = Console(theme=Theme({"repr.number": color_number}))

class ReactionMessage(SettingsFunction):
    """Using reactions"""

    def __init__(self, sessions):
        self.sessions = sessions
        self.emoji = emoji

        console.print(
            "[1] Put a reaction to the post/msg",
            "[2] Flood reactions",
            sep="\n",
            style="bold"
        )
        choice = console.input("[bold]>> [/]")
        peer, post_id = self.ids(console.input("[bold red]link to the post/msg> [/]"))
        
        print(peer, post_id)

        self.mix_reacion = Confirm.ask("[bold red]use random reactions?[/]")

        if not self.mix_reacion:
            for number, name in enumerate(self.emoji, 1):
                console.print(
                    "[bold white][{}] {}"
                    .format(number, name)
                )

            self.emoji = [self.emoji[int(console.input("[bold white]>> [/]"))-1]]

        self.account_count()

        if choice == "2":
            function = self.flood_reaction
        elif choice == "1":
            function = self.add_reaction

        asyncio.get_event_loop().run_until_complete(
            asyncio.gather(*[
                function(session, peer, post_id)
                for session in self.sessions
            ])
        ) 

    async def add_reaction(self, session, peer, post_id):
        await self.launch(session)

        try:
            await session.send_reaction(
                peer,
                post_id,
                random.choice(self.emoji)
            )
        except Exception as error:
            console.print(error)

    async def flood_reaction(self, session, peer, post_id):
        if await self.launch(session):
            try:
                messages = session.get_chat_history(peer)

            except Exception as error:
                console.print(error, style="bold")

            else:
                count = 0
                async for message in messages:
                    try:
                        await session.send_reaction(peer, message.id, random.choice(self.emoji))

                    except Exception as error:
                        console.print("Not sent. {}".format(error), style="bold white")

                    else:
                        count += 1
                        console.print("Successfully. COUNT: {}".format(count), style="bold green")
