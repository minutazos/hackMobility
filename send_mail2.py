#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
from email.mime.image import MIMEImage
import os
import datetime


smtpUser = 'alvaro.garcia.bamala@gmail.com'
smtpPass = 'agbHackathon96'

toAdd = 'classicsold@gmail.com'
fromAdd = smtpUser

today = datetime.date.today()

subject  = 'Data File 01 %s' % today.strftime('%Y %b %d')
header = 'To :' + toAdd + '\n' + 'From : ' + fromAdd + '\n' + 'Subject : ' + subject + '\n'
body = 'This is a data file on %s' % today.strftime('%Y %b %d')

attach = 'Data on %s.csv' % today.strftime('%Y-%m-%d')

print (header)


def sendMail(to, subject, text, files=[]):
    assert type(to)==list
    assert type(files)==list

    msg = MIMEMultipart()
    msg['From'] = smtpUser
    msg['To'] = COMMASPACE.join(to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach( MIMEText(text) )

    fp = open('files/photo.png', 'rb')
    img = MIMEImage(fp.read())
    fp.close()
    msg.attach(img)

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo_or_helo_if_needed()
    server.starttls()
    server.ehlo_or_helo_if_needed()
    server.login(smtpUser,smtpPass)
    server.sendmail(smtpUser, to, msg.as_string())

    print ('Done')

    server.quit()


sendMail( [toAdd], subject, body, [attach] )
