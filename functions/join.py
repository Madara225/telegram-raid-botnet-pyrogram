from pyrogram import Client
from pyrogram.errors import UserAlreadyParticipant

from rich.console import Console, Theme
from rich.prompt import Prompt, Confirm
from rich.progress import track

import asyncio
from time import perf_counter, sleep
from async_lru import alru_cache

from settings.function import SettingsFunction
from functions.flood import FloodChat
from settings.config import time_captcha

console = Console()

class Joined(FloodChat):
    """Join to chat"""

    def __init__(self, sessions):
        self.sessions = sessions
        self.flood_joining = None
        self.captcha = None

        self.account_count()

        peer = self.invitation(console.input("[bold red]link> [/]"))
        
        print()

        console.print(
            "[1] Joining the chat/channel",
            "[2] Joining the channel chat",
            sep="\n",
            style="bold"
        )

        print()

        self.mode = console.input("[bold]>> [/]")
        self.entry_time = Prompt.ask("[bold red]speed", choices=["norm", "fast"])

        asyncio.get_event_loop().run_until_complete(
            self.mode_selection(peer)
        )

    @alru_cache
    async def mode_selection(self, peer: str):
        console.print(
            f"[bold white]The {self.entry_time} mode is set!"
        )

        if self.entry_time == "norm":
            self.captcha = Confirm.ask("[bold red]captcha?")
            delay = int(console.input("[bold blue]delay> [/]"))

            for session in track(self.sessions):
                await self.execute(session, peer)
                await asyncio.sleep(delay)

        elif self.entry_time == "fast":
            self.flood_joining = Confirm.ask(
                "[bold red]flood after joining?[/]"
            )

            if self.flood_joining:
                self.flood = FloodChat(self.sessions)
                self.flood.ask()

            joined = 0
            start = perf_counter()

            tasks = await asyncio.gather(*[
                self.execute(session, peer)
                for session in self.sessions
            ])

            for result in tasks:
                joined += 1

            join_time = round(perf_counter()-start, 2)

            console.print(
                "[+] {joined} bots joined [yellow]{time}[/]s"
                .format(joined=joined, time=join_time)
            )

    async def join(self, session: Client, peer: str) -> int:
        try:
            if self.mode == "2":
                group = await session.get_chat(peer)
                peer = group.linked_chat.id
            
            await session.join_chat(peer)

        except UserAlreadyParticipant:
            ...

        except Exception as error:
            console.print("[-] Not join. Error : [red]{error}".format(error=error), style="bold white")

        try:
            if self.mode == "1":
                group = await session.get_chat(peer)
                peer = group.id
        except:
            ...

        return peer

    async def execute(self, session: Client, link: str):
        await self.launch(session)

        peer = await self.join(session, link)

        if isinstance(peer, str):
            return None

        if self.captcha:
            await self.solve_captcha(session, peer)

        if self.flood_joining:
            reply_msg = None
            await self.flood.flood(
                session,
                peer,
                reply_msg
            )

    async def solve_captcha(self, session: Client, chat_id: int):
        sleep(time_captcha)

        message = session.get_chat_history(
            chat_id,
            limit=5
        )

        async for msg in message:
            try:
                callback = msg.reply_markup \
                    .inline_keyboard[0][0].callback_data

                await session.request_callback_answer(
                    chat_id,
                    msg.id,
                    callback
                )
            except:
                pass
