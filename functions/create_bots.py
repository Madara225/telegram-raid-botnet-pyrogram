from pyrogram import Client
from settings.function import SettingsFunction
from rich.console import Console

import asyncio
import random
import string
import time

console = Console()

class CreateBots(SettingsFunction):
    """Creating bots"""

    def __init__(self, sessions):
        self.sessions = sessions
        console.print("[bold white]The usernames will be selected randomly.")

        self.account_count()
        nickname = console.input("[bold red]Nickname> ")

        for session in self.sessions:
            username = "".join(random.choices(string.ascii_letters, k=10))+"bot"
            self.create_bot(session, nickname, username)

    def create_bot(self, session: Client, nickname: str, username: str):
        asyncio.get_event_loop().run_until_complete(
            self.launch(session)
        )

        commands = [
            "/newbot",
            nickname,
            username
        ]

        for command in commands:
            try:
                session.send_message("@BotFather", command)
            except Exception as error:
                return None
            else:
                time.sleep(0.5)

        token = self.parse_token(session)
        if token:
            console.print("Bot: ({}, @{})".format(token, username), style="bold white")
        else:
            console.print("[bold red]Error, maybe the username is already in use.")

    def parse_token(self, session: Client) -> str | None:
        try:
            messages = session.get_chat_history("@BotFather", limit=1)
            message = [text for text in messages][0]    
            token = message.text.split("\n")[3]
        except Exception:
            ...
        
        return token