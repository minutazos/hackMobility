import random

Diccionary={'State':['What is black, white, and red all over? A sunburnt penguin!',
                    "Do you know when you're getting old? When you go to an antique auction and three people bid on you!",
                    "Anton, do you think I’m a bad mother? And the son replies. My name is Paul, mom."],
            'Ask4Joke':'Do you want to hear a joke?',
            'HowDay':'How have been going your day?',
            'Tired':"Hey! don't you think you need a break up?some coffee?",
            'LookF':"Hey! Look at the road!",
            'WakeUp':"Wake up!, you lazy",
            'NoJokes':"Oh!, you hurt my circuits"
            }

def Ask4Joke():
    return Diccionary['Ask4Joke']
def GetJoke():
    return random.choice(Diccionary['State'])
def HowDay():
    return Diccionary['HowDay']
def Tired():#contador
    return Diccionary['Tired']
def LookF():#cara desaparece
    return Diccionary['LookF']
def WakeUp():#+nombre
    return Diccionary['WakeUp']
def NoJokes():
    return Diccionary['NoJokes']
