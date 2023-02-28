from pyrogram import Client
import asyncio, sys, os
from rich.console import Console, Theme

from settings.function import SettingsFunction
from settings.config import color_number

from pytgcalls import PyTgCalls, idle
from pytgcalls.types import AudioPiped, AudioVideoPiped, LowQualityVideo

console = Console(theme=Theme({"repr.number": color_number}))

class TgCalls(SettingsFunction):
    """Play video/audio in voice chat"""

    def __init__(self, sessions):
        self.sessions = sessions
        directory = os.path.join("resources", "voice")
        files = os.listdir(directory)

        console.print("[bold red]To finish, press ctrl+\\")

        link = self.invitation(console.input("[bold red]link> [/]"))

        console.print("Path: ({})".format(directory), style="bold magenta")

        console.print(
            "[1] Audio",
            "[2] Video",
            sep="\n",
            style="bold"
        )
        self.function = console.input("[bold]>> [/]")

        for index, mode in enumerate(files, 1):
            console.print("[{}] {}".format(index, mode), style="bold")
        
        choice = int(console.input("[bold]>> [/]"))-1
        self.file = os.path.join(directory, files[choice])

        self.account_count()

        asyncio.get_event_loop().run_until_complete(
            asyncio.gather(*[
                self.started(session, link)
                for session in self.sessions
            ])
        )

    async def started(self, session, link):
        await self.launch(session)

        try:
            chat, app = await session.get_chat(link), PyTgCalls(session)
            await app.start()

            if self.function == "1":
                await self.call(app, chat)
            elif self.function == "2":
                await self.video(app, chat)

            await idle()

        except Exception as error:
            console.print(
                error,
                style="bold"
            )

    async def call(self, app, chat):
        await app.join_group_call(
            chat.id,
            AudioPiped(
                self.file
            )
        )

    async def video(self, app, chat):
        await app.join_group_call(
            chat.id,
            AudioVideoPiped(
                self.file,
                video_parameters=LowQualityVideo()
            )
        )
