from rich.prompt import Prompt, Confirm
import asyncio

class SettingsFunction:
	def account_count(self, connect_sessions):
		acc_count = int(Prompt.ask('[bold red]how many accounts to use?',
							 default=str(len(connect_sessions))
							 ))

		self.connect_sessions = connect_sessions[:acc_count]
		
	async def flood_start(self, app, users_id, chat_id, reply_msg_id):
		return await {
			'1': lambda: self.flood_text(
				app,
				users_id,
				chat_id,
				reply_msg_id
				),

			'2': lambda: self.flood_stickers(
				app,
				chat_id,
				reply_msg_id
				),
		
			'3': lambda: self.flood_photo(
				app,
				chat_id,
				reply_msg_id
				),
		}.get(self.flood_menu, lambda: console.print('[bold red]ERROR'))()
