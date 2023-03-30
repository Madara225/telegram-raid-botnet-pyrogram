import git
import requests
import pip
from rich.console import Console

console = Console()

def update():
    with console.status("Update..."):
        repo = git.Repo()
        origin = repo.remote("origin")
        origin.pull()

        try:
            pip.main(["install", "-r", "requirements.txt", "--break-system-packages", "--quiet"])
        except:
            console.log("Try updating the pip.")

def get_commit() -> None | bool:
    try:
        repo = git.Repo()
        local_hash = repo.heads[0].commit.hexsha
        server_hash = git.Remote(repo, "origin").fetch()[0].commit.hexsha

    except Exception as error:
        console.log("Error : %s" % error, style="bold white")

    if local_hash == server_hash:
        console.print("[bold green]Latest commit! :D")
    else:
        update()

def get_version() -> None | bool:
    try:
        server_version = requests.get("https://raw.githubusercontent.com/Madara225/telegram-raid-botnet-pyrogram/master/.version").text.strip()
        with open(".version") as file:
            local_version = file.read().strip()

    except Exception as error:
        console.log("Error : %s" % error, style="bold white")

    if server_version == local_version:
        console.print("[bold green]Versions match.")

    else:
        console.print(
            "[bold red]Versions don't match.[/] Perhaps the server did not have time to update :)"
        )
        console.print(
            "Local version: {local} Server: {server}"
            .format(local=local_version, server=server_version)
        )

def execute():
    console.log("Checking for updates...")
    get_version() 
    get_commit()