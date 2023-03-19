from pyrogram import Client

import string
import random
import asyncio
import json

from settings.function import SettingsFunction
from rich.console import Console

console = Console()

class CreateChannels(SettingsFunction):

	def __init__(self, sessions):
		self.sessions = sessions
		name = "".join(random.choices(string.ascii_letters, k=5))

		self.account_count()

		asyncio.get_event_loop().run_until_complete(
			asyncio.gather(*[
				self.add_channel(session)
				for session in self.sessions
			])
		)

	async def add_channel(self, session):
		await self.launch(session)

		try:
			channel = await session.create_channel("test")

		except Exception as error:
			console.print("Error : {}".format(error))

		# else:
		# 	with open("channels.json", "w") as file:
		# 		json.dump(channel, file, indent=4)

		# 	console.print(channel, style="bold white")