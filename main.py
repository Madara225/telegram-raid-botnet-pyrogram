import sys
from sys import platform
from rich.console import Console, Theme

from settings.storage.storage_settings import Settings
from settings.update import execute
from settings.config import color_number
from settings.storage.storage_sessions import ConnectSessions

console = Console(theme=Theme({"repr.number": color_number}))

if platform == "win32":
    console.print("[bold red]The script will work with errors (use linux or WSL).")

console.print(
    "GitHub botnet on pyrogram: https://github.com/Madara225/telegram-raid-botnet-pyrogram",
    "GitHub botnet on telethon: https://github.com/json1c/telegram-raid-botnet",
    sep="\n",
    style="bold white"
)

print()

execute()

functions = list(Settings().get_functions())
accounts = ConnectSessions()

def main():
    console.print("[bold]botnet accounts >> %d[/]" % len(accounts.sessions))

    for index, function in enumerate(functions, 1):
        console.print(
            "[bold][{color}][{num}][/] {name}[/]"
            .format(color=color_number, num=index, name=function.__doc__.lower())
        )

    print()

    return functions[int(console.input(">> "))-1]

while True:
    try:
        function = main()
        function(accounts.sessions)

    except KeyboardInterrupt:
        console.print("\n<https://t.me/sower_telegram>")
        sys.exit()

    except Exception as error:
        console.print(error)

    finally:
        print("Done.")
