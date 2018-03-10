
import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps

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
            img = cozmo.world.World.latest_image()
            rawData = open(img,'rb').read()
            imgSize = (x,y)
            img = Image.fromstring('L', imgSize, rawData, 'raw', 'F;16')
            img.save("/files/photo.png")
            robot.set_all_backpack_lights(cozmo.lights.blue_light)
            print("Unknown driver face appeared")
            time.sleep(5)
            return
        else:
            print("Known driver")
            robot.set_backpack_lights_off()
            time.sleep(5)



#def send_mail():
#    remitente = "From HackMobility <classicsold@gmail.com>"
#    destinatario = "SEAT User <classicsold@gmail.com>"
#    asunto = "Some stranger is using your car!"
#    mensaje = """Hi!<br/> <br/>
#    This message is sent when there is an unrecognized driver.
#    An image of the driver's face is attached to the e-mail.
#    """
#
#    email = """From: %s
#    To: %s
#    MIME-Version: 1.0
#    Content-type: text/html
#    Subject: %s
#
#    %s
#    """ % (remitente, destinatario, asunto, mensaje)
##
    ##we charge img
#    fp = open('/files/photo.png','rb')
#    adjunto = MIMEBase('multipart', 'encrypted')
#    adjunto.set_payload(fp.read())
#    fp.close()
    #base64 encryption to send it
#    encoders.encode_base64(adjunto)
    #header and title
#    adjunto.add_header('Content-Disposition', 'attachment', filename='unknownDriver.png')
    #msg attach
#    email.attach(adjunto)

    #we send the mail
#    try:
#        smtp = smtplib.SMTP('localhost')
#        smtp.sendmail(remitente, destinatario, email)
#        print ("Correo enviado")
#        smtp.quit()
#    except:
#        print ("""Error: el mensaje no pudo enviarse.
#        Compruebe que sendmail se encuentra instalado en su sistema""")



cozmo.run_program(track_face, use_viewer=True, force_viewer_on_top=True)
