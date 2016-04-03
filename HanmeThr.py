#-*- coding: utf-8 -*-

import time
import threading #Thread, Lock
import Queue
import slack_msg
from SLACK_URL import *
import random

# count = 10
# lock = threading.Lock()

# han_play = False;
# log_queue = Queue.Queue();

class Hanme(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.queue = Queue.Queue()
		self.state = 0 # 0: standby 1: start
		self.score = {}
		self.cur_prob = ""
		f = open("StarInNight.txt", "r")
		self.prob = f.readlines()

		f.close()
		#for l in f.readlines():
		#	self.prob[self.total_idx] = l
		#	self.total_idx += 1

	def run(self):
		while True:
			log_data = self.queue.get()
			print("::::%s : %s" % (log_data['user'], log_data['text']))
			
			event_channel = log_data['channel']
			event_user = log_data['user']
			event_text = log_data['text']
			
			if self.state == 0 and "미사카 전투 시작" in log_data['text']:
				#
				#	generate problem
				#	make problem string
				#	using python random
				#
				#prob = self.prob[1].encode("utf-8")
				self.state = 1
				self.cur_prob = random.choice(self.prob) #self.prob[random.random() % total_idx]
				msg = (" =>" + self.cur_prob)
				data_values = slack_msg.makeMsgForm(channel = event_channel, 
										text = msg)
				slack_msg.postMessage(POST_URL, data_values) 

			elif self.state == 1 and "미사카 문제 다시" in log_data['text']:
				self.cur_prob = random.choice(self.prob)
				msg = (" =>" + self.cur_prob)
				data_values = slack_msg.makeMsgForm(channel = event_channel, 
										text = msg)
				slack_msg.postMessage(POST_URL, data_values) 
			
			elif self.state == 1 and "미사카 한메 정산" in log_data['text']:
				
				msg = "----------------\n"
				for i in self.score.keys():
					msg += ("%s : %d\n" % (i, self.score[i]))
				msg += "----------------"
				data_values = slack_msg.makeMsgForm(channel = event_channel, 
										text = msg)
				slack_msg.postMessage(POST_URL, data_values) 
				self.state = 0
				self.score.clear()

			elif self.state == 1 and log_data['text'] in self.cur_prob:
				if log_data['user'] in self.score :
					self.score[log_data['user']] += 1
				else:
					self.score[log_data['user']] = 1

				self.cur_prob = random.choice(self.prob)
				msg = "misaka : %s = %d (+1).\n =>" % (log_data['user'], self.score[log_data['user']])
				msg += self.cur_prob
				data_values = slack_msg.makeMsgForm(channel = event_channel,
										text = msg)
				slack_msg.postMessage(POST_URL, data_values)

			elif self.state == 1 and log_data['text'] not in self.cur_prob:
				msg = "misaka : %s 오답!! 땡!!!\n =>" % (log_data['user'])
				msg += self.cur_prob
				data_values = slack_msg.makeMsgForm(channel = event_channel,
										text = msg)
				slack_msg.postMessage(POST_URL, data_values)


			
			self.queue.task_done()
			#
			#	game stop case
			#
"""계절이 지나가는 하늘에는
가을로 가득 차 있습니다.

나는 아무 걱정도 없이
가을 속의 별들을 다 헬 듯합니다.

가슴속에 하나 둘 새겨지는 별을
이제 다 못 헤는 것은
쉬이 아침이 오는 까닭이요,
내일 밤이 남은 까닭이요,
아직 나의 청춘이 다하지 않은 까닭입니다.

별 하나에 추억과
별 하나에 사랑과
별 하나에 쓸쓸함과
별 하나에 동경과
별 하나에 시와
별 하나에 어머니, 어머니,

어머님, 나는 별 하나에 아름다운 말 한마디씩 불러 봅니다. 소학교 때 책상을 같이 했던 아이들의 이름과, 패, 경, 옥, 이런 이국 소녀들의 이름과, 벌써 아기 어머니 된 계집애들의 이름과, 가난한 이웃 사람들의 이름과, 비둘기, 강아지, 토끼, 노새, 노루, '프랑시스 잠[1]', '라이너 마리아 릴케[2]' 이런 시인의 이름을 불러 봅니다.

이네들은 너무나 멀리 있습니다.
별이 아스라이 멀듯이.

어머님,
그리고 당신은 멀리 북간도에 계십니다.

나는 무엇인지 그리워
이 많은 별빛이 내린 언덕 위에
내 이름자를 써 보고
흙으로 덮어 버리었습니다.

딴은 밤을 새워 우는 벌레는
부끄러운 이름을 슬퍼하는 까닭입니다.

그러나 겨울이 지나고 나의 별에도 봄이 오면
무덤 위에 파란 잔디가 피어나듯이
내 이름자 묻힌 언덕 위에도
자랑처럼 풀이 무성할 게외다."""