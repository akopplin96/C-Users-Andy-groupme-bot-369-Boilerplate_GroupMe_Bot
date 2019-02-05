# RESOURCE: http://www.apnorton.com/blog/2017/02/28/How-I-wrote-a-Groupme-Chatbot-in-24-hours/


# IMPORTS
import os
import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from flask import Flask, request

import csv
import math
import numpy

app = Flask(__name__)
bot_id = "7e7227e09435e736f9a9633e93"

# Called whenever the app's callback URL receives a POST request
# That'll happen every time a message is sent in the group

@app.route('/', methods=['POST'])
def webhook():
	# 'message' is an object that represents a single GroupMe message.
	message = request.get_json()

	#message['text']  = '#BP Andy beat Michael'
	#########################################################################################
	#Bot Logic


	#Checks if bot has been named directly
	reply_requested = 0

	if '#toggaf' in message['text'].lower() and not sender_is_bot(message): # if message bot name
		reply_requested = 1


	if reply_requested == 1 and 'hi' in message['text'].lower() and not sender_is_bot(message): # if message contains 'penis', ignoring case, and sender is not a bot...
			reply('wassup')

	if 'indian' == message['text'].lower() and not sender_is_bot(message): # if message contains 'penis', ignoring case, and sender is not a bot...
		reply('bobs and vagene')

	if who_dis(message['text']) != 'home slice' and not sender_is_bot(message):
		reply(who_dis(message['text']))


	if '#BP' in message['text']:
		Retrieve_competitor_scores(competitors)

		if 'beat' in message['text']:
			names = message['text'].split('beat')
			name1=names[0]
			name1=name1.replace('#BP ','')
			name2 = name1.strip()
			name3 = names[1].strip()

			EloSystem(name2,name3,30,1)

			write_competitor_scores()

			reply('read ya loud and clear')
		
		else: reply('whoopsie')


	return "ok", 200

################################################################################

#Important Functions and Dictionaries

# Checks whether the message sender is a bot
def sender_is_bot(message):
	return message['sender_type'] == "bot"

def sent_to_words(msg):
	words= msg.split(' ')
	return words


competitors = ['Andy', 'Michael', 'Andrew', 'Chris', 'Gabe', 'Ethan', 'Demetri', 'Tim', 'Karen', 'Celine', 'Danielle', 'Gabbi']
BP_scoreboard = {}

for thing in competitors:
    BP_scoreboard[thing] = 0

#lists for nickname recognition
nicknames_Tim = ['tim', 'timothy', 'mizdrak', 'tmiz']
nicknames_Andy = ['andy', 'kopplin']
nicknames_Michael = ['michael', 'mike', 'krone']
nicknames_Andrew = ['andrew', 'grabowski', 'grabowser', 'bowser']
nicknames_Gabe = ['gabe', 'gabriel', 'olson-mendoza', 'jurg']
nicknames_Chris = ['chris', 'christopher', 'cobb', 'ernie', 'gritz', 'gritz888']
nicknames_Ethan = ['ethan', 'e', 'heick']
nicknames_Demetri = ['demitri', 'demetri', 'demetre', 'dimetri', 'dimitri', 'meech']
nicknames_Danielle = ['danni', 'danielle', 'gomez', 'mvp']
nicknames_Celine = ['celine', 'wysgalla', 'scalene']
nicknames_Karen = ['karen', 'glownia', 'kern', 'krn']
nicknames_Gabbi = ['gabbi', 'gabrielle', 'goob', 'gooby', 'goober', 'goobi', 'bono']

nicknames_master = [nicknames_Tim, nicknames_Andy, nicknames_Celine, nicknames_Chris, nicknames_Danielle, nicknames_Demetri, nicknames_Ethan, nicknames_Gabbi, nicknames_Karen, nicknames_Michael, nicknames_Andrew, nicknames_Gabe]

def who_dis(dis):
	dis_lower = dis.lower()
	if dis_lower in nicknames_Andy:
		return 'Andy'
	elif dis_lower in nicknames_Celine:
		return 'Celine'
	elif dis_lower in nicknames_Chris:
		return 'Chris'
	elif dis_lower in nicknames_Danielle:
		return 'Denielle'
	elif dis_lower in nicknames_Demetri:
		return 'Demetri'
	elif dis_lower in nicknames_Ethan:
		return 'Ethan'
	elif dis_lower in nicknames_Gabbi:
		return 'Gabbi'
	elif dis_lower in nicknames_Karen:
		return 'Karen'
	elif dis_lower in nicknames_Michael:
		return 'Michael'
	elif dis_lower in nicknames_Tim:
		return 'Tim'
	elif dis_lower in nicknames_Andrew:
		return 'Andrew'
	elif dis_lower in nicknames_Gabe:
		return 'Gabe'
	else:
		return 'home slice'



#reads list of scores from csv file
def Retrieve_competitor_scores(competitors):
    reader = csv.reader(open("Beer_Pong.csv", "r"), delimiter=",")
    x = list(reader)
    beer_pong_data = numpy.array(x)

    for item in competitors:
        position = competitors.index(item)

        BP_scoreboard[item] = beer_pong_data[ len(beer_pong_data[:,1])-1,position]
    return BP_scoreboard


def write_competitor_scores():
    write_array=[]
    #writes new list of scores to csv file
    for item in competitors:
        write_array.append(BP_scoreboard[item])

    with open('Beer_Pong.csv','a', newline='') as fd:
        writer = csv.writer(fd)
        writer.writerow(write_array)
	



def Probability(a, b):
    diff = a - b
    return 1.0 / (1.0 + numpy.power(10.0,diff/ 400.0)) 

def EloSystem(player1,player2,K,d):
	Ra = float(BP_scoreboard[player1])
	Rb = float(BP_scoreboard[player2])
  
    # To calculate the Winning 
    # Probability of Player B 
	Pb = Probability(Ra,Rb)
  
    # To calculate the Winning 
    # Probability of Player A 
	Pa = Probability(Rb,Ra)
  
    # Case -1 When Player A wins 
    # Updating the Elo Ratings 
	if (d==1):
		Ra = Ra + K * (1.0 - Pa)
		Rb = Rb + K * (0.0 - Pb)

		BP_scoreboard[player1] = Ra
		BP_scoreboard[player2] = Rb

		return BP_scoreboard
      
  
    # Case -2 When Player B wins 
    # Updating the Elo Ratings 
	else:
		Ra = Ra + K * (0.0 - Pa)
		Rb = Rb + K * (1.0 - Pb)

		BP_scoreboard[player1] = Ra
		BP_scoreboard[player2] = Rb
		return BP_scoreboard



# Send a message in the groupchat
def reply(msg):
	url = 'https://api.groupme.com/v3/bots/post'
	data = {
		'bot_id'		: bot_id,
		'text'			: msg
	}
	request = Request(url, urlencode(data).encode())
	json = urlopen(request).read().decode()

# Send a message with an image attached in the groupchat
def reply_with_image(msg, imgURL):
	url = 'https://api.groupme.com/v3/bots/post'
	urlOnGroupMeService = upload_image_to_groupme(imgURL)
	data = {
		'bot_id'		: bot_id,
		'text'			: msg,
		'picture_url'		: urlOnGroupMeService
	}
	request = Request(url, urlencode(data).encode())
	json = urlopen(request).read().decode()
	
# Uploads image to GroupMe's services and returns the new URL
def upload_image_to_groupme(imgURL):
	imgRequest = requests.get(imgURL, stream=True)
	filename = 'temp.png'
	postImage = None
	if imgRequest.status_code == 200:
		# Save Image
		with open(filename, 'wb') as image:
			for chunk in imgRequest:
				image.write(chunk)
		# Send Image
		headers = {'content-type': 'application/json'}
		url = 'https://image.groupme.com/pictures'
		files = {'file': open(filename, 'rb')}
		payload = {'access_token': 'eo7JS8SGD49rKodcvUHPyFRnSWH1IVeZyOqUMrxU'}
		r = requests.post(url, files=files, params=payload)
		imageurl = r.json()['payload']['url']
		os.remove(filename)
		return imageurl