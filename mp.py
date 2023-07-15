import mediapipe as mp
import cv2
import numpy as np 
import uuid
import os


keys=[["Q","W","E","R","T","Y","U","I","O","P"],
      ["A","S","D","F","G","H","J","K","L",";"],
      ["Z","X","C","V","B","N","M",",",".","/"]]


mp_drawing=mp.solutions.drawing_utils
mp_hands=mp.solutions.hands

cap=cv2.VideoCapture(1)

with mp_hands.Hands(min_detection_confidence=0.8,min_tracking_confidence=0.5,max_num_hands=2) as hands:

	while cap.isOpened():
		ret,frame=cap.read()

		image=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
		image.flags.writeable=False# Set flag as false
		results=hands.process(image)
		image.flags.writeable=True# Set flag as true
		image=cv2.cvtColor(image,cv2.COLOR_RGB2BGR)

		#Detections
		#print(results)
		#print(results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP])
	
		#Rendering results
		if results.multi_hand_landmarks:
			print(results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP])
			for num,hand in enumerate(results.multi_hand_landmarks):
				mp_drawing.draw_landmarks(image,hand,mp_hands.HAND_CONNECTIONS)


		cv2.imshow('Hand Tracking',image)

		if cv2.waitKey(10) & 0xFF==ord('q'):
			break
cap.release()
cv2.destroyAllWindows()

