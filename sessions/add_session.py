from pyrogram import Client

import random
import asyncio
import string
import glob
import os, sys
import json, toml

import shutil

from rich.console import Console

if not os.path.exists("dead"):
    os.mkdir("dead")

console = Console()

console.print("Number of files: %d" % len(glob.glob("*.session")))

console.print(
    "[1] Create a session",
    "[2] Checking the session for validity",
    sep="\n",
    style="bold white"
)
menu = input("> ")

if not os.path.exists("sessions.json"):
    with open("sessions.json", "w") as file:
        data = dict(storage_sessions=[])
        json.dump(data, file, indent=4)

with open("../config.toml") as file:
    config = toml.load(file)["session"]

api_id = config["api_id"]
api_hash = config["api_hash"]

name = "".join(random.choices(string.ascii_letters, k=10))

def get_sessions():
    for sessions in glob.glob("*.session"):
        yield sessions.split(".")[0]

if menu == "1":
    with Client(
        name, 
        api_id, 
        api_hash
    ) as session:
        me = session.get_me()
        string = session.export_session_string()

        console.print(me.first_name, style="bold green")

        with open("sessions.json", "r") as file:
            data = json.load(file)

        with open("sessions.json", "w") as file:
            data.get("storage_sessions").append(string)
            json.dump(data, file, indent=4)

elif menu == "2":
    data = dict(storage_sessions=[])
    ids = []
    for session in get_sessions():
        console.print("Session name -> {}".format(session))

        name_session = "%s.session" % session
        session = Client(session, api_id, api_hash)

        try:
            session.start()
            me = session.get_me()
            string = session.export_session_string()

        except Exception as error:
            console.print("Error : {}".format(error), style="bold red")
            shutil.move(name_session, "dead")

        else:
            if me.id in ids:
                console.print("[bold red]Such an account already exists!")
            else:
                ids.append(me.id)
                data.get("storage_sessions").append(string)
            
            console.print(
                "Account: ({}, {})"
                .format(me.first_name, me.phone_number)
            )
            session.stop()

    with open("sessions.json", "w") as file:
        json.dump(data, file, indent=4)