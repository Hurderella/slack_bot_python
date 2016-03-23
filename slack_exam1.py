#-*- coding: utf-8 -*-

import urllib
import urllib2
import time 
import json
import tornado.websocket
from tornado import gen

URL = ""

@gen.coroutine
def connection_and_waiting():
	print("URL : " + URL)
	client = yield tornado.websocket.websocket_connect(URL)
	#client.write_message("testing from client")
	while True:
		msg = yield client.read_message()
		print("msg is : %s" % msg)

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
	URL = JS['url']
	print()

	tornado.ioloop.IOLoop.instance().run_sync(connection_and_waiting)

