from pyrogram import Client
import asyncio
from rich.console import Console
from settings.function import SettingsFunction

console = Console()

class SetPassword(SettingsFunction):
    """Enable 2fa on your account"""

    def __init__(self, sessions):
        password = console.input("[bold red]Password> [/]")

        asyncio.get_event_loop().run_until_complete(
            asyncio.gather(*[
                self.enable_password(session, password)
                for session in sessions
            ])
        )

    async def enable_password(self, session: Client, password: str):
        await self.launch(session)

        try:
            me = await session.get_me()
            await session.enable_cloud_password(password)

        except Exception as error:
            console.print(f"[bold]The password is not set.[red] Error: {error}[/]")

        else:
            console.print(f"[bold green]{me.first_name} - the password is set.[/]")
