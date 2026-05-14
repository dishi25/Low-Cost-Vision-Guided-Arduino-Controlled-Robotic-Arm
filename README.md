## Low-Cost Vision Guided Arduino Controlled Robotic Arm
A smart automation project that combines computer vision and embedded control to detect, classify, and sort objects automatically using a robotic arm.

**Project Overview** <br>
- This project presents a low-cost vision-guided robotic arm system designed for automated object sorting. A webcam captures real-time images of objects placed in the workspace, and OpenCV processes the images to identify objects based on features such as color or shape. The detected result is sent to an Arduino, which controls servo motors to move the robotic arm and place the object into the correct sorting bin.

The system demonstrates intelligent automation concepts used in Industry 4.0 and smart manufacturing.

**Technologies Used**

- Computer Vision

- OpenCV

- Arduino Programming

- Embedded Systems

- Servo Motor Control

- Serial Communication

- Automation & Robotics


🧩 Hardware Components
| Component         | Purpose                    |
| ----------------- | -------------------------- |
| Arduino Uno/Mega  | Main controller            |
| 4-DOF Robotic Arm | Pick-and-place mechanism   |
| Servo Motors      | Joint and gripper movement |
| USB Webcam        | Captures workspace images  |
| Power Supply      | System power               |
| Sorting Bins      | Object placement           |

💻 **Software Requirements**

- Python

- OpenCV

- Arduino IDE

- PySerial

⚙️ **Working Principle**

- Webcam captures live video feed.

- OpenCV processes the image.

- Objects are detected and classified.

- Python sends classification data to Arduino through serial communication.

- Arduino controls servo motors.

- Robotic arm picks the object.

- Object is placed into the correct sorting bin

🔌 **System Architecture**

Camera → OpenCV Processing → Classification → Serial Communication → Arduino → Servo Motors → Object Sorting

📊 **Features**

- Real-time object detection

- Automated object sorting

- Vision-guided robotic movement

- Low-cost implementation

- Easy scalability for industrial applications


🚨 **Applications**

- Industrial automation

- Smart manufacturing

- Packaging systems

- Recycling systems

- Warehouse sorting

- Educational robotics projects


⚠️ **Challenges**

- Lighting affects image detection accuracy

- Servo calibration required

- Limited object classification capability

- Camera positioning impacts performance



🔮 **Future Scope**

- AI/ML-based object recognition

- Conveyor belt integration

- IoT-enabled monitoring

- Multi-object detection

- Wireless robotic control

- Upgrading to 6-DOF robotic arm


🛠️ **Skills Gained**

- Computer Vision with OpenCV

- Embedded Systems Programming

- Arduino Interfacing

- Robotics & Automation

- Serial Communication

- Servo Motor Control



👩‍💻 **Team**

- Dishika G @dishi25

- Gurupriyaa N @Gurupriyaa-28

📚 **References**

- Arduino Official Documentation

- OpenCV Documentation

- Research Papers on Vision Guided Robotics
