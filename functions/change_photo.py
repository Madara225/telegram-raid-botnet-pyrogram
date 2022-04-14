from rich.console import Console, Theme
from pyrogram import Client
import asyncio
from rich.progress import track
import random

from settings.config import photo
from settings.function import SettingsFunction

console = Console(theme=Theme({"repr.number": "bold purple"}))


class ChangePhoto(SettingsFunction):
	"""change profile photo"""
	def __init__(self, connect_sessions, initialize):
		
		console.input('[magenta]photos are taken from the "photo" folder\n[bold white]press "ENTER"')
		
		for app in track(
					connect_sessions,
					description='[bold]photo change'
					):
			if not initialize:
				app.connect()
				
			me = app.get_me()
			try:
				app.set_profile_photo(
					photo="photo/"+random.choice(photo)
					   )
			except Exception as error:
				console.print(f'[bold red]ERROR[/]:{me.first_name} {error}')
