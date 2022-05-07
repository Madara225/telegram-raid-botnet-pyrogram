from rich.prompt import Prompt, Confirm
import asyncio
import sys
from rich.console import Console

console = Console()

class SettingsFunction:
    def add_api(self):
        api_id = int(console.input('[bold red]API ID:[/] '))
        api_hash = console.input('[bold red]API HASH:[/] ')
        sms_activate_key = console.input('[bold red]SMS ACTIVATE KEY:[/] ')
        my_file = open("sessions/config_api.py", "w+")
        my_file.write(f'api_id = {api_id}\napi_hash = "{api_hash}"\nsms_activate_key = "{sms_activate_key}"\n')
        my_file.close()
        sys.exit()

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
