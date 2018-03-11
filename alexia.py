from rec3 import *
from voice_to import *
from Diccionary import*

r = voiceRecognitor()
v = textRecognitor()
d = Ask4Joke()

r.threadVoice()
while True:
	if (r.text != ""):
		v.textToVoice(r.text)
		if (r.text == "tell me a joke"):
			v.textToVoice(Ask4Joke())			
			v.textToVoice(GetJoke())
			
			
		
		r.text = ""

r.ended = True


