from typing import Iterable

import numpy as np
import cv2
import cv2.aruco as aruco

from Moving_systems.Data_base import *
from OpenCV_scripts.Camera_calibration import Camera_calibration
from Moving_systems.Manipulator_shell import Manipulator
from Classes.Point_class import Point
from Classes.Vector_class import Vector
from Gripper_suspension.Gripper_suspension_resiver import GripSuspension

gripper_suspension = GripSuspension("/dev/ttyACM0", 115200)

cap = cv2.VideoCapture(0)

ret, mtx, dist, rvecs, tvecs = Camera_calibration()

# set dictionary size depending on the aruco marker selected
aruco_dict = aruco.Dictionary_get(aruco.DICT_ARUCO_ORIGINAL)
parameters = aruco.DetectorParameters_create()
parameters.adaptiveThreshConstant = 10

ADAPTIVE_CONSTANT = None

manipulator = Manipulator("", "sa", "")
find_zero_flag = False

mid_zero = None


def find_middle(points: Iterable):
    summ_x = 0
    summ_y = 0
    for p in points:
        summ_x += int(p[0])
        summ_y += int(p[1])
    return summ_x / len(points), summ_y / len(points)


# Find zero and constants
while not find_zero_flag:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    x_vector = None
    y_vector = None
    move_vector = None
    frame_center = Point(frame.shape[1] / 2, frame.shape[0] / 2)
    if ids is not None:
        ids_dict = {}
        ids_middle = {}
        for i in range(ids.size):
            ids_dict[int(ids[i][0])] = corners[i][0]
            ids_middle[int(ids[i][0])] = find_middle(corners[i][0])

        strg = ''
        for i in range(0, ids.size):
            strg += str(ids[i][0]) + ', '
            _id = ids[i][0]
            if _id in zero_ids:
                if _id == 0:
                    mid_zero = ids_middle[ids[i][0]]
                    ADAPTIVE_CONSTANT = Zero_marker0.size / \
                                        Vector(ids_dict[ids[i][0]][0], ids_dict[ids[i][0]][1]).length()
                    move_vector = Vector(mid_zero, frame_center)
                    if move_vector.length() > 2:
                        move_vector.set_length(move_vector.length() * ADAPTIVE_CONSTANT)
                        manipulator.move_by_vector(move_vector)

                if mid_zero is not None:
                    if _id == 1:
                        if ids_middle.get(0, False):
                            x_vector = Vector(ids_middle[0], ids_middle[1])
                            x_vector_move = x_vector.copy()
                            x_vector_move.set_length(x_vector.length() * ADAPTIVE_CONSTANT)
                    if _id == 2:
                        if ids_middle.get(0, False):
                            y_vector = Vector(ids_middle[0], ids_middle[2])
                            y_vector_move = y_vector.copy()
                            y_vector_move.set_length(y_vector.length() * ADAPTIVE_CONSTANT)

                    cv2.line(frame, (int(mid_zero[0]), int(mid_zero[1])),
                             (int(frame_center.x), int(frame_center.y)), (0, 200, 0), 3)
                    cv2.putText(frame, "(0, 0)", (int(mid_zero[0]),
                                                  int(mid_zero[1])), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (200, 0, 0))

                    # print(f"Zero: {mid_zero}")
                    if x_vector is not None:
                        cv2.line(frame, (int(mid_zero[0]), int(mid_zero[1])),
                                 (int(x_vector.end_point.x), int(x_vector.end_point.y)), (0, 0, 200), 3)
                        print(f"X: {x_vector.end_point}")
                    if y_vector is not None:
                        cv2.line(frame, (int(mid_zero[0]), int(mid_zero[1])),
                                 (int(y_vector.end_point.x), int(y_vector.end_point.y)), (0, 200, 0), 3)
                        # print(f"Y: {y_vector.end_point}")

    if move_vector is None and y_vector is not None and x_vector is not None:
        manipulator_zero_poss = manipulator.get_pos()
        x_vector_move.move_to_point(manipulator_zero_poss)
        x_vector_move.set_length(x_vector.length() * ADAPTIVE_CONSTANT)
        y_vector_move.move_to_point(manipulator_zero_poss)
        y_vector_move.set_length(y_vector.length() * ADAPTIVE_CONSTANT)
        gripper_suspension.set_zero()
        while gripper_suspension.latest_val()[0].start_point.z < 100:
            manipulator.move_by_vector(Point(0, 0, -1))
        manipulator_zero_poss = manipulator.get_pos()
        manipulator.move_to_point(manipulator_zero_poss + Point(0, 0, SAFETY_MOVE_HEIGHT))

        while not find_zero_flag:
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
            move_vector = None
            frame_center = Point(frame.shape[1] / 2, frame.shape[0] / 2)
            if ids is not None:
                ids_dict = {}
                ids_middle = {}
                for i in range(ids.size):
                    ids_dict[int(ids[i][0])] = corners[i][0]
                    ids_middle[int(ids[i][0])] = find_middle(corners[i][0])

                for i in range(0, ids.size):
                    _id = ids[i][0]
                    if _id in zero_ids:
                        if _id == 0:
                            mid_zero = ids_middle[ids[i][0]]
                            ADAPTIVE_CONSTANT = Zero_marker0.size / \
                                                Vector(ids_dict[ids[i][0]][0], ids_dict[ids[i][0]][1]).length()
                            move_vector = Vector(mid_zero, frame_center)
                            gripper_suspension.set_zero()
                            find_zero_flag = True
                            break
        break

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# End of find


# Scan
detected_markers = [0, 1, 2]

for x_l in range(0, 900, 100):
    x_vector_move.set_length(x_l)
    for y_l in range(0, 500, 100):
        y_vector_move.set_length(y_l)
        move_vector = x_vector_move + y_vector_move
        manipulator.move_to_point(move_vector.end_point)

        for i in range(20):
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
            for i in range(0, ids.size):
                _id = ids[i][0]
                if _id in detected_markers:
                    marker_is_detect = False
                    while not marker_is_detect:
                        ret, frame = cap.read()
                        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
                        x_vector = None
                        y_vector = None
                        move_vector = None
                        frame_center = Point(frame.shape[1] / 2, frame.shape[0] / 2)
                        if ids is not None:
                            ids_dict = {}
                            ids_middle = {}

                            for i in range(ids.size):
                                ids_dict[int(ids[i][0])] = corners[i][0]
                                ids_middle[int(ids[i][0])] = find_middle(corners[i][0])

                            if _id in ids_dict.keys():
                                middle = ids_middle[_id]
                                move_vector = Vector(middle, frame_center)
                                if move_vector.length() > 2:
                                    move_vector.set_length(move_vector.length() * ADAPTIVE_CONSTANT)
                                    manipulator.move_by_vector(move_vector)
                                else:
                                    if

try:
    while True:
        markers_data = {}

        ret, frame = cap.read()

        # operations on the frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # detector parameters can be set here (List of detection parameters[3])

        # lists of ids and the corners belonging to each id
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

        if np.all(ids != None):
            for _id in range(0, ids.size):
                # draw axis for the aruco markers
                # aruco.drawAxis(frame, mtx, dist, rvec[i], tvec[i], 0.05)
                pass

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
finally:
    cap.release()
    cv2.destroyAllWindows()

# References
# 1. https://docs.opencv.org/3.4.0/d5/dae/tutorial_aruco_detection.html
# 2. https://docs.opencv.org/3.4.3/dc/dbb/tutorial_py_calibration.html
# 3. https://docs.opencv.org/3.1.0/d5/dae/tutorial_aruco_detection.html
