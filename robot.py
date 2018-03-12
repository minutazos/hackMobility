import drowsy
from imutils.video import VideoStream
from threading import Thread
import time

#cozmo libs
import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps

#lib para email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
from email.mime.image import MIMEImage
import os
import datetime


moods=["happy","sad","surprised","neutral","angry"]

TIMER= 20
TRESHOLD=5
DELAYTIME=0.05
class Robot:

	def __init__(self):
		self.ended=False
		self.asleep=False
		self.visible=False
		self.visibleAlert=False
		self.head_moving=0# 0 not moving,1 saying "yes", -1 saying "no"
		self.drowsy=drowsy.DrowC()
		self.recognizing=False
		self.robot=cozmo.robot.Robot
		self.faceDirection="front"
		self.yawning=False

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

	def deactivateAlert(self):
		self.visibleAlert=False
		drowsy.visibleAlert=False
	def getMood(self):
		result="sad"

		return result
	def initRecognition(self):
		#t = Thread(target=self.loop)
		#t.deamon = True
		self.loop()
		#t.start()
	def loop(self):
		try:
			track_face(self.robot)
			vs = self.robot.world.latest_image

			while(self.drowsy.detect(np.array(vs,cv.COLOR_RGB)) != -1):
				vs = self.robot.world.latest_image
				self.asleep=self.drowsy.asleep
				self.visible=self.drowsy.visible
				self.faceDirection=self.drowsy.faceDirection
				if(self.faceDirection!="front" and not self.recognizing):
					t = Thread(target=self.getHeadMove)
					t.deamon = True

					t.start()



			

			self.ended=True
		except:
			print("could not connect to cozmo")
			self.loop_old()
	def loop_old(self):
		vs = VideoStream(0).start()
		temp=vs.read()
		print(type(temp))
		while(self.drowsy.detect(temp)!=-1):
			temp=vs.read()

			self.asleep=self.drowsy.asleep
			self.yawning=self.drowsy.yawning
			self.faceDirection=self.drowsy.faceDirection
			if(self.faceDirection!="front" and not self.recognizing):
				t = Thread(target=self.getHeadMove)
				t.deamon = True
			
				t.start()

		
		vs.stop() 
		self.ended=True
def track_face(robot):
		#robot.say_text("Kozmo faces activado").wait_for_completed()
		# Move lift down and tilt the head up
		robot.move_lift(-3)
		robot.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE).wait_for_completed()
		robot.set_lift_height(0.0).wait_for_completed()
		face = None
		faceRevealed = False
		print("Press CTRL-C to quit")

		while (not faceRevealed):
			if (cozmo.faces.EvtFaceAppeared()):
				faceRevealed = True
				print("taking a picture...")
				robot.play_anim_trigger(cozmo.anim.Triggers.MeetCozmoScanningIdle).wait_for_completed()
				robot.play_anim_trigger(cozmo.anim.Triggers.MemoryMatchCozmoFollowTapsSoundOnly).wait_for_completed()
				pic_filename = "photo.png"
				latest_image = robot.world.latest_image
				latest_image.raw_image.convert('L').save(pic_filename)
				robot.set_all_backpack_lights(cozmo.lights.blue_light)
				send_mail()
				print("Unknown driver face appeared")
				time.sleep(5)
				return
			else:
				print("Known driver")
				robot.set_backpack_lights_off()
				time.sleep(5)

def send_mail():
    smtpUser = 'alvaro.garcia.bamala@gmail.com'
    smtpPass = 'agbHackathon96'

    toAdd = 'chewbacca.team.hack@gmail.com'
    fromAdd = smtpUser

    today = datetime.date.today()

    subject  = 'CAR ALERT SECURITY-Stranger Detected'
    header = 'To :' + toAdd + '\n' + 'From : ' + fromAdd + '\n' + 'Subject : ' + subject + '\n'
    body = 'The system detected a stranger in your car.'+ '\n'+  '\n' + 'You can see a data image.'+ '\n' + '\n' 'You recognize it?'

    attach = 'Data on %s.csv' % today.strftime('%Y-%m-%d')

    print (header)
    #assert type(toAdd)==list
    #assert type(attach)==list

    msg = MIMEMultipart()
    msg['From'] = smtpUser
    msg['To'] = COMMASPACE.join(toAdd)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach( MIMEText(body) )

    fp = open('photo.png', 'rb')
    img = MIMEImage(fp.read())
    fp.close()
    msg.attach(img)

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo_or_helo_if_needed()
    server.starttls()
    server.ehlo_or_helo_if_needed()
    server.login(smtpUser,smtpPass)
    server.sendmail(smtpUser, toAdd, msg.as_string())

    print ('Done')

    server.quit()







