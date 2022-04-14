from rich.console import Console, Theme
from pyrogram import Client
import asyncio
from rich.prompt import Prompt, Confirm
from time import perf_counter
from rich.progress import track

from settings.function import SettingsFunction

console = Console(theme=Theme({"repr.number": "bold purple"}))


class Joined(SettingsFunction):
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


		if self.mode == '1':
			try:
				invite = self.link.split('/')[3]
				if invite[0] == '+':
					await app.join_chat('https://t.me/joinchat/'+invite[1:])

				elif invite == 'joinchat':
					await app.join_chat(self.link)

				else:
					await app.join_chat(invite)

			except Exception as error:
				console.print(f'[bold red]ERROR[/]:{me.first_name} {error}')


		elif self.mode == '2':
			try:
				invite = self.link.split('/')[3]
				if invite[0] == '+':
					channel = await app.get_chat('https://t.me/joinchat/'+invite[1:])

				elif invite == 'joinchat':
					channel = await  app.get_chat(self.link)

				else:
					channel = await app.get_chat(invite)

				await app.join_chat(channel.linked_chat.id)

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
						description='[bold]JOIN',
						):
				await self.join_chat(app)
				await asyncio.sleep(time_normal)

		
