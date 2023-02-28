from pyrogram import Client

import random, os
import asyncio

from rich.console import Console, Theme
from rich.progress import track

from settings.function import SettingsFunction
from settings.config import color_number

console = Console(theme=Theme({"repr.number": color_number}))

class ChangePhoto(SettingsFunction):
    """Change profile photo"""

    def __init__(self, sessions):

        console.print(
            "[1] Set new photo",
            "[2] Delete all photos",
            sep="\n",
            style="bold"
        )

        choice = console.input("[bold]>> [/]")

        if choice == "1":
            function = self.change_photo
        elif choice == "2":
            function = self.delete_photo

        asyncio.get_event_loop().run_until_complete(
            asyncio.gather(*[
                function(session)
                for session in sessions
            ])
        )

    async def change_photo(self, session):
        await self.launch(session)

        directory = os.path.join("resources", "account_photo")

        try:
            me = await session.get_me()

            file = random.choice(os.listdir(directory))
            await session.set_profile_photo(photo=directory+file)

        except Exception as error:
            console.print(
                "Error : {}".format(error), style="bold white"
            )

        else:
            console.print(
                "[bold green][+] {name} {file}[/]"
                .format(name=me.first_name, file=file)
            )

    async def delete_photo(self, session):
        await self.launch(session)
        
        try:
            photos = [photo async for photo in session.get_chat_photos("me")]

            await session.delete_profile_photos(
                [photo.file_id for photo in photos[0:]]
            )

        except Exception as error:
            console.print(error, style="bold white")

        else:
            console.print("[-] DELETED", style="bold green")