from rich.console import Console, Theme
from pyrogram import Client
import asyncio
from rich.progress import track
from rich.prompt import Prompt, Confirm
import random

from settings.function import SettingsFunction
from settings.config import first_name

console = Console(theme=Theme({"repr.number": "bold purple"}))

class TextProfile(SettingsFunction):
	"""change biography/nickname"""
	def __init__(self, connect_sessions, initialize):
		self.first_name = first_name
		self.initialize = initialize
		self.connect_sessions = connect_sessions
		
		name = Confirm.ask('[bold red]to take names from a config?[bold magenta]',
						 choices=["y", "n"]
						 )
		if not name:
			self.first_name = console.input('[bold red]first name[/]> ').split()
			
		self.bio = console.input('[bold red]bio[/]> ')
		self.last_name = console.input('[bold red]last name[/]> ')
		
		for app in track(
				self.connect_sessions,
				description='[bold]CHANGE'
				):
			self.change_profile(app)

	def change_profile(self, app):

		if not self.initialize:
			app.connect()
			
		me = app.get_me()

		try:
			app.update_profile(
				first_name=random.choice(self.first_name),
				bio=self.bio,
				last_name=self.last_name
				)

		except Exception as error:
			console.print(f'[bold red]ERROR[/]:{me.first_name} {error}')

