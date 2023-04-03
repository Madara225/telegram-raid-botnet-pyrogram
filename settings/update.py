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

        packages = ["install", "-r", "requirements.txt", "--quiet"]

        try:
            if float(pip.__version__[:-2]) >= 23.0:
                pip.main(packages+["--break-system-packages"])
            else:
                pip.main(packages)

        except Exception as error:
            console.log(error)

def get_commit() -> None | bool:
    try:
        repo = git.Repo()
        local_hash = repo.heads[0].commit.hexsha
        server_hash = git.Remote(repo, "origin").fetch()[0].commit.hexsha

    except Exception as error:
        console.log("Error : %s" % error, style="bold white")

    else:
        if local_hash == server_hash:
            return True
        
        if console.input("Update? (y/n): ") == "y":
            update()