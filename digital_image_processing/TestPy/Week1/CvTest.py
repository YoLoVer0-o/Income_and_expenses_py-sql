import cv2

img = cv2.imread("340288627_1076117436528898_2722072001963406275_n.jpg")
grayscale = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

edge = cv2.Canny(img,200,300)

cv2.imshow("Image Displaying", img)
cv2.imshow("grayscale", grayscale)
cv2.imshow("Edge canny", edge)


cv2.waitKey()
cv2.destroyAllWindows()