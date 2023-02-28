from rich.console import Console
import toml

console = Console()

class Registration:

    def get_settings(self):
        console.rule("Session")
        api_id, api_hash, my_id, names = self.setup_session()

        console.rule("Flood")

        trigger, message_count, messages = self.setup_flood()

        self.save(
            api_id,
            api_hash,
            my_id,
            trigger,
            message_count,
            messages,
            names
        )

    def setup_session(self):
        api_id = int(console.input("[bold red]API_ID: [/]"))
        api_hash = console.input("[bold red]API_HASH: [/]")

        my_id = int(console.input("[bold red]ID (main account id): [/]"))

        print()

        console.print(
            "Enter account names",
            style = "bold red"
        )

        names = []
        while name := console.input("[bold white]>> [/]"):
            names.append(name)      

        return api_id, api_hash, my_id, names

    def setup_flood(self):
        trigger = console.input("[bold yellow]message to start flooding: [/]")
        message_count = int(console.input("[bold yellow]number of messages> [/]"))

        print()

        console.print(
            "Enter flood messages text",
            style = "bold green"
        )

        messages = []
        while message := console.input("[bold white]>> [/]"):
            messages.append(message)

        return trigger, message_count, messages

    def save(
        self,
        api_id,
        api_hash,
        my_id,
        trigger,
        message_count,
        messages,
        names
    ):

        config = dict(
            session = dict(
                api_hash = api_hash,
                api_id = api_id,
                my_id = my_id,
                names = names
            ),

            flood = dict(
                message_count = message_count,
                trigger = trigger,
                messages = messages
            )
        )

        with open("config.toml", "w") as file:
            toml.dump(config, file)

        console.rule("[bold white]Happy use! https://t.me/sower_qq :)[/]")
        console.print("[bold white]Run the file again.[/]")
