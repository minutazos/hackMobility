

from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
from threading import Thread
import numpy as np
import playsound
import argparse
import imutils
import time
import dlib
import cv2
import pyttsx3
import math
import random

TRESHOLD= 80
TRESHOLD_Y= 30

class DrowC:
    EYE_AR_THRESH = 0.3
    EYE_AR_CONSEC_FRAMES = 30#48

    COUNTER = 0
    ALARM_ON = False
    visible=False
    yawning=False
    lostCounter=0
    mouthSize=0
    faceDirection="front"
    distractedCounter=-1
    def __init__(self):
        print("[INFO] loading facial landmark predictor...")
        self.asleep=False
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("shape_predictor.dat")

        # grab the indexes of the facial landmarks for the left and
        # right eye, respectively
        (self.lStart, self.lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (self.rStart, self.rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    def say_goodbye(self):
        #engine.say("Hey... Where are you?")
        #engine.runAndWait()
        pass

    def say_distraction(self):
        #engine.say("Hey... Look forward?")
        #engine.runAndWait()
        pass
    def sound_alarm(self):
    	self.asleep=True
    	pass
		# play an alarm sound
        #engine.say("Hey... Wake up!")
        #engine.runAndWait()
		#playsound.playsound(path)

    def say_hello(self):
		# play an alarm sound
        #engine.say("Hello... welcome back!")
        #engine.runAndWait()
        #engine.say("what's your name?")
        #engine.runAndWait()
        pass
		#playsound.playsound(path)

    def mouth_size(self,points):
        mouth=points[48:][:]
        x=np.array([i[0] for i in mouth.tolist()])
        
        y=np.array([i[1] for i in mouth.tolist()])
        xdist=0
        ydist=0
        
        for i in range(len(x)):
        	for j in range(i,len(x)):
        		#print("x: ",x[i]-x[j])
        		xdist+=math.pow(x[i]-x[j],2)
        		ydist+=math.pow(y[i]-y[j],2)



        x=math.sqrt(xdist)
        y=math.sqrt(ydist)
        return np.array((x,y))
    def eye_aspect_ratio(self,eye):
	# compute the euclidean distances between the two sets of
	# vertical eye landmarks (x, y)-coordinates
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])

        # compute the euclidean distance between the horizontal
        # eye landmark (x, y)-coordinates
        C = dist.euclidean(eye[0], eye[3])

        # compute the eye aspect ratio
        ear = (A + B) / (2.0 * C)

        # return the eye aspect ratio
        return ear
    def detect(self,frame):
        










            
            frame = imutils.resize(frame, width=450)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # detect faces in the grayscale frame
            rects = self.detector(gray, 0)
            new_user=False
            if(len(rects)!=0):
                if(not self.visible):
                     self.visible=True
                     new_user=True
                     t = Thread(target=self.say_hello)
                     t.deamon = True
                     t.start()
                self.lostCounter=-1
            elif(self.visible and self.lostCounter<=0):
                 
                 
                 self.lostCounter=1000
                 self.distractedCounter=int(random.random()*(self.lostCounter *0.2)+self.lostCounter*0.8)
            elif(self.visible):
                
                self.lostCounter-=1
                if(self.lostCounter==0):
                    t = Thread(target=self.say_goodbye)
                    t.deamon = True
                    t.start()
                    self.visible=False
                if(self.lostCounter==self.distractedCounter):
                    t = Thread(target=self.say_distraction)
                    t.deamon = True
                    t.start()


            # loop over the face detections
            for rect in rects:
                    # determine the facial landmarks for the face region, then
                    # convert the facial landmark (x, y)-coordinates to a NumPy
                    # array

                    shape = self.predictor(gray, rect)
                    shape = face_utils.shape_to_np(shape)
                    if(new_user):
                    	self.mouthSize=self.mouth_size(shape)
                    """for p in np.array(shape):
                    	cv2.circle(frame, (int(p[0]), int(p[1])), 3, (0,0,255), -1)
                    """
                    #print(len(shape))
                    points=np.array([shape[33],shape[8],shape[45],shape[36],shape[54],shape[48]],dtype="double")
                    self.FACE_PROPORTION=distance(shape[1],shape[15])/distance(meanPoint(shape[19],shape[24]),shape[8])
                    #print(points)
                    cv2.imwrite("prueba.png",frame)
                    self.faceDirection=detect_direction(frame,points)
                    # extract the left and right eye coordinates, then use the
                    # coordinates to compute the eye aspect ratio for both eyes
                    leftEye = shape[self.lStart:self.lEnd]
                    rightEye = shape[self.rStart:self.rEnd]
                    leftEAR = self.eye_aspect_ratio(leftEye)
                    rightEAR = self.eye_aspect_ratio(rightEye)

                    # average the eye aspect ratio together for both eyes
                    ear = (leftEAR + rightEAR) / 2.0

                    # compute the convex hull for the left and right eye, then
                    # visualize each of the eyes
                    leftEyeHull = cv2.convexHull(leftEye)
                    rightEyeHull = cv2.convexHull(rightEye)
                    cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
                    cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
                    if(self.yawning):
                    	cv2.putText(frame, "bostezando", (60, 30),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    # check to see if the eye aspect ratio is below the blink
                    # threshold, and if so, increment the blink frame counter
                    tempMouth=self.mouth_size(shape)
                    if(not isinstance(self.mouthSize,int)):

                    	if(tempMouth[1]<=self.mouthSize[1]*1.3):
                    		self.yawning=False

                    if ear < self.EYE_AR_THRESH:
                            self.COUNTER += 1
                            if(not isinstance(self.mouthSize,int)):
                            	if(tempMouth[1]>self.mouthSize[1]*1.3):
                            		self.yawning=True
                            # if the eyes were closed for a sufficient number of
                            # then sound the alarm
                            if self.COUNTER >= self.EYE_AR_CONSEC_FRAMES:
                                    # if the alarm is not on, turn it on
                                    if not self.ALARM_ON:
                                            self.ALARM_ON = True

                                            
                                            t = Thread(target=self.sound_alarm)
                                            t.deamon = True
                                            t.start()

                                    

                    # otherwise, the eye aspect ratio is not below the blink
                    # threshold, so reset the counter and alarm
                    else:
                            
                            self.COUNTER = 0
                            self.asleep=False
                            self.ALARM_ON = False

                    # draw the computed eye aspect ratio on the frame to help
                    # with debugging and setting the correct eye aspect ratio
                    # thresholds and frame counters
                    cv2.putText(frame, self.faceDirection, (10, 30),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    """cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)"""
     
            # show the frame
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF
     
            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
            	cv2.destroyAllWindows()
            	return -1





def detect_direction(im,image_points):
    size = im.shape
  
    model_points = np.array([
                            (0.0, 0.0, 0.0),             # Nose tip
                            (0.0, -330.0, -65.0),        # Chin
                            (-225.0, 170.0, -135.0),     # Left eye left corner
                            (225.0, 170.0, -135.0),      # Right eye right corne
                            (-150.0, -150.0, -125.0),    # Left Mouth corner
                            (150.0, -150.0, -125.0)      # Right mouth corner
                         
                        ])
 
 
    # Camera internals
     
    focal_length = 0.0385#size[1]
    center = (size[1]/2, size[0]/2)
    camera_matrix = np.array(
                 [[focal_length, 0, center[0]],
                 [0, focal_length, center[1]],
                 [0, 0, 1]], dtype = "double"
                 )
     
    #print ("Camera Matrix :\n {0}".format(camera_matrix))
     
    dist_coeffs = np.zeros((4,1)) # Assuming no lens distortion
    (success, rotation_vector, translation_vector) = cv2.solvePnP(model_points, image_points, camera_matrix, dist_coeffs)
     
    #print ("Rotation Vector:\n {0}".format(rotation_vector))
    #print ("Translation Vector:\n {0}".format(translation_vector))
     
     
    # Project a 3D point (0, 0, 1000.0) onto the image plane.
    # We use this to draw a line sticking out of the nose
     
     
    (nose_end_point2D, jacobian) = cv2.projectPoints(np.array([(0.0, 0.0, 1000.0)]), rotation_vector, translation_vector, camera_matrix, dist_coeffs)
     
    for p in image_points:
        cv2.circle(im, (int(p[0]), int(p[1])), 3, (0,0,255), -1)
     
     
    p1 = ( int(image_points[0][0]), int(image_points[0][1]))
    p2 = ( int(nose_end_point2D[0][0][0]), int(nose_end_point2D[0][0][1]))
     
    cv2.line(im, p1, p2, (255,0,0), 2)
    
    if(p1[0]-p2[0]>TRESHOLD):
    	return "left"
    elif(p2[0]-p1[0]>TRESHOLD):
    	return "right"
    elif(p2[1]-p1[1]>TRESHOLD_Y):
    	return "down"
    elif(p2[1]<=np.mean([a[1] for a in image_points])):
    	return "up"

    return "front"
def meanPoint(point1,point2):
	x=(point1[0]+point2[0])/2
	y=(point1[0]+point2[0])/2
	return np.array((x,y))
def distance(point1,point2):
	x=point1[0]-point2[0]
	y=point1[1]-point2[1]
	return math.sqrt(math.pow(x,2)+math.pow(y,2))

if(__name__=="__main__"):

	d=DrowC()
	vs = VideoStream(0).start()
	#engine= pyttsx3.init()
	#engine.setProperty("rate",150)
	while(d.detect(vs.read())!=-1):
	    pass
	cv2.destroyAllWindows()
	vs.stop()    
