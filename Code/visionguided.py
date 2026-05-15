
#Vision-based red-cube picker arm


import cv2
import numpy as np
import serial
import time
import imutils

IP_WEBCAM_URL = "http://192.168.13.166:8080/video"
SERIAL_PORT = "COM7"
BAUDRATE = 9600

FRAME_WIDTH = 640
FRAME_HEIGHT = 480


ARM_BASE_X = 320
ARM_BASE_Y = 420

# Neutral/home servo positions
BASE_HOME = 90
SHOULDER_HOME = 100
ELBOW_HOME = 80
WRIST_HOME = 90
GRIPPER_OPEN = 80
GRIPPER_CLOSED = 10

# Current servo states
servo_base = BASE_HOME
servo_shoulder = SHOULDER_HOME
servo_elbow = ELBOW_HOME
servo_wrist = WRIST_HOME
servo_gripper = GRIPPER_OPEN

# Servo limits
B_MIN, B_MAX = 20, 160
S_MIN, S_MAX = 30, 150
E_MIN, E_MAX = 20, 160
W_MIN, W_MAX = 10, 170
G_MIN, G_MAX = 10, 90

# Detection tuning
CENTER_TOLERANCE_PX = 25

AREA_CLOSE_THRESHOLD = 12000
AREA_FAR_THRESHOLD = 1500

GRIP_CLOSE_DELAY = 0.5

# Motion smoothing
SMOOTHING_ALPHA = 0.2


last_command = ""
gripped = False
last_seen = time.time()


def clamp(v, a, b):
    return max(a, min(v, b))


def map_range(val, in_min, in_max, out_min, out_max):
    if in_max - in_min == 0:
        return out_min

    return int(
        out_min
        + ((val - in_min) / (in_max - in_min))
        * (out_max - out_min)
    )


def smooth(current, target, alpha=0.2):
    return int(alpha * target + (1 - alpha) * current)


#serial

ser = None

try:
    ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)
    time.sleep(2)
    print("Serial connected:", SERIAL_PORT)

except Exception as e:
    print("WARNING: Serial connection failed:", e)
    ser = None


def send_servo_angles(b, s, e, w, g):

    global last_command

    # Clamp values
    b = clamp(int(b), B_MIN, B_MAX)
    s = clamp(int(s), S_MIN, S_MAX)
    e = clamp(int(e), E_MIN, E_MAX)
    w = clamp(int(w), W_MIN, W_MAX)
    g = clamp(int(g), G_MIN, G_MAX)

    line = f"{b},{s},{e},{w},{g}\n"

    # Prevent serial flooding
    if line != last_command:

        if ser:
            ser.write(line.encode("utf-8"))

        print("SEND:", line.strip())

        last_command = line


#camera

cap = cv2.VideoCapture(IP_WEBCAM_URL)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

# Reduce latency buffer
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

# Initial pose
send_servo_angles(
    servo_base,
    servo_shoulder,
    servo_elbow,
    servo_wrist,
    servo_gripper,
)

#loop

try:

    while True:

        ret, frame = cap.read()

        # Safer reconnect
        if not ret or frame is None:

            print("Frame read failed. Reconnecting...")

            cap.release()

            time.sleep(1)

            cap = cv2.VideoCapture(IP_WEBCAM_URL)

            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

            continue

        frame = imutils.resize(frame, width=FRAME_WIDTH)

        blurred = cv2.GaussianBlur(frame, (7, 7), 0)

        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        #redcolor

        lower1 = np.array([0, 120, 70])
        upper1 = np.array([10, 255, 255])

        lower2 = np.array([170, 120, 70])
        upper2 = np.array([180, 255, 255])

        mask1 = cv2.inRange(hsv, lower1, upper1)
        mask2 = cv2.inRange(hsv, lower2, upper2)

        mask = cv2.bitwise_or(mask1, mask2)

        kernel = np.ones((5, 5), np.uint8)

        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        #contour

        cnts = cv2.findContours(
            mask.copy(),
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE,
        )

        cnts = imutils.grab_contours(cnts)

        if len(cnts) > 0:

            c = max(cnts, key=cv2.contourArea)

            area = cv2.contourArea(c)

            if area > 200:

                rect = cv2.minAreaRect(c)

                box = cv2.boxPoints(rect)

                # FIXED np.int0
                box = box.astype(int)

                M = cv2.moments(c)

                if M["m00"] != 0:

                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])

                else:

                    cx, cy = rect[0]

                    cx = int(cx)
                    cy = int(cy)

                #draw

                cv2.drawContours(frame, [box], 0, (0, 255, 0), 2)

                cv2.circle(frame, (cx, cy), 5, (255, 0, 0), -1)

                cv2.putText(
                    frame,
                    f"AREA:{int(area)}",
                    (cx + 10, cy - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 255, 255),
                    1,
                )

                last_seen = time.time()

                # ==========================================
                # CONTROL
                # ==========================================

                dx = cx - ARM_BASE_X

                # Wrist tracking
                target_wrist = map_range(
                    dx,
                    -FRAME_WIDTH // 2,
                    FRAME_WIDTH // 2,
                    W_MIN,
                    W_MAX,
                )

                target_wrist = clamp(
                    target_wrist,
                    W_MIN,
                    W_MAX,
                )

                # Minimal base movement
                target_base = BASE_HOME

                if abs(dx) > FRAME_WIDTH * 0.35:

                    nudge = map_range(
                        dx,
                        -FRAME_WIDTH // 2,
                        FRAME_WIDTH // 2,
                        B_MIN,
                        B_MAX,
                    )

                    target_base = int(
                        BASE_HOME + (nudge - BASE_HOME) * 0.25
                    )

                target_base = clamp(
                    target_base,
                    B_MIN,
                    B_MAX,
                )

                # Distance estimation via contour area
                target_shoulder = SHOULDER_HOME
                target_elbow = ELBOW_HOME

                if area > AREA_CLOSE_THRESHOLD:

                    target_shoulder -= 6
                    target_elbow += 6

                elif area < AREA_FAR_THRESHOLD:

                    target_shoulder += 6
                    target_elbow -= 6

                # Clamp
                target_shoulder = clamp(
                    target_shoulder,
                    S_MIN,
                    S_MAX,
                )

                target_elbow = clamp(
                    target_elbow,
                    E_MIN,
                    E_MAX,
                )

                #smooth

                servo_base = smooth(
                    servo_base,
                    target_base,
                    SMOOTHING_ALPHA,
                )

                servo_shoulder = smooth(
                    servo_shoulder,
                    target_shoulder,
                    SMOOTHING_ALPHA,
                )

                servo_elbow = smooth(
                    servo_elbow,
                    target_elbow,
                    SMOOTHING_ALPHA,
                )

                servo_wrist = smooth(
                    servo_wrist,
                    target_wrist,
                    SMOOTHING_ALPHA,
                )

                # ==================================
                # GRIPPING LOGIC
                # ==================================

                centered = abs(dx) < CENTER_TOLERANCE_PX

                ready_to_grip = (
                    centered
                    and AREA_FAR_THRESHOLD * 4 < area
                    < AREA_CLOSE_THRESHOLD * 1.6
                )

                # GRIP
                if ready_to_grip and not gripped:

                    servo_gripper = GRIPPER_CLOSED

                    send_servo_angles(
                        servo_base,
                        servo_shoulder,
                        servo_elbow,
                        servo_wrist,
                        servo_gripper,
                    )

                    time.sleep(GRIP_CLOSE_DELAY)

                    # Lift object
                    servo_shoulder = clamp(
                        servo_shoulder - 10,
                        S_MIN,
                        S_MAX,
                    )

                    servo_elbow = clamp(
                        servo_elbow + 15,
                        E_MIN,
                        E_MAX,
                    )

                    send_servo_angles(
                        servo_base,
                        servo_shoulder,
                        servo_elbow,
                        servo_wrist,
                        servo_gripper,
                    )

                    gripped = True

                else:

                    send_servo_angles(
                        servo_base,
                        servo_shoulder,
                        servo_elbow,
                        servo_wrist,
                        servo_gripper,
                    )

                # Lost object reset
                if gripped and area < 500:

                    print("Object lost -> opening gripper")

                    servo_gripper = GRIPPER_OPEN

                    gripped = False

        else:

            # Idle mode
            if time.time() - last_seen > 1.0 and not gripped:

                send_servo_angles(
                    servo_base,
                    servo_shoulder,
                    servo_elbow,
                    servo_wrist,
                    servo_gripper,
                )

        #ui

        cv2.circle(
            frame,
            (ARM_BASE_X, ARM_BASE_Y),
            6,
            (0, 0, 255),
            -1,
        )

        cv2.putText(
            frame,
            "Press q to quit",
            (10, 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 255),
            1,
        )

        cv2.imshow("frame", frame)
        cv2.imshow("mask", mask)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

        # FPS limiting
        time.sleep(0.03)

# =========================================================

except KeyboardInterrupt:

    print("Interrupted by user.")

# =========================================================

finally:

    print("Cleaning up...")

    try:

        send_servo_angles(
            BASE_HOME,
            SHOULDER_HOME,
            ELBOW_HOME,
            WRIST_HOME,
            GRIPPER_OPEN,
        )

        time.sleep(0.5)

    except:
        pass

    if ser:
        ser.close()

    cap.release()

    cv2.destroyAllWindows()
