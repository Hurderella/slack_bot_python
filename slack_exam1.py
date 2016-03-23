#-*- coding: utf-8 -*-

import urllib
import urllib2
import time 
import json
import tornado.websocket
from tornado import gen

LISTEN_URL = ""
POST_URL = "https://slack.com/api/chat.postMessage"

@gen.coroutine
def connection_and_waiting():
	print("LISTEN_URL : " + LISTEN_URL)
	client = yield tornado.websocket.websocket_connect(LISTEN_URL)
	#client.write_message("testing from client")
	while True:
		msg = yield client.read_message()
		print("msg is : %s" % msg)
		event_infos = json.loads(msg)
		event_type = event_infos['type']
		if event_type == "message" and 'user' in event_infos:
			event_channel = event_infos['channel']
			event_user = event_infos['user']
			event_text = event_infos['text']
			print("[%s] [%s] [%s] [%s]" % (event_infos['type'], event_infos['channel'],
				event_infos['user'], event_infos['text']))
			data_values = {'token' : 'xoxb-27393677335-H3b46NTQxgA8PjBaW0wjScpF',
			'channel' : event_channel,
			'text' : event_text,
			'as_user' : 'false'}
			data = urllib.urlencode(data_values)
			req = urllib2.Request(POST_URL, data)
			response = urllib2.urlopen(req)
			#'text' : '미코토는 \'' + event_text + '\'라고 에코합니다.'}



if __name__ == "__main__":
	rtm_url = "https://slack.com/api/rtm.start"
	values = {'token' : 'tokenkey'}

	data = urllib.urlencode(values)
	req = urllib2.Request(rtm_url, data)
	response = urllib2.urlopen(req)
	#k = 0
	#while k != 5:
	#	the_path = response.read()
	#	print(the_path)
	#	k += 1
	#	time.sleep(5)

	the_path = response.read()
	print(">>" + the_path)
	JS = json.loads(the_path)
	print(">>" + JS['url'])
	LISTEN_URL = JS['url']
	print()

	tornado.ioloop.IOLoop.instance().run_sync(connection_and_waiting)

