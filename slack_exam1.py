#-*- coding: utf-8 -*-
import sys
import time 
import json
import tornado.websocket
from tornado import gen
import Queue

import slack_msg
import misaka
import HanmeThr
from SLACK_URL import *

LISTEN_URL = ""
#POST_URL = misaka.POST_URL#"https://slack.com/api/chat.postMessage"
#CHANNEL_LIST_URL = misaka.CHANNEL_LIST_URL#"https://slack.com/api/channels.list"


#GLOBAL_SHIT = False

@gen.coroutine
def connection_and_waiting():
	print("LISTEN_URL : " + LISTEN_URL)
	client = yield tornado.websocket.websocket_connect(LISTEN_URL)
	#client.write_message("testing from client")
	print(">>>>>>>>");
	
	channel_misaka = {}
	
	# han = HanmeThr.Hanme()
	# han.setDaemon(True)
	# han.start()
	# HanmeThr.han_play = False

	while True:
		msg = yield client.read_message()
		#print("msg is : %s" % msg)
		event_infos = json.loads(msg)
	

		if event_infos['type'] == "hello":
			data_values = {'token' : TOKEN }
						
			k = slack_msg.postMessage(CHANNEL_LIST_URL, data_values)
			channel_info = json.loads(k.read())
			for c in channel_info['channels']:
				print(c['id'])
				channel_misaka[c['id']] = misaka.Misaka();
				channel_misaka[c['id']].setDaemon(True)
				channel_misaka[c['id']].start()
			#print(channel_misaka)
			
		if event_infos['type'] == "message" and 'user' in event_infos:
			
			if event_infos['text'] == "!all kill":
				exit()
				for c in channel_misaka.keys():
					if channel_misaka[c].shit :
						channel_misaka[c].queue.put(event_infos)
						channel_misaka[c].queue.join()
				
				break;
			elif event_infos['text'] == "!turn on":
				channel = event_infos['channel']
				event_infos['text'] = "미사카 에코"
				channel_misaka[channel].queue.put(event_infos)
			elif event_infos['text'] == "!turn off":
				channel = event_infos['channel']
				event_infos['text'] = "미사카 닥쳐"
				channel_misaka[channel].queue.put(event_infos)
			else:
				channel = event_infos['channel']
				channel_misaka[channel].queue.put(event_infos)


if __name__ == "__main__":
	reload(sys)
	sys.setdefaultencoding('utf-8')
	rtm_url = "https://slack.com/api/rtm.start"
	values = {'token' : TOKEN}

	response = slack_msg.postMessage(rtm_url, values)
	# data = urllib.urlencode(values)
	# req = urllib2.Request(rtm_url, data)
	# response = urllib2.urlopen(req)


	the_path = response.read()
	print(">>" + the_path)
	JS = json.loads(the_path)
	print(">>" + JS['url'])
	LISTEN_URL = JS['url']
	print()

	tornado.ioloop.IOLoop.instance().run_sync(connection_and_waiting)

	HanmeThr.log_queue.join()
