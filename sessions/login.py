from pyrogram import Client, idle

app = Client(input("Name session>> "))

app.start()

me = app.get_me()

print(me.phone_number, me.first_name)

@app.on_message()
async def my_handler(client, message):
	print(message.text)

idle()
