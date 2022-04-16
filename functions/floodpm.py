from rich.console import Console, Theme
from pyrogram import Client
import asyncio
from pyrogram.session import Session
from rich.prompt import Prompt, Confirm
import time

from settings.config import range_acc
from settings.function import SettingsFunction
from settings.config import color_number

console = Console(theme=Theme({"repr.number": color_number}))

class FloodMP(SettingsFunction):
	"""flood to PM"""
	
	def __init__(self, connect_sessions, initialize):
		self.connect_sessions = connect_sessions
		self.initialize = initialize
		
		self.account_count(self.connect_sessions)
		
		self.users = console.input('[bold red]USER[/]> ')
		self.text_flood = console.input('[bold red]text flood[/]> ')
		self.delay = console.input('[bold red]delay[/]> ')
		
		if not self.delay:
			self.delay = 0
		
		asyncio.get_event_loop().run_until_complete(
			asyncio.gather(*[
				self.flood_pm(app)
				for app in self.connect_sessions
				])
			)
		
	async def flood_pm(self, app):
		if not self.initialize:
			await app.connect()
			
		me = await app.get_me()
		count = 0

		while True:
			try:
				await app.send_message(
					self.users,
					self.text_flood
					)
				count += 1
				console.print(f'[{me.first_name}] [bold green]sent: [{count}]')
				
			except Exception as error:
				console.print(f'[bold red]ERROR[/]:{me.first_name} {error}')
			
			await asyncio.sleep(int(self.delay))

