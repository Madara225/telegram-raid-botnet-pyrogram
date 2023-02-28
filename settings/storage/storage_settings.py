import os, sys
import inspect
import importlib.util
import toml

from rich.console import Console
from settings.registration import Registration

console = Console()

class Settings:
    
    def __init__(self):
        if not os.path.exists("config.toml"):
            Registration().get_settings()
            sys.exit()

        with open("config.toml", encoding="utf-8") as file:
            config = toml.load(file)

        self.api_hash = config["session"]["api_hash"]
        self.api_id = config["session"]["api_id"]
        self.my_id = config["session"]["my_id"]
        self.names = config["session"]["names"]

        self.messages = config["flood"]["messages"]
        self.message_count = config["flood"]["message_count"]
        self.trigger = config["flood"]["trigger"]

    def get_functions(self):
        path = "functions"
        functions = sorted([file[:-3] for file in os.listdir(path) if file.endswith(".py")])

        return self.load_functions(path, functions)

    def load_functions(self, path, functions):
        for function in functions:
            try:
                function = importlib.import_module(f"{path}.{function}")
                for _, classobj in inspect.getmembers(function, inspect.isclass):
                    if path in classobj.__module__ and not classobj.__doc__ is None:
                        yield classobj

            except Exception as error:
                console.log("Error : {}".format(error), style="bold")