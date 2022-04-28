from rich.console import Console, Theme
from pyrogram import Client
import asyncio
from rich.prompt import Prompt, Confirm
from time import perf_counter
from rich.progress import track

from settings.function import SettingsFunction
from settings.config import color_number
from functions.flood import FloodChat

console = Console(theme=Theme({"repr.number": color_number}))


class Joined(FloodChat):
	"""join to chat"""
	def __init__(self, connect_sessions, initialize):
		
		self.initialize = initialize
		self.connect_sessions = connect_sessions

		self.account_count(self.connect_sessions)
			
		self.mode = console.input(f'''[bold]
[1] - joining a chat/channel
[2] - joining a chat via a channel
[bold red]mode[/]> ''')
		
		self.link = console.input(f'[bold red]link[/]> ')
		self.settings_join = Prompt.ask('[bold red]speed[bold magenta]', 
choices=["norm", "fast"])

		asyncio.get_event_loop().run_until_complete(
			 self.start_joined()
			 )

	async def join_chat(self, app):
		if not self.initialize:
			await app.connect()
			
		me = await app.get_me()

		try:
			invite = self.link.split('/')[3]
			if invite[0] == '+':
				link = 'https://t.me/joinchat/'+invite[1:]

			elif invite == 'joinchat':
				link = self.link

			else:
				link = invite
			

			if self.mode == '1':
				await app.join_chat(link)

			elif self.mode == '2':
				link = await app.get_chat(link)
				await app.join_chat(link.linked_chat.id)
				
			
		except Exception as error:
			console.print(f'[bold red]ERROR[/]:{me.first_name} {error}')

	async def start_joined(self):
		if self.settings_join == 'fast':

			joined = 0
			start = perf_counter()

			with console.status("[bold]JOIN", spinner='aesthetic'):
				tasks = await asyncio.gather(*[
					self.join_chat(app)
					for app in self.connect_sessions
					])

			for result in tasks:
					joined += 1

			join_time = round(perf_counter() - start, 2)
			console.print(f"[+] {joined} bots joined [yellow]{join_time}[/]s")
				

		elif self.settings_join == 'norm':

			time_normal = int(console.input('[bold blue]delay[/]> '))
			for app in track(
					self.connect_sessions,
					description='[bold]JOIN'):
				
				await self.join_chat(app)
				await asyncio.sleep(time_normal)

		
