from pyrogram import Client, enums
import asyncio
import numpy
import random
from rich.console import Console, Theme

from settings.config import color_number
from settings.function import SettingsFunction

console = Console(theme=Theme({"repr.number": color_number}))

class InviteUsers(SettingsFunction):
    """Inviting users to chat"""

    def __init__(self, sessions):
        self.sessions = sessions
        self.users = []

        link = self.invitation(console.input("[bold red]Where to get users from> "))
        self.link_add_group = self.invitation(console.input("[bold red]Where to invite users> "))

        self.account_count()
        self.parse_users(random.choice(self.sessions), link)

    def chunks(self, count_sessions):
        return [self.users[i::count_sessions] for i in range(count_sessions)]

    async def invite(self, users, session, invite_chat):
        await self.launch(session)

        count = 0
        for user in users:
            try:
                await session.add_chat_members(invite_chat.id, user)
            except Exception as error:
                console.print("Not invited. Error : {}".format(error), style="bold red")
            else:
                count += 1
                console.print("Invited: {} users".format(count), style="bold green")

    def parse_users(self, session, link):
        asyncio.get_event_loop().run_until_complete(
            self.launch(session)
        )

        try:
            chat = session.get_chat(link)
            invite_chat = session.get_chat(self.link_add_group)

        except Exception as error:
            console.print(error, style="bold")

        else:
            for member in session.get_chat_members(chat.id):
                if not member.user.is_bot:
                    if not member.user.username:
                        self.users.append(member.user.id)
                    else:   
                        self.users.append(member.user.username)

            console.print(
                "[bold yellow][*] Got %d users." % len(self.users)
            )
            users = self.chunks(len(self.sessions))

            asyncio.get_event_loop().run_until_complete(
                asyncio.gather(*[
                    self.invite(users, session, invite_chat)
                    for session, users_chunk in zip(self.sessions, users)
                ])
            )