import wikipedia

import urllib
import os
import threading
from time import sleep








class seccion:
    
    def __init__(self,nombre,texto,secciones={},nombres=[],depth=0):
        self.name=nombre
        self.text=texto
        self.secciones=secciones
        self.seccionesNames=nombres
        self.selected=False
        self.depth=depth
        
        
        if(len(texto)>=1 and len(secciones.keys())>=1):
            
            self.seccionesNames=[self.name+" summary"]+self.seccionesNames
            self.secciones[self.name+" summary"]=seccion(self.name+" summary",texto,{},[],depth)
    def resetSelected(self):
        self.selected=False
        for i in self.secciones.keys():
            self.secciones[i].resetSelected()
    def setSelected(self,name):
        if(not self.selected):
            if(name in self.secciones.keys()):
                self.selected=name
                return True
            else:
                
                return False
        else:
            result =self.secciones[self.selected].setSelected(name)
            if(not result):
                self.selected=False
          
    def show(self):
        text="="*self.depth+" "+self.name+" "+self.depth*"="+"\n"
        text+="\n".join(self.text)+"\n"
        for i in self.seccionesNames:
            text+=self.secciones[i].show()   
        return text             
    def getSections(self):
         if(len(self.secciones)==0):
             return False
         result=[]
         for i in self.seccionesNames:
             result.append(self.secciones[i].name)
         return result
             
    def lastSelected(self):
        i=self.getSelected()
        if(not i):
            return self
        while((i.getSelected())!=False):
            i=i.getSelected()
        return i
    def getSelected(self):
        if(self.selected):
            return self.secciones[self.selected]
        return False           
    def getSecions(self):
             if(self.selected==False):
                 if(len(self.secciones.keys())==0):
                     return False
                 else:
                     return self.seccionesNames
             else:
                 return self.secciones[self.selected].getSections()
                 
    def getText(self):
        if(len(self.secciones)==0 or self.selected==False):
            return "\n".join(self.text)
        else:
            return self.secciones[self.selected].getText()
        
        
    
    
class concepto:
    
    
    
    def __init__(self,word,downloadImages=True):
        self.name=word
        self.secciones={}
        self.seccionesNames=[]
        self.selectedSec="summary"
        self.selectedSubSec=""
        if os.path.exists("resources/"+self.name):
            self.load()
            return
        self.page=wikipedia.page(word)
        images=self.page.images
        self.text=self.page.content.split("\n")
        self.saveText()
        if(downloadImages):
            self.downloadImages(self.page.images,len(self.page.images))
        self.showCounter=0
        self.image1=False
        self.image2=False
        self.imageCounter=0
        self.imageTimer=0
        self.imageTimerMax=100
        self.imageNames=[]
        self.loadText()
    def getSelected(self):
        return self.selectedSec
    def createSection(self,name,text,counter=3):
        subSections={}
        subNames=[]
        t=[]
        subt=[]
        subName=""
        sub=False
        for i in text:
            if(len(i)==0):
                continue
            if(i[0]=="="):
                pass                
            if(i[:counter]=="="*counter and i[:counter+1]!="="*(counter+1)):
                
                
                if not sub:
                    sub=True
                    subName=i.lower()
                    subName=subName.strip("=")
                    subName=subName.strip(" ")
                    
                    
                    
                else:
                    subSections[subName]=self.createSection(subName,subt,counter+1)
                    subNames.append(subName)
                    subt=[]
                    subName=i.lower()
                    subName=subName.strip("=")
                    subName=subName.strip(" ")
                
            
            else:
                
                if(sub):
                    if(i!=""):
                        subt.append(i)
                else:
                    if(i!=""):
                        
                        t.append(i)
        if(subt!=[]):
            subSections[subName]=self.createSection(subName,subt,counter+1)
            subNames.append(subName)
        
        s=seccion(name,t,subSections,subNames,counter-1)
        return s
                    
                   
                
        
        
    def getSection(self):
        
        
        if(self.selectedSec in self.secciones.keys()):
            return self.secciones[self.selectedSec].getText()
        
        return -1
    def load(self):
        self.loadText()

        self.showCounter=0
        self.image1=False
        self.image2=False
        self.imageCounter=0
        self.imageTimer=0
        self.imageTimerMax=100
        self.imageNames=[]
        imageNames=["resources/"+self.name+"/"+i for i in os.listdir("resources/"+self.name) if(os.path.isfile("resources/"+self.name+"/"+i)and i!=self.name+".txt")]
        self.imageNames=imageNames
        #self.saveSections("prueba")
    def getSections(self):
        result=[]
        for i in self.seccionesNames:
            result.append(self.secciones[i].name)
        return result
    def getSubsections(self):
        results=[]
        if(self.selectedSec in self.secciones.keys()):
            for i in self.secciones[self.selectedSec].secciones.keys():
                results.append(self.secciones[self.selectedSec].secciones[i].name)
            
            return results
        return -1
    def loadText(self,name=False):
        if(not name):
            name=self.name
        directory="resources/"+self.name
        file=open(directory+"/"+self.name+".txt","r")
        self.text=file.read().split("\n")
        self.divideText(self.text)
    def saveSections(self,name=False):
        if(not name):
            name=self.name   
        directory="resources/"+self.name
        if not os.path.exists(directory):
            os.makedirs(directory)
        file=open(directory+"/"+name+".txt","w+")
        for s in self.seccionesNames:
            if(s!= "summary"):
                file.write(self.secciones[s].show())
            else:
                file.write("\n".join(self.secciones[s].text)+"\n")
                
    def getSummary(self):
        if("summary"in self.secciones):
            return self.secciones["summary"].text
        return -1
                    
    def divideText(self,text):
        if(not isinstance(text,list) and not isinstance(text,tuple)):
            temp=text.split("\n")
        else:
            temp= text
        name=""
        text=[]
        turn=0
        subClass=False
        secciones={}
        for i in temp:
            if(i==""):
                continue
            if(i[:2]=="==" and i[:3]!="==="):
                
                if(turn==0):
                    self.secciones["summary"]=seccion("summary",text)
                    self.seccionesNames.append("summary")
                    name=i.lower()
                    name=name.strip("=")
                    name=name.strip(" ")
                    
                    
                    text=[]
                    turn=1
                else:
                    s=self.createSection(name,text)
                    self.secciones[name]=s
                    self.seccionesNames.append(name)
                    text=[]
                    
                    name=i.lower()
                    name=name.strip("=")
                    name=name.strip(" ")
                    
                    
                    
            else:
                if(i!=""):
                    text.append(i)
        s=self.createSection(name,text)
        self.secciones[name]=s
        self.seccionesNames.append(name)
        
        
    def saveText(self,name=False):
        if(not name):
            name=self.name   
        directory="resources/"+self.name
        if not os.path.exists(directory):
            os.makedirs(directory)
        file=open(directory+"/"+name+".txt","w+")
        for i in self.text:
            #i=i.encode("ascii","ignore")
            file.write(i+"\n") 
        file.close
        
    def downloadImages(self,images,num):
        for i in range(num):
            t=threading.Thread(target=self.addImage,args=(images[i],i,))
            t.start()
    def download_web_image(self,url,name):
        
        full_name = name
        extension=url.split(".")[-1]
        if(extension=="svg"):
            return -1
        name+="."+extension
        
        urllib.request.urlretrieve(url, os.path.join(os.getcwd(), name)) # download and save image
        return name
    def addImage(self,url,counter):
        name=self.name
        directory="resources/"+self.name
        if not os.path.exists(directory):
            os.makedirs(directory)
        name=self.download_web_image(url,directory+"/"+name+str(counter))
        if(name ==-1):
            counter-=1
            return -1
        self.imageNames.append(name)
        #image=self.screen.load(name,x,y)
        #self.images.append(image)
    
                    
        
       