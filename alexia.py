from rec3 import *
from textToVoice import *
from Diccionary import*
import time
r = voiceRecognitor()
v = textRecognitor()
d = Ask4Joke()

#r.threadVoice()
"""while True:
	if (r.text != ""):
		v.textToVoice(r.text)
		if (r.text == "tell me a joke"):
			v.textToVoice(Ask4Joke())			
			v.textToVoice(GetJoke())
			
			
		
		r.text = ""

r.ended = True"""
def callJoke():
	#v.textToVoice(r.text)
	v.textToVoice(Ask4Joke())	
	time.sleep(1)
	
	
	#print(r.text)
	v.textToVoice(GetJoke())
			
			
		
	#r.text = ""


def destr():
	pass
	#r.ended=True