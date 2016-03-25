#-*- coding: utf-8 -*-

import urllib
import urllib2
import time 
import json
import tornado.websocket
from tornado import gen

LISTEN_URL = ""
POST_URL = "https://slack.com/api/chat.postMessage"

def postMessage(url, value):
	data = urllib.urlencode(value)
	req = urllib2.Request(url, data)
	response = urllib2.urlopen(req)
	return response

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
						'text' : "",
						'username' : 'misaka',
						'icon_url' : 'http://cfile5.uf.tistory.com/image/2375064056F2AA581BABEC',
						'as_user' : 'false'}
			data_values['text'] = '미사카! 출격합니다!'
			
			if event_text == "!turn off":
				data_values['text'] = "미사카 미코토! 종료합니다!"
				postMessage(POST_URL, data_values)
				exit()
				break;

			miko_mention = '미사카는 \'' + event_text.encode('utf-8') + '\'이라고 에코합니다.'
			data_values['text'] = miko_mention
			postMessage(POST_URL, data_values)


if __name__ == "__main__":
	rtm_url = "https://slack.com/api/rtm.start"
	values = {'token' : 'tokenkey'}

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

