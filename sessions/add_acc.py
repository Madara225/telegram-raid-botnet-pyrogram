import glob
import json
import os
import random
import string
from asyncio import *

import requests
from pyrogram import *
from rich.console import Console

from config_api import api_hash, api_id, sms_activate_key

console = Console()

menu = input('''
[1] create an account
[2] add an account to the botnet
[3] checking the session for validity
>> ''')

data = {"storage_sessions": []}

if menu == '1':
    sub_menu = input('''
    [1] add existing account
    [2] create new account (5sim.net)
    >> ''')
    if sub_menu == '1':
        name = "".join(random.choices(string.ascii_letters, k=10))
        app = Client(name, api_id, api_hash)
        with app:
            me = app.get_me()
            print([me.first_name])
    elif sub_menu == '2':
        count = int(input('''
Register Count 
>> '''))
        registered = 0
        while registered != count:
            global buy_account

            buy_account = requests.get('https://5sim.net/v1/user/buy/activation/russia/any/tele', headers={
                'Authorization': 'Bearer ' + sms_activate_key,
                'Accept': 'application/json',
            }).text
            
            buy_account = json.loads(buy_account)
            Client(
                api_id=api_id,
                api_hash=api_hash,
                name=buy_account['phone'],
                phone_number=buy_account['phone']
            ).start()
            
            registered += 1

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
