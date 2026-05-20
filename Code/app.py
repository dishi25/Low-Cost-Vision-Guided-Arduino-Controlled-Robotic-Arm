from flask import Flask, Response, render_template_string, request
import cv2
import numpy as np

app = Flask(__name__)


camera_url = "http://192.168.137.238:8080/video"
camera = cv2.VideoCapture(camera_url)


last_message = "No action yet."

html_page = """
<!DOCTYPE html>
<html>
<head>
    <title>📱 Phone Camera Stream</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; background: #f4f4f4; }
        h1 { color: #333; }
        img { border: 4px solid #333; border-radius: 12px; margin-top: 20px; }
        .controls { margin-top: 20px; }
        button {
            padding: 12px 20px;
            font-size: 16px;
            border: none;
            border-radius: 8px;
            margin: 5px;
            cursor: pointer;
            background-color: #4CAF50;
            color: white;
        }
        button.red { background-color: #e74c3c; }
        button.green { background-color: #2ecc71; }
        .status { margin-top: 20px; font-size: 18px; color: #333; }
    </style>
</head>
<body>
    <h1>📷 Live Phone Camera Stream</h1>
    <img src="/video" width="640" height="480">

    <div class="controls">
        <form action="/detect" method="post">
            <button class="red" name="color" value="red">🔴 Pick Red Object</button>
            <button class="green" name="color" value="green">🟢 Pick Green Object</button>
        </form>
    </div>

    <div class="status">
        <p>{{ message }}</p>
    </div>
</body>
</html>
"""

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template_string(html_page, message=last_message)

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/detect', methods=['POST'])
def detect():
    global last_message
    color = request.form['color']

    # Capture one frame
    success, frame = camera.read()
    if not success:
        last_message = "❌ Could not read camera"
        return render_template_string(html_page, message=last_message)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    if color == "red":
        # Red color range
        lower1 = np.array([0, 120, 70])
        upper1 = np.array([10, 255, 255])
        lower2 = np.array([170, 120, 70])
        upper2 = np.array([180, 255, 255])
        mask1 = cv2.inRange(hsv, lower1, upper1)
        mask2 = cv2.inRange(hsv, lower2, upper2)
        mask = mask1 | mask2
    else:
        # Green color range
        lower = np.array([40, 50, 50])
        upper = np.array([90, 255, 255])
        mask = cv2.inRange(hsv, lower, upper)

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        c = max(contours, key=cv2.contourArea)
        (x, y, w, h) = cv2.boundingRect(c)
        cx = x + w // 2
        cy = y + h // 2
        last_message = f"🎯 Found {color.capitalize()} Object at (x={cx}, y={cy})"
    else:
        last_message = f"⚠️ No {color} object detected."

    return render_template_string(html_page, message=last_message)

if __name__ == "__main__":
    app.run(debug=True)
