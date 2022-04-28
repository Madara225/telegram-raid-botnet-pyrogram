from rich.console import Console, Theme
from pyrogram import Client, idle
import asyncio
from rich.prompt import Prompt, Confirm
from rich.progress import track
from multiprocessing import Process
import sys
import random
import time


from settings.config import *
from functions.flood import FloodChat
from settings.config import color_number

console = Console(theme=Theme({"repr.number": color_number}))

class FloodChatNoTrigger(FloodChat):
	"""flood to chat no trigger"""
	def __init__(self, connect_sessions, initialize):
		self.connect_sessions = connect_sessions
		
		if initialize:
			console.print('[bold red]cannot be used with initialization')
			sys.exit()
		
		self.chat_id = int(console.input('[bold red]id chat[/]: '))
		self.reply_msg_id = console.input('[bold red]link message [False][/]: ')
		
		try:
			self.reply_msg_id = int(self.reply_msg_id.split('/')[-1])
		
		except:
			self.reply_msg_id = False
		
		print(self.reply_msg_id)
			
		self.flood_menu = console.input(
'''[bold]
[1] - flood text
[2] - flood stickers/video
[3] - flood photo
>> ''')
		
		self.notify = Confirm.ask('[bold red]notify admins?')
		
		self.start_process_flood()
		
	def flood(self, app, num_accs): 
		try:
			app.connect()
			console.log(f'initialized[*]{num_accs}')
			self.me = app.get_me()

			self.users_id = []
			self.admins = []
			
		except Exception as error:
				console.print(f'[bold red]ERROR[/]:{self.me.first_name} {error}')


		for member1 in app.iter_chat_members(self.chat_id, filter="administrators"):
			self.admins_id = member1.user.id
			self.admins.append(str(self.admins_id))

		for member in app.iter_chat_members(self.chat_id):
			self.user_id = member.user.id
			self.users_id.append(str(self.user_id))
			
		if not self.notify:
			self.users_id = list(set(self.users_id)-set(self.admins))

		count = 0
		for _ in range(range_acc):
			try:
				asyncio.get_event_loop().run_until_complete(
				self.flood_start(
						app,
						random.choice(self.users_id),
						self.chat_id,
						self.reply_msg_id
						)
				)
				count += 1
				console.print(f'[{self.me.first_name}] [bold green]sent[/] COUNT: [{count}]')

			except Exception as error:
				console.print(f'[bold red]ERROR[/]:{self.me.first_name} {error}')

			time.sleep(int(self.delay))



	def start_process_flood(self):
		self.account_count(self.connect_sessions)
		self.delay = console.input('[bold blue]delay[/](0)> ')
		
		if not self.delay:
			self.delay = 0
			
		processes = []

		for num_accs, session in enumerate(
				self.connect_sessions, 
				start=1):
			
			process = Process(
				target=self.flood, args=(session, num_accs,)
				)
			process.start()
			processes.append(process)

		for process in processes:
			process.join()
