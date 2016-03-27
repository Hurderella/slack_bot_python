#-*- coding: utf-8 -*-

import urllib
import urllib2
import misaka

def makeMsgForm(**kargs):
	data_values = {
		'token' : misaka.TOKEN,
		'channel' : 'nil',
		'text' : 'Hello World',
		'username' : misaka.USER_NAME,
		'icon_url' : misaka.ICON_URL,
		'as_user' : 'false'
	}
	for key, word in kargs.iteritems():
		data_values[key] = word
	return data_values


def postMessage(url, value):
	data = urllib.urlencode(value)
	req = urllib2.Request(url, data)
	response = urllib2.urlopen(req)
	return response
