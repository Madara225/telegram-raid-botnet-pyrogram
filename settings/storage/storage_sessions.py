from pyrogram import Client, idle

import json, sys, os
import asyncio

from rich.prompt import Prompt, Confirm
from rich.console import Console, Theme

from settings.function import SettingsFunction
from settings.storage.storage_settings import Settings

console = Console()

class ConnectSessions(SettingsFunction):
    
    def __init__(self):
        path = "sessions/sessions.json"

        self.initialize = Prompt.ask(
            "[bold]Initialize sessions?[/]",
            choices=["y", "n"], default="n"
        )

        self.sessions = []

        if not os.path.exists(path):
            console.print("[bold red]Add accounts![/]")
            sys.exit()

        with open(path, "r") as json_session:
            asyncio.get_event_loop().run_until_complete(
                asyncio.gather(*[
                    self.initialize_client(session)
                    for session in json.load(json_session)["storage_sessions"]
                ])
            )

    async def initialize_client(self, session):
        session = Client("session", session_string=session)
        self.sessions.append(session)

        if self.initialize == "y":
            try:
                await session.start()
                console.log("CONNECTED")

            except Exception as error:
                self.sessions.remove(session)
                console.print(error, style="bold")