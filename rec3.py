import speech_recognition as sr
from gtts import gTTS
import pyttsx3
from threading import Thread

class voiceRecognitor:
	text="" 
	ended = False

	def threadVoice(self):
		
		t = Thread(target=self.voiceTotext)
		t.start()
		

	def voiceTotext(self):

		# Obtenemos el audio del microfono
		while not self.ended:
			r = sr.Recognizer()
			with sr.Microphone() as source:
			    print("Say something!")
			    r.adjust_for_ambient_noise(source)
			    audio = r.listen(source)

			# Intenta reconocer el audio
			try:
		            self.text = r.recognize_google(audio)
			    #Reconoce el audio y lo imprime por pantalla
		            print("Alexia thinks you said " + self.text)
		
			    
			    
			#No reconoce el audio
			except sr.UnknownValueError:
			    print("Alexia could not understand audio")
	
			#Error en el request
			except sr.RequestError as e:
			    print("Alexia error; {0}".format(e))

