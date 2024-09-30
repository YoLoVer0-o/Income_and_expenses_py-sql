# import cv2
# import numpy as np


# def detect_color_from_video(video_path, lower_color, upper_color):
#     cap = cv2.VideoCapture(video_path)

#     while True:
#         ret, frame = cap.read()

#         if not ret:
#             break

#         hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#         mask = cv2.inRange(hsv_frame, lower_color, upper_color)
#         result = cv2.bitwise_and(frame, frame, mask=mask)
#         cv2.imshow("Original Frame", frame)
#         cv2.imshow("Masked Frame", result)
#         if cv2.waitKey(1) & 0xFF == ord("q"):
#             break
#     cap.release()
#     cv2.destroyAllWindows()


# lower_red = np.array([0, 120, 70])
# upper_red = np.array([10, 255, 255])
# video_path = r"C:\Learn Python\VideoColorDetect\color_video.mp4"
# detect_color_from_video(video_path, lower_red, upper_red)


import cv2
import numpy as np


def detect_colored_object(video_path, lower_color, upper_color):
    cap = cv2.VideoCapture(video_path)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_frame, lower_color, upper_color)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 500:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imshow("Original Frame", frame)
        cv2.imshow("Masked Frame", mask)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()


#  color_ranges
lower_red = np.array([0, 120, 70])
upper_red = np.array([10, 255, 255])

video_path = r"C:\Learn Python\VideoColorDetect\object_video.mp4"
detect_colored_object(video_path, lower_red, upper_red)
