## <img src="https://cdn.worldvectorlogo.com/logos/arduino-1.svg" width="24"> Arduino Servo Tracking Module (.ino)


---

This `.ino` module controls the robotic arm servos using real-time positional data received from the OpenCV vision system.

The program receives object tracking coordinates through serial communication and dynamically adjusts the:

- Base servo for horizontal alignment
- Shoulder servo for vertical tracking

The control logic enables smooth real-time movement of the robotic arm to follow a detected red object captured through the vision system.

---

### <img src="https://img.icons8.com/fluency/48/workflow.png" width="22"> Workflow

```text
Camera Detection
        ↓
OpenCV Tracking
        ↓
Serial Communication
        ↓
Arduino Servo Control
        ↓
Robotic Arm Movement
```

---

### <img src="https://img.icons8.com/fluency/48/settings.png" width="22"> Purpose

This module acts as the embedded hardware control layer of the project, enabling real-time vision-guided robotic motion and forming the foundation for automated pick-and-place operations.

--- 
