from robot import Robot
import alexa
import time
from threading import Thread








class Application:


	def __init__(self):
		self.status="idle"
		self.robot=Robot()
		self.alexa=alexa.Alexa()
		self.init()








	def init(self):
		
		t = Thread(target=self.loop)
		t.deamon = True
		#self.loop()
		t.start()
		self.robot.initRecognition()
		pass

	def loop(self):
		while(1):
			#print(self.robot.asleep)
			#print(self.robot.faceDirection)
			if(self.robot.head_moving==1):
				print("YES")
			if(self.robot.head_moving==-1):
				print("NO")	
			if(self.robot.ended):
				return
			
			time.sleep(1)





Application()