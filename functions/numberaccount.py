from pyrogram import Client
from rich.console import Console, Theme
import asyncio
import phonenumbers
from phonenumbers.phonenumberutil import (
    region_code_for_country_code,
    region_code_for_number,
    country_code_for_region
)

from settings.function import SettingsFunction
from settings.config import color_number

console = Console(theme=Theme({"repr.number": color_number}))

class Checkingnumber(SettingsFunction):
    """Number statistics"""

    def __init__(self, sessions):
        self.sessions = sessions

        self.code = []
        self.country_list = {}

        asyncio.get_event_loop().run_until_complete(
            asyncio.gather(*[
                self.checking_number(session)
                for session in self.sessions
            ])
        )

        for name, code in self.country_list.items():
            if code in self.code:
                console.print(name, self.code.count(code))

    async def checking_number(self, session):
        await self.launch(session)

        try:
            me = await session.get_me()
            country = phonenumbers.parse(f"+{me.phone_number}")

            string_country = region_code_for_country_code(country.country_code)
            code_country = country_code_for_region(string_country)

            self.country_list[string_country]=code_country
            self.code.append(code_country)

        except Exception as error:
            console.print(error, style="bold white")
