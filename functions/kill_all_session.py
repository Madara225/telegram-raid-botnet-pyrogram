from pyrogram import Client
from pyrogram.raw import types, functions
from pyrogram.errors import HashInvalid

import asyncio
from rich.console import Console
from settings.function import SettingsFunction

console = Console()

class ResetAuth(SettingsFunction):
    """Killed all account sessions"""

    def __init__(self, sessions):
        asyncio.get_event_loop().run_until_complete(
            asyncio.gather(*[
                self.kill_all_session(session)
                for session in sessions
            ])
        )

    async def kill_all_session(self, session):
        if await self.launch(session):
            me = await session.get_me()
            account = await session.invoke(functions.account.GetAuthorizations())

            for x in account.authorizations[::1]:
                try:
                    await session.invoke(functions.account.ResetAuthorization(hash=x.hash))

                except HashInvalid:
                    continue

                except Exception as error:
                    console.print("Error : {}".format(error), style="bold red")

                else:
                    console.print(
                        "[bold]Kill: ({device}, {ip}) -> [bold red]{account_hash}[/]"
                        .format(device=x.device_model, ip=x.ip, account_hash=x.hash)
                    )