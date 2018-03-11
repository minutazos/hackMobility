import drowsy
from imutils.video import VideoStream
from threading import Thread
import time

moods=["happy","sad","surprised","neutral","angry"]

TIMER= 20
TRESHOLD=5
DELAYTIME=0.05
class Robot:

	def __init__(self):
		self.ended=False
		self.asleep=False
		self.head_moving=0# 0 not moving,1 saying "yes", -1 saying "no"
		self.drowsy=drowsy.DrowC()
		self.recognizing=False
		self.faceDirection="front"

	def getHeadMove(self):
		tempTimer=TIMER
		positive=0
		negative=0
		self.recognizing=True
		last="front"
		while(tempTimer):

			direction=self.faceDirection
			if(direction=="up" or direction=="down"):
				if(last!= direction):
					positive+=1
				
			elif(direction=="left" or direction=="right"):
				if(last!= direction):
					negative+=1
				
			last=direction
			tempTimer-=1
			time.sleep(DELAYTIME)
		value=1
		direction= positive
		if(negative > positive):
			direction=negative
			value=-1

		if(direction < TRESHOLD):
			value=0

		self.head_moving=value
		self.recognizing=False


	def getMood(self):
		result="sad"

		return result
	def initRecognition(self):
		#t = Thread(target=self.loop)
		#t.deamon = True
		self.loop()
		#t.start()

	def loop(self):
		vs = VideoStream(0).start()
		while(self.drowsy.detect(vs.read())!=-1):
			self.asleep=self.drowsy.asleep
			self.faceDirection=self.drowsy.faceDirection
			if(self.faceDirection!="front" and not self.recognizing):
				t = Thread(target=self.getHeadMove)
				t.deamon = True
			
				t.start()

		
		vs.stop() 
		self.ended=True









