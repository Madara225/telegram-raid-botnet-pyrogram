from functions.flood import FloodChat
from settings.function import SettingsFunction

class FloodSettings(SettingsFunction):
    """Flood to chat"""

    def __init__(self, sessions):
        flood = FloodChat(sessions)
        flood.ask()

        flood.start_process_flood()
