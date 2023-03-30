import git
from rich.console import Console

console = Console()

def get_commit() -> str:
	try:
		repo = git.Repo()
		local_hash = repo.heads[0].commit.hexsha
		server_hash = git.Remote(repo, "origin").fetch()[0].commit

	except Exception as error:
		console.log("Error : %s" % error, style="bold white")

	else:
		if local_hash == server_hash:
			return True

console.print(get_commit())

