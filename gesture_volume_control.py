import cv2
import mediapipe as mp
import numpy as np
import math
import time
import pyautogui
from pycaw.pycaw import AudioUtilities

# ==================================================
# AUDIO SETUP
# ==================================================
devices = AudioUtilities.GetSpeakers()
volume = devices.EndpointVolume

# ==================================================
# MEDIAPIPE SETUP
# ==================================================
mpHands = mp.solutions.hands
hands = mpHands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mpDraw = mp.solutions.drawing_utils

# ==================================================
# CAMERA
# ==================================================
cap = cv2.VideoCapture(0)

# ==================================================
# PARAMETERS
# ==================================================
alpha = 0.2
DEAD_ZONE = 0.02
MUTE_ON = 0.15
MUTE_OFF = 0.20
UPDATE_INTERVAL = 0.05
GESTURE_COOLDOWN = 1.0

# NEW: MODE CONTROL
VOLUME_ACTIVATION_THRESHOLD = 0.55
MODE_SWITCH_DELAY = 0.6

# ==================================================
# STATE VARIABLES
# ==================================================
smooth_val = None
prev_val = 0
muted = False
last_update = 0
prevVolScalar = -1
last_gesture_time = 0

media_state = "PLAYING"
last_gesture = "NONE"

gesture_mode = "MEDIA"
volume_mode_start = 0

# ==================================================
# GESTURE FUNCTIONS
# ==================================================
def is_fist(lm):
    return (
        lm[8][2]  > lm[6][2] and
        lm[12][2] > lm[10][2] and
        lm[16][2] > lm[14][2] and
        lm[20][2] > lm[18][2]
    )

def is_open_palm(lm):
    return (
        lm[8][2]  < lm[6][2] and
        lm[12][2] < lm[10][2] and
        lm[16][2] < lm[14][2] and
        lm[20][2] < lm[18][2]
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

            # Thumb & Index distance
            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]
            length = math.hypot(x2 - x1, y2 - y1)

            # Normalize
            hand_size = math.hypot(
                lmList[0][1] - lmList[9][1],
                lmList[0][2] - lmList[9][2]
            )
            norm_dist = length / hand_size

            # Smooth
            smooth_val = norm_dist if smooth_val is None else (
                alpha * norm_dist + (1 - alpha) * smooth_val
            )
            if abs(smooth_val - prev_val) < DEAD_ZONE:
                smooth_val = prev_val
            prev_val = smooth_val

            now = time.time()

            # =========================================
            # MEDIA GESTURES (LOCK MEDIA MODE)
            # =========================================
            if is_fist(lmList):
                gesture_mode = "MEDIA"
                volume_mode_start = 0

                if last_gesture != "FIST" and now - last_gesture_time > GESTURE_COOLDOWN:
                    if media_state != "PAUSED":
                        pyautogui.press("playpause")
                        media_state = "PAUSED"
                    last_gesture_time = now
                last_gesture = "FIST"

                cv2.putText(img, "PAUSED", (330, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 0, 255), 3)

            elif is_open_palm(lmList):
                gesture_mode = "MEDIA"
                volume_mode_start = 0

                if last_gesture != "PALM" and now - last_gesture_time > GESTURE_COOLDOWN:
                    if media_state != "PLAYING":
                        pyautogui.press("playpause")
                        media_state = "PLAYING"
                    last_gesture_time = now
                last_gesture = "PALM"

                cv2.putText(img, "PLAYING", (330, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 255, 0), 3)

            # =========================================
            # MODE SWITCH: MEDIA → VOLUME
            # =========================================
            else:
                last_gesture = "NONE"

                if gesture_mode == "MEDIA":
                    if smooth_val > VOLUME_ACTIVATION_THRESHOLD:
                        if volume_mode_start == 0:
                            volume_mode_start = now
                        elif now - volume_mode_start > MODE_SWITCH_DELAY:
                            gesture_mode = "VOLUME"
                            volume_mode_start = 0
                    else:
                        volume_mode_start = 0

                # =====================================
                # VOLUME MODE
                # =====================================
                if gesture_mode == "VOLUME":
                    if smooth_val < MUTE_ON:
                        muted = True
                    elif smooth_val > MUTE_OFF:
                        muted = False

                    if muted:
                        volume.SetMute(1, None)
                        pyautogui.press("volumemute")
                    else:
                        volume.SetMute(0, None)

                        volScalar = np.interp(smooth_val, [0.2, 1.0], [0.0, 1.0])
                        volScalar = volScalar ** 2

                        if now - last_update > UPDATE_INTERVAL:
                            volume.SetMasterVolumeLevelScalar(volScalar, None)
                            if abs(volScalar - prevVolScalar) > 0.02:
                                pyautogui.press("volumeup")
                                pyautogui.press("volumedown")
                                prevVolScalar = volScalar
                            last_update = now

            # Visuals
            cv2.circle(img, (x1, y1), 10, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (255, 0, 0), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    cv2.imshow("Gesture Based Volume & Media Controller", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
