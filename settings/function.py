from rich.prompt import Prompt
from rich.console import Console

import random, sys

from settings.storage.storage_settings import Settings

console = Console()

class SettingsFunction:
    def __init__(self):
        self.settings = Settings()

    def account_count(self):
        account_count = int(Prompt.ask(
            "[bold red]How many accounts to use?[/]",
            default=str(len(self.sessions))
        ))

        self.sessions = random.sample(
            self.sessions,
            account_count
        )

    async def launch(self, session):
        try:
            await session.start()

        except ConnectionError:
            pass

        except Exception as error:
            console.print("[bold red]Not connected.[/] Error : {}".format(error), style="bold white")

    def invitation(self, link: str) -> str:
        if not "/+" in link:
            if "/joinchat" in link:
                result = link
            else:
                result = link.split("/")[3]
        else:
            result = link.replace("/+", "/joinchat/")

        return result

    def ids(self, link: str) -> str:
        group = "".join(link.split("/")[-2:-1])
        post_id = int(link.split("/")[-1])

        if group.isdigit():
            group = int(f"-100{group}")

        return group, post_id