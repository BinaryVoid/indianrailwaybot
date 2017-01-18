import telepot
from pprint import pprint
import config, functions

bot = telepot.Bot(config.telegram_key)
railkey = config.railway_key

def on_msg(msg):
	if msg['text'].startswith("/"):
		if msg['text'].split(" ")[0] == "/between":
			functions.on_between_request(msg)
		elif msg['text'].split(" ")[0] == "/pnr":
			functions.on_pnr_request(msg)
	else:
		bot.sendMessage(msg['chat']['id'], "Enter a valid command")

bot.message_loop({'chat': on_msg},	
				 run_forever='Listening ...')


