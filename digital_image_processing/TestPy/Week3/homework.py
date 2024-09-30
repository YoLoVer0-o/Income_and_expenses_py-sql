import cv2
from matplotlib import pyplot as plt

img = cv2.imread(r"C:\Learn Python\TestPy\Week3\asset\babu.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
ret, threshold_global = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
ret, binary_inv = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)
MEAN_C = cv2.adaptiveThreshold(
    gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2
)
GAUSSIAN_C = cv2.adaptiveThreshold(
    gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
)
equalized_img = cv2.equalizeHist(gray, 255)
medianBlur = cv2.medianBlur(gray, 5)
GaussianBlur = cv2.GaussianBlur(gray, (7, 7), 0)


# cv2.imshow("bun",img)
# cv2.imshow("gray",gray)
# cv2.imshow("binary",binary)
# cv2.imshow("binary_inv",binary_inv)
# cv2.imshow("binary_inv",adp)
cv2.imshow("equalized_img", equalized_img)
cv2.imshow("filterimg", medianBlur)
cv2.imshow("filterimg1", GaussianBlur)
title = [
    "original",
    "gray",
    "threshold_global",
    "threshold_global_inv",
    "MEAN_C",
    "GAUSSIAN_C",
    "equalized_img",
    "medianBlur",
    "GaussianBlur",
]
image = [
    img,
    gray,
    threshold_global,
    binary_inv,
    MEAN_C,
    GAUSSIAN_C,
    equalized_img,
    medianBlur,
    GaussianBlur,
]

for i in range(9):
    plt.subplot(3, 3, i + 1), plt.imshow(image[i], "gray")
    plt.title(title[i])
    plt.xticks([]), plt.yticks([])
plt.show()


cv2.waitKey(0)
cv2.destroyAllWindows()
