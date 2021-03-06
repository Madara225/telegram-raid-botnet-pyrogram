from rich.console import Console, Theme
from pyrogram import Client
import asyncio
from settings.config import color_number

console = Console(theme=Theme({"repr.number": color_number}))

class Leavechat:
    """leave the chat"""

    def __init__(self, connect_sessions, initialize):
        self.initialize = initialize
        self.connect_sessions = connect_sessions

        if console.input('[bold red]are you sure? (y/n): ') == 'y':
            asyncio.get_event_loop().run_until_complete(
                asyncio.gather(*[
                        self.leavechats(session)
                        for session in self.connect_sessions
                    ])
                )

    async def leavechats(self, session):
        if not self.initialize:
            await session.connect()

        try:
            async for dialog in session.get_dialogs():
                if dialog.chat.title != None:
                    print(dialog.chat.title)
                    await session.leave_chat(
                            dialog.chat.id,
                            delete=True
                        )

        except Exception as error:
            console.print(f'[bold red]ERROR[/]:{error}')
