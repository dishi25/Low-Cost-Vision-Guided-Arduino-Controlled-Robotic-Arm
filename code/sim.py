

import cv2
import numpy as np
import serial
import time
import imutils


IP_WEBCAM_URL = "http://192.168.13.166:8080/video"  
SERIAL_PORT = "COM7"                              
BAUDRATE = 9600


ARM_BASE_X = 320  
ARM_BASE_Y = 420  

FRAME_WIDTH = 640
FRAME_HEIGHT = 480

servo_base = 90
servo_shoulder = 100
servo_elbow = 80
servo_wrist = 90
servo_gripper = 80

B_MIN, B_MAX = 20, 160
S_MIN, S_MAX = 30, 150
E_MIN, E_MAX = 20, 160
W_MIN, W_MAX = 10, 170
G_MIN, G_MAX = 10, 90

# Behavior tuning:
CENTER_TOLERANCE_PX = 25     
AREA_CLOSE_THRESHOLD = 12000 
AREA_FAR_THRESHOLD = 1500    
GRIP_CLOSE_DELAY = 0.5       

def clamp(v, a, b):
    return max(a, min(b, v))

def map_range(val, in_min, in_max, out_min, out_max):
    # linear mapping
    if in_max - in_min == 0: return out_min
    return int(out_min + (float(val - in_min) / (in_max - in_min)) * (out_max - out_min))

# open serial
ser = None
try:
    ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)
    time.sleep(2)
    print("Serial opened:", SERIAL_PORT)
except Exception as e:
    print("WARNING: Could not open serial port:", e)
    ser = None

def send_servo_angles(b, s, e, w, g):
    # clamps
    b = clamp(int(b), B_MIN, B_MAX)
    s = clamp(int(s), S_MIN, S_MAX)
    e = clamp(int(e), E_MIN, E_MAX)
    w = clamp(int(w), W_MIN, W_MAX)
    g = clamp(int(g), G_MIN, G_MAX)
    line = f"{b},{s},{e},{w},{g}\n"
    if ser:
        ser.write(line.encode('utf-8'))
  
    print("SEND:", line.strip())
    return

cap = cv2.VideoCapture(IP_WEBCAM_URL)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

send_servo_angles(servo_base, servo_shoulder, servo_elbow, servo_wrist, servo_gripper)

last_seen = time.time()
gripped = False

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to read frame. Reconnecting...")
            time.sleep(0.5)
            cap = cv2.VideoCapture(IP_WEBCAM_URL)
            continue

        frame = imutils.resize(frame, width=FRAME_WIDTH)
        blurred = cv2.GaussianBlur(frame, (7,7), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        # Red color range (two ranges because red wraps in HSV)
        lower1 = np.array([0, 120, 70])
        upper1 = np.array([10, 255, 255])
        lower2 = np.array([170, 120, 70])
        upper2 = np.array([180, 255, 255])

        mask1 = cv2.inRange(hsv, lower1, upper1)
        mask2 = cv2.inRange(hsv, lower2, upper2)
        mask = cv2.bitwise_or(mask1, mask2)

        # Morphology to clear noise
        kernel = np.ones((5,5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # Find contours
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        center = None

        if len(cnts) > 0:
            # largest contour = assumed cube
            c = max(cnts, key=cv2.contourArea)
            area = cv2.contourArea(c)
            # filter tiny noise
            if area > 200:
                rect = cv2.minAreaRect(c)
                box = cv2.boxPoints(rect)
                box = np.int8(box)
                M = cv2.moments(c)
                if M["m00"] != 0:
                    cx = int(M["m10"]/M["m00"])
                    cy = int(M["m01"]/M["m00"])
                else:
                    cx, cy = rect[0]
                    cx, cy = int(cx), int(cy)

                # angle of rect: rotation of the box
                angle = rect[2]
                # rect returns angle in [-90,0) in many cases; normalize
                if rect[1][0] < rect[1][1]:
                    angle = angle + 90

                # draw for debug
                cv2.drawContours(frame, [box], 0, (0,255,0), 2)
                cv2.circle(frame, (cx, cy), 5, (255,0,0), -1)
                cv2.putText(frame, f"A:{int(area)} Ang:{int(angle)}", (cx+10, cy-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)

                last_seen = time.time()
                center = (cx, cy)

                # CONTROL LOGIC:
                # 1) Compute horizontal offset relative to arm base to decide wrist rotation primarily.
                dx = cx - ARM_BASE_X
                dy = ARM_BASE_Y - cy  # positive when cube is in front of arm (upwards)

                # Map dx to wrist rotation (wrist does the bulk of turning)
                # If object is left of base, rotate appropriate direction.
                # Map dx in [-FRAME_WIDTH/2, FRAME_WIDTH/2] to wrist angle range [W_MIN,W_MAX]
                wrist_angle = map_range(dx, -FRAME_WIDTH//2, FRAME_WIDTH//2, W_MAX, W_MIN)
                wrist_angle = clamp(wrist_angle, W_MIN, W_MAX)

                # Base movement minimal: small adjustment if dx very large
                base_angle = servo_base
                if abs(dx) > FRAME_WIDTH*0.35:
                    # small nudge of base (very minimal)
                    base_nudge = map_range(dx, -FRAME_WIDTH//2, FRAME_WIDTH//2, B_MAX, B_MIN)
                    base_angle = int(servo_base + (base_nudge - servo_base) * 0.25)  # fraction move
                    base_angle = clamp(base_angle, B_MIN, B_MAX)

                # Adjust shoulder/elbow minimally based on area (distance)
                shoulder_angle = servo_shoulder
                elbow_angle = servo_elbow
                if area > AREA_CLOSE_THRESHOLD:
                    # object is too close -> raise shoulder slightly and retract elbow
                    shoulder_angle = clamp(servo_shoulder - 6, S_MIN, S_MAX)
                    elbow_angle = clamp(servo_elbow + 6, E_MIN, E_MAX)
                elif area < AREA_FAR_THRESHOLD:
                    # object far -> extend elbow a bit and lower shoulder slightly
                    shoulder_angle = clamp(servo_shoulder + 6, S_MIN, S_MAX)
                    elbow_angle = clamp(servo_elbow - 6, E_MIN, E_MAX)
                # otherwise keep them nearly the same (minimal movement)

                # Decide gripper action: if centered horizontally and area in right range -> grip
                gripper_angle = servo_gripper  # default keep
                centered = abs(cx - ARM_BASE_X) < CENTER_TOLERANCE_PX
                ready_to_grip = centered and (AREA_FAR_THRESHOLD*4 < area < AREA_CLOSE_THRESHOLD*1.6)

                if ready_to_grip and (not gripped):
                    # Move gripper to closing angle, then lift slightly
                    send_servo_angles(base_angle, shoulder_angle, elbow_angle, wrist_angle, G_MIN)  # close
                    time.sleep(GRIP_CLOSE_DELAY)
                    # lift a bit after gripping
                    send_servo_angles(base_angle, clamp(shoulder_angle-10, S_MIN, S_MAX),
                                      clamp(elbow_angle+15, E_MIN, E_MAX), wrist_angle, G_MIN)
                    gripped = True
                elif not ready_to_grip and gripped:
                    # keep holding pose (do nothing) - user can add place logic later
                    pass
                else:
                    # Regular following behavior (approach)
                    send_servo_angles(base_angle, shoulder_angle, elbow_angle, wrist_angle, servo_gripper)

                # update cached servo states to the values we *sent*
                servo_base = base_angle
                servo_shoulder = shoulder_angle
                servo_elbow = elbow_angle
                servo_wrist = wrist_angle
                # gripper updated only when gripping
                if ready_to_grip:
                    servo_gripper = G_MIN

        else:
            # no contours found
            # small safety: if nothing seen for a while, open gripper slightly and hold
            if time.time() - last_seen > 1.0 and not gripped:
                # safe idle pose (no big movements)
                send_servo_angles(servo_base, servo_shoulder, servo_elbow, servo_wrist, servo_gripper)

        # show debugging window
        cv2.circle(frame, (ARM_BASE_X, ARM_BASE_Y), 6, (0,0,255), -1)
        cv2.putText(frame, "Press q to quit", (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255), 1)
        cv2.imshow("frame", frame)
        cv2.imshow("mask", mask)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

except KeyboardInterrupt:
    pass
finally:
    print("Exiting, sending safe stop and releasing resources...")
    try:
        send_servo_angles(90, 100, 80, 90, 80)  # rest pose
        time.sleep(0.3)
    except:
        pass
    if ser:
        ser.close()
    cap.release()
    cv2.destroyAllWindows()
