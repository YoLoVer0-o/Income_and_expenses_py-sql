import cv2
import numpy as np
import matplotlib.pyplot as plt


def apply_threshold(image, threshold):
    _, binary_image = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
    return binary_image

image = cv2.imread(r"C:\Learn Python\Threshold&Reshape\babu.jpg", cv2.IMREAD_GRAYSCALE)

threshold = 128
binary_image = apply_threshold(image, threshold)
plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.imshow(image, cmap="gray")
plt.title("Original Image")
plt.axis("off")
plt.subplot(1, 2, 2)
plt.imshow(binary_image, cmap="gray")
plt.title(f"Binary Image (Threshold={threshold})")
plt.axis("off")

plt.show()
