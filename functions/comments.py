from pyrogram import Client
import asyncio
from rich.console import Console, Theme
from rich.prompt import Prompt, Confirm
import random

from settings.function import SettingsFunction
from settings.config import text, range_acc
from settings.config import color_number

console = Console(theme=Theme({"repr.number": color_number}))

class FloodComments(SettingsFunction):
	"""flood to channel comments"""
	def __init__(self, connect_sessions, initialize):
		
		self.initialize = initialize
		self.connect_sessions = connect_sessions
		self.text = text
		
		self.account_count(self.connect_sessions)
		
		self.link_comment = console.input('[bold red]link to post[/]> ')
		self.message = Confirm.ask('[bold red]get text from config?[/]:')
		
		if not self.message:
			self.text = [console.input('[bold red]message[/]> ')]
			
		self.delay = console.input('[bold blue]delay[/](0)> ')
		
		if not self.delay:
			self.delay = 0
			
		asyncio.get_event_loop().run_until_complete(
			asyncio.gather(*[
				self.flood(app)
				for app in self.connect_sessions
				])
			)
			
	async def flood(self, app):
		
		if not self.initialize:
			await app.connect()
			
		me = await app.get_me()
		
		try:
			link = self.link_comment.split('/')
			if link[3] == 'c':
				link_channel = int('-100'+link[4])
				post_id = int(link[5])
			else:
				link_channel = link[3]
				post_id = int(link[4])
			
			print(link_channel, post_id)
			
		except Exception as error:
			console.print(f'[bold red]ERROR[/]:{me.first_name} {error}')
				
		
		post = await app.get_discussion_message(link_channel, post_id)
		count = 0
		for _ in range(range_acc):
			try:
				await post.reply(random.choice(self.text))
				count+=1
				console.print(f'[{me.first_name}] [bold green]sent[/] COUNT: [{count}]')
				
			except Exception as error:
				console.print(f'[bold red]ERROR[/]:{me.first_name} {error}')
				
			await asyncio.sleep(int(self.delay))
