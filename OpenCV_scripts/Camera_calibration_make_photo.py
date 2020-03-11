import numpy as np
import cv2
from time import time
c_time = time()
# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6 * 7, 3), np.float32)
objp[:, :2] = np.mgrid[0:7, 0:6].T.reshape(-1, 2)

# Arrays to store object points and image points from all the images.
objpoints = []  # 3d point in real world space
imgpoints = []  # 2d points in image plane.

cap = cv2.VideoCapture(0)
cv2.namedWindow("Capture", 0)
cv2.namedWindow("Capture_modified", 0)

num = 9
try:
    while True:
        ret, img = cap.read()
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # gray = (np.float32(img), cv2.COLOR_RGB2GRAY)
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (7, 6), None)

        # If found, add object points, image points (after refining them)

        cv2.imshow("Capture", img)
        if ret:
            if time() - c_time > 500:
                objpoints.append(objp)

                cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
                imgpoints.append(corners)

                # Draw and display the corners
                image = cv2.drawChessboardCorners(img, (7, 6), corners, ret)
                cv2.imshow("Capture_modified", image)
                cv2.imwrite(f"Calibration_images/Calibration_image_#{num}.png", img)
                cv2.waitKey(100)
                num += 1
                ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
        cv2.waitKey(1)
finally:
    cv2.destroyAllWindows()
