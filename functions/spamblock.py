from pyrogram import Client
from rich.console import Console, Theme
import re
import asyncio

from settings.function import SettingsFunction
from settings.config import color_number

console = Console(theme=Theme({"repr.number": color_number}))

class SpamBlock(SettingsFunction):
	"""checking accounts for spam block"""
	def __init__(self, connect_sessions, initialize):
		self.connect_sessions = connect_sessions
		self.initialize = initialize
		
		for app in self.connect_sessions:
			self.checking_block(app)

	def checking_block(self, app):
		if not self.initialize:
			app.connect()
		try:
			me = app.get_me()
			app.send_message('SpamBot', '/start')

		except Exception as error:
			app.unblock_user(178220800)
			console.print(f'[bold red]ERROR[white bold]: <I tried to unban the bot, try again!>[/] {me.first_name} {error}')
			
		self.message = app.get_history('SpamBot', limit=1)
			
		for msg in self.message:
			if msg.text != '/start':
				try:
					if msg.text == 'Ваш аккаунт свободен от каких-либо ограничений.' or msg.text == 'Good news, no limits are currently applied to your account. You’re free as a bird!':
						console.print(f'[bold green][+][/] [{me.first_name}] [{me.phone_number}] id:[{me.id}]')

					else:
						text = re.findall(r"\d+\s\w+\s\d{4}", msg.text)
						console.print(f'[bold red][-][/] [{me.first_name}] [{me.phone_number}] id:[{me.id}] = {text[0]}')

				except:
					console.print(f'[bold red][-][/] [{me.first_name}] [{me.phone_number}] id:[{me.id}] [bold red] permanent block[/]')
