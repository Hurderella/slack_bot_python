#-*- coding: utf-8 -*-

import time
import threading #Thread, Lock
import Queue
import slack_msg
import HanmeThr
from SLACK_URL import *

class Misaka(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.queue = Queue.Queue()
		self.shit = True;
	
	def run(self):
		han = HanmeThr.Hanme()
		han.setDaemon(True);
		han.start()

		while(True):
			event_infos = self.queue.get()
			
			event_type = event_infos['type']
			if event_type == "message" and 'user' in event_infos:
				event_channel = event_infos['channel']
				event_user = event_infos['user']
				event_text = event_infos['text']
				
				print("[%s] [%s] [%s] [%s]" % (event_infos['type'], event_infos['channel'],
					event_infos['user'], event_infos['text']))
				data_values = slack_msg.makeMsgForm(channel = event_channel)
				
				if "미사카" in event_text :
					if "닥쳐" in event_text or "시끄러" in event_text:
						data_values['text'] = '미사카는 닥칩니다.'
						slack_msg.postMessage(POST_URL, data_values)
						self.shit = True
					elif "에코" in event_text:
						#GLOBAL_SHIT = False
						data_values['text'] = '미사카는 에코 합니다.'
						slack_msg.postMessage(POST_URL, data_values)
						self.shit = False
					elif "전투" in event_text:
						if han.state == 0 :
							data_values['text'] = '미사카 전투 돌입합니다. 종목은 한메 타자.'
							slack_msg.postMessage(POST_URL, data_values)
							event_infos['text'] = '미사카 전투 시작'
							self.shit = True
							han.queue.put(event_infos)
						# HanmeThr.han_play = True;
					elif "문제 다시" in event_text or "문제다시" in event_text:
						event_infos['text'] = '미사카 문제 다시'
						han.queue.put(event_infos)
					elif "한메 정산" in event_text:
						event_infos['text'] = '미사카 한메 정산'
						han.queue.put(event_infos)
						
						

				elif self.shit == False:
					miko_mention = '미사카는 \'' + event_text + '\'이라고 에코합니다.'
					data_values['text'] = miko_mention	
					slack_msg.postMessage(POST_URL, data_values)

				elif han.state != 0 :
					han.queue.put(event_infos)
			# 	if HanmeThr.han_play == True:
			# 		data_values['text'] = event_text
			# 		HanmeThr.log_queue.put(data_values)
