# <img src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png" width="35"> Low-Cost Vision-Guided Robotic Arm for Automated Object Sorting

<div align="center">

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green?style=for-the-badge&logo=opencv)
![Arduino](https://img.shields.io/badge/Arduino-Embedded%20Systems-00979D?style=for-the-badge&logo=arduino)

### Intelligent Vision-Based Pick-and-Place Automation System

</div>

---

## <img src="https://cdn-icons-png.flaticon.com/512/1828/1828919.png" width="22"> Project Overview

This project presents a **low-cost vision-guided robotic arm system** capable of performing real-time **object detection, classification, and automated sorting** using computer vision and embedded control.

A webcam continuously monitors the workspace while OpenCV-based image processing identifies objects based on visual characteristics such as color, contour, and shape. The processed data is transmitted to an Arduino through serial communication, enabling precise control of servo motors for robotic pick-and-place operations.

The system demonstrates concepts used in:

- Industry 4.0
- Smart Manufacturing
- Industrial Automation
- Intelligent Robotics
- Machine Vision Systems

---

## <img src="https://cdn-icons-png.flaticon.com/512/3523/3523887.png" width="22"> Key Features

- Real-time object detection and tracking
- Automated robotic pick-and-place operation
- Vision-guided servo motor control
- Low-cost and scalable architecture
- Embedded serial communication system
- Intelligent sorting mechanism
- Modular and upgrade-friendly design

---

## <img src="https://cdn-icons-png.flaticon.com/512/2721/2721297.png" width="22"> Tech Stack

<div align="center">

| Technology | Description |
|---|---|
| <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" width="40"><br>Python | Core programming language |
| <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/opencv/opencv-original.svg" width="40"><br>OpenCV | Computer vision and image processing |
| <img src="https://cdn.worldvectorlogo.com/logos/arduino-1.svg" width="40"><br>Arduino | Embedded system controller |
| <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/cplusplus/cplusplus-original.svg" width="40"><br>C++ | Arduino firmware programming |
| <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/numpy/numpy-original.svg" width="40"><br>NumPy | Numerical computations |
| <img src="https://img.icons8.com/fluency/48/serial-tasks.png" width="40"><br>PySerial | Serial communication |
| <img src="https://img.icons8.com/fluency/48/robot-2.png" width="40"><br>Servo Control | Robotic arm actuation |

</div>

---

## <img src="https://cdn-icons-png.flaticon.com/512/1048/1048953.png" width="22"> Hardware Components

| Component | Function |
|---|---|
| Arduino Uno / Mega | Main embedded controller |
| 4-DOF Robotic Arm | Pick-and-place mechanism |
| Servo Motors | Joint and gripper actuation |
| USB / IP Webcam | Real-time workspace monitoring |
| External Power Supply | Stable system power delivery |
| Sorting Bins | Object segregation |

---

## <img src="https://cdn-icons-png.flaticon.com/512/1006/1006363.png" width="22"> Software Requirements

<div align="center">

| Requirement | Purpose |
|---|---|
| <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" width="40"><br>Python 3.x | Main software environment |
| <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/opencv/opencv-original.svg" width="40"><br>OpenCV | Object detection and tracking |
| <img src="https://cdn.worldvectorlogo.com/logos/arduino-1.svg" width="40"><br>Arduino IDE | Arduino programming and uploading |
| <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/numpy/numpy-original.svg" width="40"><br>NumPy | Matrix and array operations |
| <img src="https://img.icons8.com/fluency/48/serial-tasks.png" width="40"><br>PySerial | Python-Arduino communication |
| <img src="https://img.icons8.com/color/48/artificial-intelligence.png" width="40"><br>Imutils | Image processing utilities |

</div>

### Installation

```bash
pip install opencv-python pyserial numpy imutils
```

---

## <img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" width="22"> Fields

<div align="center">

| Field | Domain |
|---|---|
| <img src="https://img.icons8.com/color/48/motherboard.png" width="40"><br>Embedded Systems | Hardware-software interfacing and control |
| <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/opencv/opencv-original.svg" width="40"><br>OpenCV | Real-time image processing |
| <img src="https://img.icons8.com/color/48/computer-vision.png" width="40"><br>Computer Vision | Object detection and visual tracking |
| <img src="https://img.icons8.com/fluency/48/robot-2.png" width="40"><br>Robotics & Automation | Intelligent robotic control systems |

</div>

---

## <img src="https://cdn-icons-png.flaticon.com/512/1827/1827933.png" width="22"> System Workflow

```text
Camera Feed
      ↓
OpenCV Image Processing
      ↓
Object Detection & Classification
      ↓
Serial Communication (Python → Arduino)
      ↓
Servo Motor Control
      ↓
Robotic Pick-and-Place Operation
      ↓
Automated Object Sorting
```

---

## <img src="https://cdn-icons-png.flaticon.com/512/2620/2620999.png" width="22"> System Architecture

```text
┌──────────────┐
│   Webcam     │
└──────┬───────┘
       ↓
┌──────────────┐
│ OpenCV + AI  │
│ Image Engine │
└──────┬───────┘
       ↓
┌──────────────┐
│ Python Logic │
└──────┬───────┘
       ↓
┌──────────────┐
│ Serial Comm  │
└──────┬───────┘
       ↓
┌──────────────┐
│   Arduino    │
└──────┬───────┘
       ↓
┌──────────────┐
│ Servo Motors │
└──────┬───────┘
       ↓
┌──────────────┐
│ Object Sort  │
└──────────────┘
```

---

## <img src="https://cdn-icons-png.flaticon.com/512/2920/2920349.png" width="22"> Applications

- Industrial Automation
- Smart Manufacturing Systems
- Packaging and Sorting Lines
- Recycling Automation
- Warehouse Management
- Educational Robotics
- Intelligent Conveyor Systems

---

## <img src="https://cdn-icons-png.flaticon.com/512/595/595067.png" width="22"> Engineering Challenges

- Lighting conditions affect detection accuracy
- Servo calibration impacts positioning precision
- Camera placement influences tracking stability
- Mechanical vibration reduces repeatability
- Limited classification capability for complex objects

---

## <img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" width="22"> Future Enhancements

- AI/ML-based object recognition
- Conveyor belt integration
- Multi-object simultaneous detection
- Wireless robotic control
- IoT-enabled monitoring dashboard
- Upgrade to industrial-grade 6-DOF robotic arm
- Reinforcement learning-based grasp optimization

---

## <img src="https://cdn-icons-png.flaticon.com/512/2721/2721279.png" width="22"> Skills Demonstrated

- Computer Vision with OpenCV
- Embedded Systems Development
- Arduino Interfacing
- Robotics and Automation
- Serial Communication Protocols
- Servo Motor Control
- Real-Time Image Processing

---

## <img src="https://cdn-icons-png.flaticon.com/512/942/942748.png" width="22"> Project Structure

```bash
├── Hardware/
│   └── robotic_arm_control.ino
│
├── Code/
│   └── vision_guided_sorting.py
│
├── Media/
│   └── system_demo.png
│
├── README.md
└── requirements.txt
```

---

## <img src="https://cdn-icons-png.flaticon.com/512/1077/1077114.png" width="22"> Team

### Developers

- **Dishika G** — [@dishi25](https://github.com/dishi25)
- **Gurupriyaa N** — [@Gurupriyaa-28](https://github.com/Gurupriyaa-28)

---

## <img src="https://cdn-icons-png.flaticon.com/512/2991/2991148.png" width="22"> References

- Arduino Official Documentation
- OpenCV Official Documentation
- Research Papers on Vision-Guided Robotics
- Embedded Automation System Design Resources

---

## <img src="https://cdn-icons-png.flaticon.com/512/190/190411.png" width="22"> Project Vision

This project demonstrates how low-cost embedded systems and computer vision can be integrated to build scalable robotic systems inspired by modern industrial automation and smart manufacturing environments.

---

<div align="center">
  
## Thank you

</div>
