from concepts import concepto
import wikipedia
import random

FRASES_DUDA={0:"I dont understand",1:"what?",2:"sorry?",3:"could you repeat, please?"}
QUICK_ANSWERS={"hello":"hello","thank you":"you are welcome","thanks": "you are welcome","bye":"bye","hi":"hi","hey":"hey"}

FRASES_PASO={0:"wow, slow down, what do you want to know?",1:"okay, this is what i know, tell me one ",2:"this is what i can tell you"}


class wikibot:
	def __init__(self):
		self.concepts=[]
		self.name="friend"
	def getConcept(self,keyword,downloadImages=True):
		try:

			self.concepts.append(concepto(keyword,downloadImages))

		except wikipedia.exceptions.PageError:
                    self.tema=""
                    
                    return random.choice(FRASES_DUDA)
		except wikipedia.exceptions.DisambiguationError:
                    self.tema=""
                    return "you will have to be more specific, "+self.name

if  __name__ =="__main__" :
           
     
	w=wikibot()
	w.getConcept("hackathon",False)