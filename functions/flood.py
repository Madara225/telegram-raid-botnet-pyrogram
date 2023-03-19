from pyrogram import Client, idle, enums
from pyrogram.errors import (
    FloodWait, 
    SlowmodeWait, 
    RandomIdDuplicate
)


import asyncio
import random, sys, time, os

from rich.console import Console, Theme
from rich.prompt import Prompt, Confirm
from rich.progress import track

from multiprocessing import Process
from pyrogram.raw import functions, types
from async_lru import alru_cache

from settings.function import SettingsFunction
from settings.config import color_number

console = Console(theme=Theme({"repr.number": color_number}))

class FloodChat(SettingsFunction):
    
    def __init__(self, sessions):
        super().__init__()
        self.sessions = sessions

    def ask(self):
        choices = (
            ("Raid text", self.send_text),
            ("Raid video", self.send_video),
            ("Raid stickers", self.send_stickers)
        )

        for number, function in enumerate(choices, 1):
            console.print(
                "[bold white][{number}] {name}[/]"
                .format(number=number, name=function[0])
            )

        choice = int(console.input("[bold white]>> [/]"))-1
        self.function = choices[choice][1]

        self.notify_all = Confirm.ask(
            "[bold red]notify all?[/]",
            default="y"
        )

        if self.notify_all:
            self.notify_admin = Confirm.ask(
                "[bold red]notify admin?[/]",
                default="y"
            )

        self.delay = int(Prompt.ask(
            "[bold red]delay[/]",
            default="0"
        ))

    async def send_text(self, session, peer, message, reply_msg):
        await session.send_message(
            peer,
            message,
            reply_to_message_id=reply_msg
        )

    async def send_video(self, session, peer, message, reply_msg):
        file = random.choice(os.listdir(os.path.join("resources", "video")))

        await session.send_video(
            peer,
            os.path.join(
                "resources", "video", 
                file
            ),
            caption=message,
            reply_to_message_id=reply_msg
        )

    async def send_stickers(self, session, peer, message, reply_msg):
        file = random.choice(os.listdir(os.path.join("resources", "stickers")))

        await session.send_sticker(
            peer,
            os.path.join(
                "resources", "stickers", 
                file
            ),
            reply_to_message_id=reply_msg
        )

    async def flood(self, session, peer, reply_msg):
        await self.launch(session)

        if self.notify_all:
            users = [users async for users in session.get_chat_members(peer)]

            users_id = []
            for user in users:
                if user.status in [
                    enums.ChatMemberStatus.OWNER,
                    enums.ChatMemberStatus.ADMINISTRATOR
                ] and not self.notify_admin:
                    continue

                users_id.append(user.user.id)

        me = await session.get_me()

        count = 0
        errors_count = 0

        while count < self.settings.message_count:
            if not self.notify_all:
                message = random.choice(self.settings.messages)
            else:
                message = "<a href=\"tg://user?id={user_id}\">\u206c\u206f</a>{message}" \
                .format(
                    user_id = random.choice(users_id),
                    message = random.choice(self.settings.messages)
                )

            try:
                count += 1

                await self.function(
                    session,
                    peer,
                    message,
                    reply_msg
                )

                console.print(
                    "\[{name}] [green]sent[/] COUNT: {count}"
                    .format(
                        name=me.first_name,
                        count=count
                    ),  style="bold"
                )

            except SlowmodeWait as error:
                self.delay = error.value

                console.print(
                    f"Waiting {error.value} seconds!",
                    style="bold red"
                )

            except RandomIdDuplicate:
                continue

            except Exception as error:
                errors_count += 1
                console.print("Not sent. Error : %s" % error, style="bold white")

            finally:
                await asyncio.sleep(self.delay)

            if errors_count == 3:
                try:
                    await session.leave_chat(
                        peer,
                        delete=True
                    )

                except Exception as error:
                    console.print(
                        error,
                        style="bold"
                    )

                finally:
                    break

    def handler(self, session, index):
        asyncio.get_event_loop().run_until_complete(
            self.launch(session)
        )

        console.print(f"[bold green]successfully ({index})[/]")

        @session.on_message()
        async def main(
            client,
            message
        ):
            if message.text == self.settings.trigger \
                    and message.from_user.id == self.settings.my_id:
                reply_msg = message.reply_to_message_id
                peer = message.chat.id

                await self.flood(session, peer, reply_msg)

        idle()

    def start_process_flood(self):
        self.account_count()

        processes = []

        for index, session in enumerate(self.sessions, 1):
            process = Process(
                target = self.handler,
                args = (session, index)
            )

            process.start()
            processes.append(process)

        console.print(
            "[*][bold white]SEND \"[yellow]{trigger}[/]\" to chat[/]"
            .format(trigger=self.settings.trigger)
        )

        for process in processes:
            process.join()
