from pyrogram import Client
import asyncio, random

from rich.prompt import Prompt, Confirm
from rich.console import Console, Theme

from functions.flood import FloodChat
from settings.function import SettingsFunction
from settings.config import color_number

console = Console(theme=Theme({"repr.number": color_number}))

class FloodComments(SettingsFunction):
    """Flood to channel comments"""

    def __init__(self, sessions):
        super().__init__()
        self.sessions = sessions
        
        self.account_count()

        peer, msg_id = self.ids(console.input("[bold red]link post: [/]"))
        delay = int(Prompt.ask("[bold red]delay", default="0"))

        asyncio.get_event_loop().run_until_complete(
            asyncio.gather(*[
                self.flood_comments(session, peer, msg_id, delay)
                for session in self.sessions
            ])
        )

    async def flood_comments(self, session, peer, msg_id, delay):
        await self.launch(session)

        try:
            me = await session.get_me()
            post = await session.get_discussion_message(peer, msg_id)

        except Exception as error:
            console.print("Error : {}".format(error), style="bold white")

        else:
            count = 0
            while count < self.settings.message_count:
                try:
                    await post.reply(random.choice(self.settings.messages))

                except Exception as error:
                    console.print("Not sent. {}".format(error))

                else:
                    count += 1
                    console.print(
                        "[bold]\[{name}] [green]sent[/] COUNT: {count}"
                        .format(name=me.first_name, count=count),
                    )
                finally:
                    await asyncio.sleep(delay)