from rich.console import Console, Theme
from pyrogram import Client
import sys

from settings.settings import MenuSettings
from settings.settings_session import ConnectSessions
from settings.config import color_number

console = Console(theme=Theme({"repr.number": color_number}))

console.print('''[bold white]
idea taken from @huis_bn
botnet on telethon: https://github.com/json1c/telegram-raid-botnet
botnet on pyrogram: https://github.com/Madara225/telegram-raid-botnet-pyrogram
''')

accs = ConnectSessions()
list_function = MenuSettings()


console.print("Author's channel: https://t.me/Pepe_devs")

def botnet_main():
	
	menu_function={}
	
	console.print(f'[bold white]botnet accounts >> [{color_number}]{len(accs.connect_sessions)}')
	
	for num_function, function in enumerate(
			list_function.menu_botnet, 
			start=1
		):
		
		menu_function[num_function]=function
		console.print(f'[bold][{num_function}] - {function.__doc__}')
		
	try:
		menu = int(console.input('>> '))
			
		for num, classes in menu_function.items():
			if num == menu:
				classes(
					accs.connect_sessions, 
					accs.initialize
					)

	except KeyboardInterrupt:
		sys.exit()
		
	except:
		botnet_main()

botnet_main()
