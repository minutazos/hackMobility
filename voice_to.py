import pyttsx3


class textRecognitor:
	engine = pyttsx3.init()

	def textToVoice(self,text):
		self.engine.say(text)
		self.engine.runAndWait()
