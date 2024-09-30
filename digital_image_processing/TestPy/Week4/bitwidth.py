import cv2
from matplotlib import pyplot as plt

dog_img = cv2.imread(r"C:\Learn Python\TestPy\Week4\dog.png")
cat_img = cv2.imread(r"C:\Learn Python\TestPy\Week4\cat.png")

and_img = cv2.bitwise_and(dog_img, cat_img)
or_img = cv2.bitwise_or(dog_img, cat_img)
xor_img = cv2.bitwise_xor(dog_img, cat_img)
not_img = cv2.bitwise_not(
    dog_img,
)

cv2.imshow("Original Dog Image", dog_img)
cv2.imshow("Original Cat Image", cat_img)
cv2.imshow("AND Image", and_img)
cv2.imshow("Or Image", or_img)
cv2.imshow("XOR Image", xor_img)
cv2.imshow("NOT Image", not_img)

title = [
    "Original Dog Image",
    "Original Cat Image",
    "AND Image",
    "Or Image",
    "XOR Image",
    "NOT Image",
]
image = [
    dog_img,
    cat_img,
    and_img,
    or_img,
    xor_img,
    not_img,
]

for i in range(6):
    plt.subplot(2, 3, i + 1)
    plt.imshow(image[i])
    plt.title(title[i])
    plt.xticks([]), plt.yticks([])
plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()
