#-*- coding: utf-8 -*-

import urllib
import urllib2
import time
import tornado.websocket
from tornado import gen
#import urllib.request as urllib2
#xoxb-27393677335-RrnsR3aCwbj89hJrPUUNAv2y
###

#url = "wss://mpmulti-49gs.slack-msgs.com/websocket/CGP-T3zk5ftpFnENVddLxAt7ZutgphoVpoL-8Yp4Wk2Ojvj7vj5wNIHLryrR1bGqqdwDAQRuJWML1SyHRF-06_RUKwUFNMquxk32sVlk38f1dhl7pdZGJLqXF8EuTNdy8lgO48YsHk1uFh0KDqDk5A=="
"""url = "wss://echo.websocket.org"

client = tornado.websocket.websocket_connect(url)

while True:
	msg = client.read_message()
	print("msg is %s" % msg)
	time.sleep(1)
"""

url = "wss://mpmulti-n2p4.slack-msgs.com/websocket/xdGSyVb6UTAEudLvTOmWWIChMZSxR6mwkyqTKjl6ILVmuSGsQJ2RVRyTqhxc7hG4QMPQZMOuXR4cYBdi9GgAcDhfUKOhbAQdlPsKrFuvr0aloN69geTZ8IoTE-94ecv7nn5EseYqiKTevIzIqqR3Ag=="

@gen.coroutine
def test_ws():
	client = yield tornado.websocket.websocket_connect(url)
	#client.write_message("testing from client")
	while True:
		msg = yield client.read_message()
		print("msg is : %s" % msg)


if __name__ == "__main__":
	tornado.ioloop.IOLoop.instance().run_sync(test_ws)