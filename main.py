from robot import Robot
import alexia
import time
from threading import Thread

from wikiRobot import wikibot
from rec3 import *
from textToVoice import *

import random

FRASES_DUDA={0:"I dont understand",1:"what?",2:"sorry?",3:"could you repeat, please?"}
QUICK_ANSWERS={"hello":"hello","thank you":"you are welcome","thanks": "you are welcome","bye":"bye","hi":"hi","hey":"hey"}

FRASES_PASO={0:"wow, slow down, what do you want to know?",1:"okay, this is what i know, tell me one ",2:"this is what i can tell you"}

YAWN_PHRASES={0:"Are you tired?",1:"looks like you should rest",2:"I see you yawn, maybe you should rest",3:"""I am tired too, lets take a rest"""}

SLEEP_PHRASES={0: "Please, open your eyes",1:"Are you asleep?",2:"Your eyes are closed, It is very risky while you are driving",3:"""open your eyes if you do not want to kill us!"""}
ATTENTION_PHRASES={0:"Please, look forward!",1:"Whereare you looking at?",2:"Do not get distracted!"}

MAX_ALERT_TIME=5

class Application:

	text=""
	def __init__(self):
		self.status="idle"
		self.robot=Robot()
		self.ended=False
		self.wiki=wikibot()
		self.voice=textRecognitor()
		self.wiki.getConcept("hackathon")
		self.voice.textToVoice("Hello, my name is Alexia")


		self.alertTime=MAX_ALERT_TIME
		self.alerting=False


		self.init()
		
	
	def init(self):
		
		t = Thread(target=self.loop)
		t.deamon = True
		#self.loop()
		t.start()
		t = Thread(target=alexia.callJoke)
		t.deamon = True
		#self.loop()
		t.start()
		self.robot.initRecognition()
		pass

	def loop(self):
		while(not self.ended):
			#print(self.robot.asleep)
			#print(self.robot.faceDirection)
			if(self.robot.head_moving==1):
				print("YES")

			if(self.robot.head_moving==-1):
				print("NO")	

			if(self.alerting==True and self.alertTime>0):
				self.alertTime-=1
				continue
			
			
			if(self.robot.yawning):
				self.voice.textToVoice(random.choice(YAWN_PHRASES))
				self.alerting=True
				self.alertTime=MAX_ALERT_TIME
			elif(self.robot.asleep):
				self.voice.textToVoice(random.choice(SLEEP_PHRASES))
				self.alerting=True
				self.alertTime=MAX_ALERT_TIME
			"""elif(not self.robot.visible):
				self.voice.textToVoice(random.choice(ATTENTION_PHRASES))
				self.alerting=True
				self.alertTime=MAX_ALERT_TIME
				self.robot.deactivateAlert()	"""
			if(self.robot.ended):
				alexia.destr()
				return
			
			time.sleep(1)





Application()