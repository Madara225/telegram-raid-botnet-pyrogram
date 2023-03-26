from pyrogram import Client
from pyrogram.errors import PeerIdInvalid, ChannelPrivate

import asyncio

from rich.console import Console, Theme
from async_lru import alru_cache

from settings.config import color_number
from settings.function import SettingsFunction

console = Console(theme=Theme({"repr.number": color_number}))

class Leavechat(SettingsFunction):
    """Leave the chat"""

    def __init__(self, sessions):
        if console.input("[bold red]Are you sure? (y/n): ") == "y":
            asyncio.get_event_loop().run_until_complete(
                asyncio.gather(*[
                    self.leavechats(session)
                    for session in sessions
                ])
            )

    @alru_cache
    async def leavechats(self, session):
        await self.launch(session)

        try:
            async for dialog in session.get_dialogs():
                await session.leave_chat(dialog.chat.id, delete=True)

                console.log(
                    "[bold green]Name: {name} id {id}"
                    .format(name=dialog.chat.title if dialog.chat.first_name is None else dialog.chat.first_name, id=dialog.chat.id)
                )

        except PeerIdInvalid:
            ...

        except ChannelPrivate as private_error:
            ...

        except Exception as error:
            console.print("Error : {}".format(error), style="bold white")