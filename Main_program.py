import numpy as np
import cv2
import cv2.aruco as aruco
from OpenCV_scripts.Camera_calibration import Camera_calibration

cap = cv2.VideoCapture(0)


ret, mtx, dist, rvecs, tvecs = Camera_calibration()

# set dictionary size depending on the aruco marker selected
aruco_dict = aruco.Dictionary_get(aruco.DICT_ARUCO_ORIGINAL)

while True:
    markers_data = {}

    ret, frame = cap.read()

    # operations on the frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    # detector parameters can be set here (List of detection parameters[3])
    parameters = aruco.DetectorParameters_create()
    parameters.adaptiveThreshConstant = 10

    # lists of ids and the corners belonging to each id
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    # for i in zip(ids, corners):
    #     markers_data[i[0]] = i[1]


    # check if the ids list is not empty
    # if no check is added the code will crash
    if np.all(ids != None):

        # estimate pose of each marker and return the values
        # rvet and tvec-different from camera coefficients
        # rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners, 0.05, mtx, dist)
        # (rvec-tvec).any() # get rid of that nasty numpy value array error

        # for i in range(0, ids.size):
        #     # draw axis for the aruco markers
        #     aruco.drawAxis(frame, mtx, dist, rvec[i], tvec[i], 0.05)

        # draw a square around the markers
        aruco.drawDetectedMarkers(frame, corners)

        # code to show ids of the marker found
        strg = ''
        for i in range(0, ids.size):
            strg += str(ids[i][0]) + ', '

        cv2.putText(frame, "Id: " + strg, (0, 64), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)


    else:
        # code to show 'No Ids' when no markers are found
        cv2.putText(frame, "No Ids", (0, 64), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

# References
# 1. https://docs.opencv.org/3.4.0/d5/dae/tutorial_aruco_detection.html
# 2. https://docs.opencv.org/3.4.3/dc/dbb/tutorial_py_calibration.html
# 3. https://docs.opencv.org/3.1.0/d5/dae/tutorial_aruco_detection.html
