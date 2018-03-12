
from sys import platform
PLATFORM="linux"
if platform == "linux" or platform == "linux2":
    # linux
    import pyttsx3

elif platform == "darwin":
    # OS X
    from os import system
    PLATFORM= "osx"
elif platform == "win32":
    # Windows...
    import pyttsx3
    PLATFORM ="windows"

class textRecognitor:
	if(PLATFORM!="osx"):
		engine = pyttsx3.init()

	def textToVoice(self,text):
		if(PLATFORM=="osx"):
			result="say -v Veena"+" '"+text+"'"
			print(result)
			system(result)
		else:

			self.engine.say(text)
			self.engine.runAndWait()