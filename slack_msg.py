#-*- coding: utf-8 -*-

import urllib
import urllib2
from SLACK_URL import *

def makeMsgForm(**kargs):
	data_values = {
		'token' : TOKEN,
		'channel' : 'nil',
		'text' : 'Hello World',
		'username' : USER_NAME,
		'icon_url' : ICON_URL,
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
