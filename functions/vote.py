from rich.console import Console, Theme
from pyrogram import Client
from rich.prompt import Prompt, Confirm
from time import perf_counter
from rich.progress import track

from settings.function import SettingsFunction
from settings.config import color_number

console = Console(theme=Theme({"repr.number": color_number}))

class Vote(SettingsFunction):
	'''vote in chat'''
	def __init__(self, connect_sessions, initialize):
		
		self.initialize = initialize

		self.account_count(connect_sessions)
		
		self.link = console.input('[bold red]message[/]> ')
		self.option = int(console.input('[bold red]option number[blue](1-10)[/]: '))-1
		
		for app in track(connect_sessions,
				   description='[bold]VOTED'
				   ):
			self.voited(app)
			
			
	def voited(self, app):
		if not self.initialize:
			app.connect()
		
		me = app.get_me()
		
		try:
			link = self.link.split('/')
			if link[3] == 'c':
				link_channel = int('-100'+link[4])
				post_id = int(link[5])
			else:
				link_channel = link[3]
				post_id = int(link[4])
			
			
		except Exception as error:
			console.print(f'[bold red]ERROR[/]:{me.first_name} {error}')
		
		try:
			app.vote_poll(link_channel, post_id, self.option)
		
		except Exception as error:
			console.print(f'[bold red]ERROR[/]:{me.first_name} {error}')
		
