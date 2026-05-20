import cv2
import numpy as np

# Create a black image 400x400
img = np.zeros((400, 400, 3), dtype=np.uint8)

# Draw a blue rectangle
cv2.rectangle(img, (50, 50), (350, 350), (255, 0, 0), 5)

# Draw a green circle inside the rectangle
cv2.circle(img, (200, 200), 100, (0, 255, 0), -1)

# Show the image in a window
cv2.imshow('OpenCV & NumPy Test', img)

# Wait until a key is pressed
cv2.waitKey(0)
cv2.destroyAllWindows()

# Print versions to confirm installation
print("NumPy version:", np._version_)
print("OpenCV version:", cv2._version_)