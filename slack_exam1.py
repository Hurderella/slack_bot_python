#-*- coding: utf-8 -*-

import urllib
import urllib2
import time 
url = "https://slack.com/api/rtm.start"
values = {'token' : 'xoxb-27393677335-RrnsR3aCwbj89hJrPUUNAv2y'}

data = urllib.urlencode(values)
req = urllib2.Request(url, data)
response = urllib2.urlopen(req)
#k = 0
#while k != 5:
#	the_path = response.read()
#	print(the_path)
#	k += 1
#	time.sleep(5)

the_path = response.read()
print(the_path)

