import cv2 

# Read the image
img = cv2.imread("340288627_1076117436528898_2722072001963406275_n.jpg")
cv2.imshow("test",img)
# Display the original image
# cv2.imshow("Original Image",img)

# Apply median blur
median = cv2.medianBlur(img, 5)

# Display the filtered image
cv2.imshow("Median Filter", median)

# Wait for a key press and close the windows
cv2.waitKey(0)
cv2.destroyAllWindows()
