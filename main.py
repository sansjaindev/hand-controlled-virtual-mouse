import cv2
import mediapipe as mp
import pyautogui as pg

cam = cv2.VideoCapture(1)
hand_detector = mp.solutions.hands.Hands(
    max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5
)

drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pg.size()

index_y = 0
index_x = 0
thumb_y = 0
thumb_x = 0
dragging = False
clicked = False

while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks
    
    if hands:
        for hand in hands:
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                if id == 8:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    index_x = screen_width / frame_width * x
                    index_y = screen_height / frame_height * y
                    pg.moveTo(index_x, index_y)

                if id == 4:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    thumb_x = screen_width / frame_width * x
                    thumb_y = screen_height / frame_height * y

                    if abs(index_y - thumb_y) < 40:
                        if not clicked:
                            pg.click()
                            clicked = True
                    else:
                        clicked = False

                    if abs(index_x - thumb_x) < 40:
                        if not dragging:
                            pg.mouseDown()
                            dragging = True
                    else:
                        if dragging:
                            pg.mouseUp()
                            dragging = False

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
