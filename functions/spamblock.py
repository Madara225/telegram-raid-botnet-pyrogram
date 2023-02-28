from pyrogram import Client
from pyrogram.errors import BadRequest

import re
import asyncio
import time

from rich import box
from rich.table import Table
from rich.console import Console, Theme

from settings.function import SettingsFunction
from settings.config import color_number

console = Console(theme=Theme({"repr.number": color_number}))

class SpamBlock(SettingsFunction):
    """Checking the status of accounts"""

    def __init__(self, sessions):
        self.sessions = sessions

        table = Table(box=box.ROUNDED)

        for name in [
            "Name", 
            "Number", 
            "Block"
        ]:
            table.add_column(name)

        count = 0

        for session in self.sessions:
            asyncio.get_event_loop().run_until_complete(
                self.message(session, table)
            )

            count += 1
            console.print(f">> {count}/{len(self.sessions)}", end="\r")

        console.rule("spam block")
        console.print(table)

    async def message(self, session, table):
        await self.launch(session)

        try:
            await session.send_message(
                "SpamBot",
                "/start"
            )

        except BadRequest:
            await session.unblock_user(178220800)
            console.print("[bold green]unblocked![/]")

            await self.message(session, table)

        except Exception as error:
            console.print(error, style="bold")

        else:
            await self.checking_block(session, table)

    async def checking_block(self, session, table):
        me = await session.get_me()

        messages = session.get_chat_history("SpamBot", limit=1)
        message = [text async for text in messages][0]

        if message.text == "/start":
            await self.checking_block(session)

        else:
            string = message.text.split("\n")

            if len(string) != 1:
                date = re.findall(r"\d+\s\w+\s\d{4}", message.text)

                if date:
                    result = date[0]

                else:
                    result = "[bold red][-][/]"

            else:
                result = "[bold green][+][/]"

        table.add_row(
            me.first_name,
            me.phone_number,
            result
        )
