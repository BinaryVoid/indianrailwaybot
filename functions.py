from urllib2 import urlopen
import config
import json
import telepot

#########VARIABLES##############

site = 'http://api.railwayapi.com/'
bot = telepot.Bot(config.telegram_key)
railkey = config.railway_key


##########VARIABLES END#########

def on_between_request(msg):

	invalid_msg = """Invalid command. 
/between helps you find trains between two stations.
The right format is: 
_/between <source-code> <dest-code> <date>_
*Eg*: /between ndls bct 17-02
Try /help for more"""
	
	final_data = []
	if len(msg['text'].split(" ")) != 4:
		bot.sendMessage(msg['chat']['id'], invalid_msg, parse_mode = 'Markdown')
		return 0
	source = msg['text'].split(" ")[1]
	dest = msg['text'].split(" ")[2]
	date = msg['text'].split(" ")[3]
	response = urlopen(site + 'between/source/' + source + '/dest/' + dest + '/date/' + date + '/apikey/' + railkey)
	data = json.load(response)
	for i in range(len(data["train"])):

		dday = data['train'][i]['days']
		running_days = ""
		for j in range(len(dday)):
			ddays = dday[j]
			if ddays['runs'] == 'Y':
				running_days += "*" + ddays['day-code'][0] + "* "
			if ddays['runs'] == 'N':
				running_days += ddays['day-code'][0] + " "

		a = "*" + str(data['train'][i]['no']) + "*. " + data['train'][i]['number'] + " " + data['train'][i]['name'] + "  " + data['train'][i]['from']['code'] + "-->" + data['train'][i]['to']['code'] + "\n"
		b = running_days + "\n"
		c = "Source departure:*" + data['train'][i]['src_departure_time'] + "* Destination Arrival: *" + data['train'][i]['dest_arrival_time'] + "* Travel Time:*" + data['train'][i]['travel_time'] + "*" + "\n"
		final_data.append(a + b + c)
	xxx = "\n".join(final_data)
	try:
		bot.sendMessage(telepot.glance(msg)[2], xxx, parse_mode = 'Markdown')
	except:
		bot.sendMessage(telepot.glance(msg)[2], "No trains", parse_mode = 'Markdown')

def on_pnr_request(msg):
	
	invalid_msg = """Invalid command. 
/pnr helps you check your pnr status.
The right format is: 
*Eg*: /pnr 1234567890
Try /help for more
"""

	if len(msg['text'].split(" ")) != 2:
		bot.sendMessage(msg['chat']['id'], invalid_msg, parse_mode = 'Markdown')
		return 0
	pnr = msg['text'].split(" ")[1]
	response = urlopen(site + 'pnr_status/pnr/' + pnr + '/apikey/' + railkey)
	data = json.load(response)
	data = pnrdata
	pnr = data['pnr']
	train_name = data['train_name']
	train_num = data['train_num']
	doj = data['doj']
	class_name = data['class']
	dest_code = data['reservation_upto']['code']
	dest_name = data['reservation_upto']['name']
	src_code = data['from_station']['code']
	src_name = data['from_station']['name']

	a1 = "train number: *" + train_num + "*\n"
	a2 = "train name: *" + train_name + "*\n" 
	a3 = "date: *" + doj + "*\n"
	a = a1 + a2 + a3
	b = "Source Station: *" + src_name + "(" + src_code + ")*"
	c = "Destination Station: *" + dest_name +  "(" + dest_code + ")*"
	print a
	print b
	print c
	pas = data['passengers']
	pass_details = []
	for i in range(len(pas)):
		current_status = pas[i]['current_status']
		booking_status = pas[i]['booking_status']
		no = pas[i]['no']
		pass_data = "*" + str(no) + ". " + booking_status + " " + current_status + "*"
		pass_details.append(pass_data)
	xxx = "\n".join(pass_details)
	d = "\nDetails of all the passengers: \n"
	final_response = "*" + pnr + "*\n" + a + "\n" + b + "\n" + c + "\n" + d + xxx
	try:
		bot.sendMessage(telepot.glance(msg)[2], final_response, parse_mode = 'Markdown')
	except:
		bot.sendMessage(telepot.glance(msg)[2], "PNR flushed", parse_mode = 'Markdown')

