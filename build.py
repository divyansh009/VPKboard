import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import numpy as np
from time import sleep

cap=cv2.VideoCapture(1)
#Inc size of window as we need a big keyboard on screen
cap.set(3,1280) #(Id no. 3 is width,Width value)
cap.set(4,720) #Id no. 4 is height, Height Value)

detector=HandDetector(detectionCon=0.8)

keys=[["Q","W","E","R","T","Y","U","I","O","P"],
      ["A","S","D","F","G","H","J","K","L",";"],
      ["Z","X","C","V","B","N","M",",",".","/"]]

finalText=""

def drawAll(img,buttonList):
    for button in buttonList:
        x,y=button.pos
        w,h=button.size
        cv2.rectangle(img,button.pos,(x+w,y+h),(255,0,255),cv2.FILLED) #(image, starting point,end point,color RGB,want filled rect)
        cv2.putText(img,button.text,(x+20,y+65),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),4) #image, letters, x-y coordinates of letter, font,scale of font ,color,thickness of font
    return img

class Button():
    def __init__(self,pos,text,size=[85,85]):
        self.pos=pos
        self.size=size
        self.text=text
        #This part we must run only nce rather than everytime bec. attributes are not changing

    #This method can be called during loop for img frame passing parameter and returning img having text
    #def draw(self,img):
        #x,y=self.pos
        #w,h=self.size
        #cv2.rectangle(img,self.pos,(x+w,y+h),(255,0,255),cv2.FILLED) #(image, starting point,end point,color RGB,want filled rect)
        #cv2.putText(img,self.text,(x+20,y+65),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),4) #image, letters, x-y coordinates of letter, font,scale of font ,color,thickness of font
        #return img

buttonList=[]

#myButton=Button([100,100],"Q")
#myButton2=Button([200,100],"W")
#myButton3=Button([300,100],"E")

for i in range(len(keys)):
    for j,key in enumerate(keys[i]):
        buttonList.append(Button([100*j+50,100*i+50],key)) #Width, Height
while True:
    success,img=cap.read()
    img=detector.findHands(img) #Finds hands
    lmList,bboxInfo=detector.findPosition(img) #Returns landmarks of our hand as lmList array and a box 
    img=drawAll(img,buttonList)

    #When using fingers, are we close to these buttons or not
    if lmList: #Hand landmarks exist atleast
        for button in buttonList: #To know location of each button, so that we can find out if our finger is in that range or not
            x,y=button.pos
            w,h=button.size
            #Landmarks 8,12 are tips of index and middle finger respectively. Pt. 8 => x=lmList[8][0]; y=lmList[8][1]
            if x<lmList[8][0]<x+w and y<lmList[8][1]<y+h:
                #Change color of our button
                cv2.rectangle(img,button.pos,(x+w,y+h),(175,0,175),cv2.FILLED) #(image, starting point,end point,color RGB,want filled rect)
                cv2.putText(img,button.text,(x+20,y+65),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),4) #image, letters, x-y coordinates of letter, font,scale of font ,color,thickness of font
                
                l,_,_=detector.findDistance(8,12,img,draw=False)#Inbuilt method of cvzone package to find dist b/w pt. 8 and 12 in frame img
                #draw=false makes the lines disappear b/w index and middle finger
                #If we wish to ignore any variable in python, we define it by underscore.

                #print(l) #Tells dist b/w pts. When this dist is below specific threshold, register it as a click
                if l<40:
                    cv2.rectangle(img,button.pos,(x+w,y+h),(0,255,0),cv2.FILLED) #(image, starting point,end point,color RGB,want filled rect)
                    cv2.putText(img,button.text,(x+20,y+65),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),4) #image, letters, x-y coordinates of letter, font,scale of font ,color,thickness of font
                    finalText+=button.text
                    sleep(0.75) #Given a timeout to avoid printing multiple letters at one go

    #After click registered, what to do?
    cv2.rectangle(img,(50,350),(700,450),(175,0,175),cv2.FILLED) #(image, starting point,end point,color RGB,want filled rect)
    cv2.putText(img,finalText,(60,430),cv2.FONT_HERSHEY_PLAIN,5,(255,255,255),5) #image, letters, x-y coordinates of letter, font,scale of font ,color,thickness of font


    #Use a universal draw function rather than individual ones:
    #img=myButton.draw(img)
    #img=myButton2.draw(img)
    #img=myButton3.draw(img)
    cv2.imshow("Image",img)
    cv2.waitKey(2)
