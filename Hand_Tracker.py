import cv2
import mediapipe as mp
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
 
devices = AudioUtilities.GetSpeakers()
interf = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interf, POINTER(IAudioEndpointVolume))
 
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
 
capture = cv2.VideoCapture(0)
 
with mp_hands.Hands(
    max_num_hands=2,  #손 개수
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
 
    while capture.isOpened():
        success, image = capture.read()
        if not success:
            continue
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)  #이미지 형식 변환
 
        results = hands.process(image) #??
 
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) #이미지 형식 변환
 
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                finger1 = int(hand_landmarks.landmark[4].x * 100 )
                finger2 = int(hand_landmarks.landmark[8].x * 100 )
    
                dist = abs(finger1 - finger2)
                cv2.putText(
                    image, text='f1=%d f2=%d dist=%d ' % (finger1,finger2,dist), org=(10, 30),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                    color=255, thickness=3)
                if(dist>=0 and dist<=100):
                    dist = -96 + dist
                    print(dist)
                    dist = min(0, dist)
                    print(dist)
   #                 volume.SetMasterVolumeLevel(dist, None)
                
 
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
 
        cv2.imshow('image', image)
        if cv2.waitKey(1) == ord('q'):
            break
 
capture.release()
