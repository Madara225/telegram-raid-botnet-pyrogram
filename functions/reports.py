from pyrogram import Client
from pyrogram import raw
from rich.console import Console, Theme
import asyncio

from settings.function import SettingsFunction
from settings.config import color_number

console = Console(theme=Theme({"repr.number": color_number}))

class Reports(SettingsFunction):
    """Report post"""

    def __init__(self, sessions):
        self.sessions = sessions

        self.account_count()

        reasons = (
            ("Report for child abuse.", raw.types.InputReportReasonChildAbuse()),
            ("Report for copyrighted content.", raw.types.InputReportReasonCopyright()),
            ("Report for illegal drugs.", raw.types.InputReportReasonIllegalDrugs()),
            ("Other.", raw.types.InputReportReasonOther()),
            ("Report for divulgation of personal details.", raw.types.InputReportReasonPersonalDetails()),
            ("Report for pornography.", raw.types.InputReportReasonPornography()),
            ("Report for spam.", raw.types.InputReportReasonSpam()),
            ("Report for violence.", raw.types.InputReportReasonViolence())
        )

        for index, reason in enumerate(reasons, 1):
            console.print(
                "[bold][{}] {}[/]"
                .format(index, reason[0])
            )
        reason_type = reasons[int(console.input(">> "))-1]

        peer, msg_id = self.ids(console.input("[bold red]link post: "))
        comment = console.input("[bold red]comment> ")

        asyncio.get_event_loop().run_until_complete(
            asyncio.gather(*[
                self.send_report(session, peer, msg_id, comment, reason_type)
                for session in self.sessions
            ])
        )

    async def send_report(
        self, session: Client, 
        peer: int, 
        msg_id: int, 
        comment: str, 
        reason_type: tuple
    ):
        await self.launch(session)

        try:
            await session.invoke(
                raw.functions.messages.Report(
                    peer=await session.resolve_peer(peer),
                    id=[msg_id],
                    reason=reason_type[1],
                    message=comment
                )
            )

        except Exception as error:
            console.print("Error : [red]{}".format(error), style="bold")

        else:
            console.print("Report sent successfully!", style="bold green")