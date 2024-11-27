import cv2
import numpy as np
import pyautogui
import mediapipe as mp

circle_radius = 10
circle_thickness = 2

mouse_position = (0,0)

def move_mouse():
    global mouse_position
    screen_width, screen_height = pyautogui.size()
    x, y = mouse_position
    x_normalized = x / cap_width
    y_normalized = y / cap_height

    pyautogui.moveTo(int(x_normalized * screen_width), int(y_normalized * screen_height))

def open_file():
    global mouse_position
    x, y = mouse_position
    pyautogui.click(x, y)

cap = cv2.VideoCapture(0)

cap_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
cap_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

mp_hands = mp.solutions.hands.Hands(static_image_mode = False, max_num_hands = 1, min_detection_confidence = 0.7)

mouse_position = (cap_width // 2, cap_height // 2)
cv2.namedWindow('webcam')

while True:
  ret, frame = cap.read()
  frame = cv2.flip(frame, 1) 
  frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
  results = mp_hands.process(frame_rgb)
  if results.multi_hand_landmarks:
     hand_landmarks = results.multi_hand_landmarks[0]
     for landmark in hand_landmarks.landmark:
        x = int(landmark.x * cap_width)
        y = int(landmark.y * cap_height)
        if landmark.HasField('visibility') and landmark.visibility < 0.1:
           continue
        mouse_position = (x, y)
        cv2.circle(frame, mouse_position, circle_radius,(0, 0, 255), circle_thickness)
  cv2.imshow('webcam', frame)

  if cv2.waitKey(1) & 0xFF == ord('q'):
     break
  move_mouse()

  if cv2.waitKey(1) & 0xFF == ord('f'):
     open_file()

cap.release()
cv2.destroyAllWindows()