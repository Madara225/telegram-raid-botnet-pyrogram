from pyrogram import Client

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
        self.sessions = []

        self.initialize = Prompt.ask("[bold]Initialize sessions?[/]", choices=["y", "n"], default="n")

        if not os.path.exists(path):
            console.print("[bold red]Add accounts![/]")
            sys.exit()

        with open(path, "r") as json_session:
            sessions = json.load(json_session)["storage_sessions"]

            asyncio.get_event_loop().run_until_complete(
                asyncio.gather(*[
                    self.initialize_session(session)
                    for session in sessions
                ])
            )

    async def initialize_session(self, session):
        session = Client("session", session_string=session)
        self.sessions.append(session)

        if self.initialize != "y":
            return

        if await self.launch(session):
            console.print("CONNECTED")
            return

        self.sessions.remove(session)