import cv2
import serial
import time
arduino = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)

camera_url = "http://192.168.0.101:8080/video" 
cap = cv2.VideoCapture(camera_url)

# Initial servo angles
base = 90
shoulder = 90
elbow = 90
wrist = 90
gripper = 90

kx = 0.02  
ky = 0.05  
BASE_MIN, BASE_MAX = 70, 110 

def send_servo(name, angle):
    angle = max(0, min(180, int(angle)))
    cmd = f"{name.upper()}:{angle}\n"
    arduino.write(cmd.encode())
    time.sleep(0.03)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (640, 480))
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Red color detection
    lower1 = (0, 120, 70)
    upper1 = (10, 255, 255)
    lower2 = (170, 120, 70)
    upper2 = (180, 255, 255)
    mask = cv2.inRange(hsv, lower1, upper1) + cv2.inRange(hsv, lower2, upper2)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cx, cy = 320, 240

    if contours:
        c = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(c)
        if area > 1000:
            x, y, w, h = cv2.boundingRect(c)
            objX = x + w // 2
            objY = y + h // 2

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.circle(frame, (objX, objY), 5, (255, 0, 0), -1)

            errX = objX - cx
            errY = cy - objY

            # Gentle base adjustment
            base += errX * kx
            base = max(BASE_MIN, min(BASE_MAX, base))

            # Normal shoulder adjustment
            shoulder += errY * ky
            shoulder = max(0, min(180, shoulder))

            send_servo("base", base)
            send_servo("shoulder", shoulder)

    cv2.imshow("Red Box Tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()
