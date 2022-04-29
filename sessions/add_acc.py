import string
import random
from pyrogram import *
import json
from asyncio import *
import glob
import os
from rich.console import Console
from config_api import api_id, api_hash

console = Console()

menu = input('''
[1] create an account
[2] add an account to the botnet
[3] checking the session for validity
>> ''')

name = "".join(random.choices(string.ascii_letters, k=10))


data = {"storage_sessions": []}


if menu == '1':
	app = Client(session, api_id, api_hash)
	with app:
		me = app.get_me()
		print([me.first_name])

elif menu == '2':

	data = {"storage_sessions": []}
	for session in glob.glob('*.session'):
		session = session[:-8]

		try:
			app = Client(session, api_id, api_hash)
			app.connect()
			me = app.get_me()
			string = app.export_session_string()
			data['storage_sessions'].append(string)
			print(f'[+]{me.first_name}')

			app.disconnect() 
		except Exception as error:
			console.print(f'[bold red]ERROR[bold white]: {session} {error}')


	with open("sessions.json", "w") as write_file:
		json.dump(data, write_file, indent = 4)

elif menu == '3':
	def checking(session):
		try:
			app = Client(session, api_id, api_hash)
			app.connect()
			me = app.get_me()
			print(me.first_name)
			app.disconnect()
		except:
			print(f'ERROR: {session}')
			os.system(f'mv {session}.session dead')

	for session in glob.glob('*.session'):
		checking(session[:-8])
