import cv2
import numpy as np

# Load the image
image = cv2.imread('Autonomous/m1.jpg')

# Define a callback function for mouse events
def get_coordinates(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f'Coordinates: ({x}, {y})')

# Create a window and set the callback function
cv2.namedWindow('Image')
cv2.setMouseCallback('Image', get_coordinates)

# Display the image and wait for the user to click
cv2.imshow('Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
