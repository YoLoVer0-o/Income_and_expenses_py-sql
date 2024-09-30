import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread(r"C:\Learn Python\Threshold&Reshape\babu.jpg", 0)

print(img.shape)
new_img = img[0:100, 0:180]
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.imshow(img, cmap="gray")
plt.title("Original Image")
plt.axis("off")
plt.subplot(1, 2, 2)
plt.imshow(new_img, cmap="gray")
plt.title("Reshape Image")
plt.axis("off")

plt.show()