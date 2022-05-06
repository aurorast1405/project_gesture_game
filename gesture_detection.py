import cv2
import mediapipe as mp
import time
import socket


ok = False
while not ok:
    try:
        host, port = "127.0.0.1", 25001
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        ok = True
    except:
        pass


cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
prev = 0


while True:
    font = cv2.FONT_HERSHEY_SIMPLEX
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handlms in results.multi_hand_landmarks:
            lmList = []
            for id, lm in enumerate(handlms.landmark):
                h, w, c = imgRGB.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
            mpDraw.draw_landmarks(img, handlms, mpHands.HAND_CONNECTIONS,
                                  mp_drawing_styles.get_default_hand_landmarks_style(),
                                  mp_drawing_styles.get_default_hand_connections_style())
            indexX = 0
            indexY = 0
            indexMid = 0
            handBottomX = 0
            handBottomY = 0
            pinkyX = 0
            pinkyY = 0

            middleY = 0
            nonameY = 0
            toe_x = 0
            for lms in lmList:
                if lms[0] == 7:
                    indexX, indexY = lms[1], lms[2]
                elif lms[0] == 5:
                    indexMid = lms[2]
                elif lms[0] == 4:
                    toe_x = lms[1]
                elif lms[0] == 11:
                    middleY = lms[2]
                elif lms[0] == 15:
                    nonameY = lms[2]
                elif lms[0] == 19:
                    pinkyX, pinkyY = lms[1], lms[2]
                elif lms[0] == 0:
                    handBottomX, handBottomY = lms[1], lms[2]
            indexMid -= 20
            if (indexY < handBottomY) and (indexY >= indexMid) and (middleY < handBottomY) and (middleY >= indexMid) \
                    and (nonameY < handBottomY) and (nonameY >= indexMid) and (abs(indexX - toe_x) <= 88) \
                    and (pinkyY >= indexMid):
                cv2.rectangle(img, (indexX, indexY), (pinkyX, handBottomY), (0, 0, 255), 2)
                # cv2.putText(imgRGB, "jump!", (pinkyX + 2, indexY - 2), (font), .7,
                #             (0, 0, 255), 1, cv2.LINE_4)
                if time.time() - prev >= 1:
                    prev = time.time()
                    s = "1"
                    sock.sendall(s.encode("UTF-8"))
                    print("Jump!")
            elif (indexY < handBottomY) and (indexY >= indexMid) and (middleY < indexMid) \
                    and (nonameY < handBottomY) and (nonameY >= indexMid) and (abs(toe_x - indexX) <= 88) \
                    and (pinkyY >= indexMid):
                cv2.rectangle(img, (indexX, indexY), (pinkyX, handBottomY), (255, 255, 0), 2)
                if time.time() - prev >= 1:
                    
                    prev = time.time()
                    print("Pause!")

    cv2.imshow("Image", img)
    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()


