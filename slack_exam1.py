#-*- coding: utf-8 -*-
import sys
import time 
import json
import tornado.websocket
from tornado import gen

from slack_msg import * 
import misaka

LISTEN_URL = ""
POST_URL = "https://slack.com/api/chat.postMessage"
CHANNEL_LIST_URL = "https://slack.com/api/channels.list"


#GLOBAL_SHIT = False

@gen.coroutine
def connection_and_waiting():
	print("LISTEN_URL : " + LISTEN_URL)
	client = yield tornado.websocket.websocket_connect(LISTEN_URL)
	#client.write_message("testing from client")
	print(">>>>>>>>");
	channel_id_list = {}
	while True:
		msg = yield client.read_message()
		print("msg is : %s" % msg)
		event_infos = json.loads(msg)
		event_type = event_infos['type']
		
		if event_type == "hello":
			data_values = {'token' : misaka.TOKEN }
						
			k = postMessage(CHANNEL_LIST_URL, data_values)
			channel_info = json.loads(k.read())
			for c in channel_info['channels']:
				print(c['id'])
				channel_id_list[c['id']] = False;
			print(channel_id_list)

		if event_type == "message" and 'user' in event_infos:
			event_channel = event_infos['channel']
			event_user = event_infos['user']
			event_text = event_infos['text']
			
			print("[%s] [%s] [%s] [%s]" % (event_infos['type'], event_infos['channel'],
				event_infos['user'], event_infos['text']))
			data_values = makeMsgForm(channel = event_channel)
			
			#global GLOBAL_SHIT
			if "미사카" in event_text :
				if "닥쳐" in event_text or "시끄러" in event_text:
					#GLOBAL_SHIT = True
					data_values['text'] = '미사카는 닥칩니다.'
					postMessage(POST_URL, data_values)
					channel_id_list[event_channel] = True
				elif "에코" in event_text:
					#GLOBAL_SHIT = False
					data_values['text'] = '미사카는 에코 합니다.'
					postMessage(POST_URL, data_values)
					channel_id_list[event_channel] = False
				elif "전투" in event_text:
					data_values['text'] = '미사카 전투 돌입합니다. 종목은 XXXX.'
			elif event_text == "!turn off":
				data_values['text'] = "미사카 미코토! 종료합니다!"
				postMessage(POST_URL, data_values)
				exit()
				break;
			elif channel_id_list[event_channel] == False:
				print(channel_id_list)
				miko_mention = '미사카는 \'' + event_text + '\'이라고 에코합니다.'
				data_values['text'] = miko_mention	
				postMessage(POST_URL, data_values)


if __name__ == "__main__":
	reload(sys)
	sys.setdefaultencoding('utf-8')
	rtm_url = "https://slack.com/api/rtm.start"
	values = {'token' : misaka.TOKEN}

	response = postMessage(rtm_url, values)
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

