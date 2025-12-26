import cv2
import mediapipe as mp
import numpy as np
import math
import pyautogui
from collections import deque
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# ==================================================
# AUDIO (PyCaw) SETUP – Python 3.12 FIX
# ==================================================
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
volume = devices.EndpointVolume

# ==================================================
# MEDIAPIPE HANDS SETUP
# ==================================================
mpHands = mp.solutions.hands
hands = mpHands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mpDraw = mp.solutions.drawing_utils

# ==================================================
# OPENCV CAMERA
# ==================================================
cap = cv2.VideoCapture(0)

# ==================================================
# SMOOTHING BUFFER (MOVING AVERAGE)
# ==================================================
smooth_buffer = deque(maxlen=5)

# ==================================================
# STATE VARIABLES
# ==================================================
paused = False
prevVolScalar = -1  # used to throttle OSD updates

# ==================================================
# FIST DETECTION FUNCTION
# ==================================================
def is_fist(lm):
    return (
        lm[8][2]  > lm[6][2] and   # index
        lm[12][2] > lm[10][2] and  # middle
        lm[16][2] > lm[14][2] and  # ring
        lm[20][2] > lm[18][2]      # pinky
    )

# ==================================================
# MAIN LOOP
# ==================================================
while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    h, w, _ = img.shape
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            lmList = []

            for id, lm in enumerate(handLms.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append((id, cx, cy))

            # Thumb tip (4) & Index tip (8)
            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]

            # Distance calculation
            length = math.hypot(x2 - x1, y2 - y1)

            # Gesture smoothing
            smooth_buffer.append(length)
            smooth_length = sum(smooth_buffer) / len(smooth_buffer)

            # Draw finger points
            cv2.circle(img, (x1, y1), 10, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (255, 0, 0), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)

            # ==================================================
            # MUTE WHEN FINGERS TOUCH
            # ==================================================
            if smooth_length < 25:
                volume.SetMute(1, None)
                pyautogui.press("volumemute")
                cv2.putText(img, "MUTED", (40, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 0, 255), 3)
            else:
                volume.SetMute(0, None)

                # ==================================================
                # VOLUME CONTROL + WINDOWS OSD
                # ==================================================
                volScalar = np.interp(
                    smooth_length, [30, 200], [0.0, 1.0]
                )
                volume.SetMasterVolumeLevelScalar(volScalar, None)

                # Trigger native Windows volume bar ONLY on change
                if abs(volScalar - prevVolScalar) > 0.02:
                    pyautogui.press("volumeup")
                    pyautogui.press("volumedown")
                    prevVolScalar = volScalar

            # ==================================================
            # PAUSE / PLAY USING FIST
            # ==================================================
            if is_fist(lmList):
                if not paused:
                    pyautogui.press("playpause")
                    paused = True
                    cv2.putText(img, "PAUSED", (350, 80),
                                cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (255, 0, 0), 3)
            else:
                paused = False

            # Draw hand landmarks
            mpDraw.draw_landmarks(
                img, handLms, mpHands.HAND_CONNECTIONS
            )

    cv2.imshow("Gesture Based Volume & Media Control", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ==================================================
# CLEAN EXIT
# =======================================
