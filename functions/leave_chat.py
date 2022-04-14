from rich.console import Console, Theme
from pyrogram import Client
import asyncio

console = Console(theme=Theme({"repr.number": "bold purple"}))

class Leavechat:
	"""leave the chat"""
	def __init__(self, connect_sessions, initialize):
		
		self.initialize = initialize
		self.connect_sessions = connect_sessions
		
		
		if console.input('[bold red]are you sure? (y/n)') == 'y':
			asyncio.get_event_loop().run_until_complete(
				asyncio.wait([
						self.leavechats(app)
						for app in self.connect_sessions
					])
				)
		
	async def leavechats(self, app):
		if not self.initialize:
			await app.connect()

		
		async for dialog in app.iter_dialogs():
			print(dialog.chat.title)
			try:
				await app.leave_chat(dialog.chat.id, delete=True)
				
			except Exception as error:
				console.print(f'[bold red]ERROR[/]:{error}')
		
		
		
		
		
		
