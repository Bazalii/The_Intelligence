import numpy as np
import cv2
import os


def Camera_calibration(**kwargs):
    '''
    :param kwargs:
    :key show принимает True или False
    :return: ret, mtx, dist, rvecs, tvecs калибровочные параметры.
    '''
    ret, mtx, dist, rvecs, tvecs = None, None, None, None, None
    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((6 * 7, 3), np.float32)
    objp[:, :2] = np.mgrid[0:7, 0:6].T.reshape(-1, 2)

    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d point in real world space
    imgpoints = []  # 2d points in image plane.

    images = os.listdir("OpenCV_scripts/Calibration_images")

    if kwargs.get("show", False):
        cv2.namedWindow("Capture")

    for fname in images:
        img = cv2.imread("OpenCV_scripts/Calibration_images/" + fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (7, 6), None)

        # If found, add object points, image points (after refining them)
        if ret:
            objpoints.append(objp)

            cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners)

            # Draw and display the corners
            cv2.drawChessboardCorners(img, (7, 6), corners, ret)
            cv2.imshow('Capture', img)
            cv2.waitKey(1000)
            ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    if kwargs.get("show", False):
        cv2.destroyAllWindows()

    return ret, mtx, dist, rvecs, tvecs
