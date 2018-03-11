#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
import time
#lib para img
try:
    from PIL import Image
except ImportError:
    sys.exit("Cannot import from PIL: Do `pip3 install --user Pillow` to install")

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

def track_face(robot: cozmo.robot.Robot):
    robot.say_text("Kozmo faces activado").wait_for_completed()
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

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

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

cozmo.run_program(track_face, use_viewer=True, force_viewer_on_top=True)
