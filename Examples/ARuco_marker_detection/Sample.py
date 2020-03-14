from typing import Iterable

import cv2
import cv2.aruco as aruco

from Moving_systems.Data_base import *
from OpenCV_scripts.Camera_calibration import Camera_calibration
from Moving_systems.Manipulator_shell import Manipulator
from Classes.Point_class import Point
from Classes.Vector_class import Vector

cap = cv2.VideoCapture(1)

ret, mtx, dist, rvecs, tvecs = Camera_calibration()

# set dictionary size depending on the aruco marker selected
aruco_dict = aruco.Dictionary_get(aruco.DICT_ARUCO_ORIGINAL)
parameters = aruco.DetectorParameters_create()
parameters.adaptiveThreshConstant = 10

ADAPTIVE_CONSTANT = None

manipulator = Manipulator("", "sa", "")
find_zero_flag = False

mid_zero = None
cv2.namedWindow("frame")
cv2.namedWindow("check")

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

                    # cv2.line(frame, (int(mid_zero[0]), int(mid_zero[1])),
                    #          (int(frame_center.x), int(frame_center.y)), (0, 200, 0), 3)
                    cv2.putText(frame, "(0, 0)", (int(mid_zero[0]),
                                                  int(mid_zero[1])), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (200, 0, 0))

                    # print(f"Zero: {mid_zero}")
                    if x_vector is not None:
                        cv2.line(frame, (int(mid_zero[0]), int(mid_zero[1])),
                                 (int(x_vector.end_point.x), int(x_vector.end_point.y)), (0, 0, 200), 3)
                        # print(f"X: {x_vector.end_point}")
                    if y_vector is not None:
                        cv2.line(frame, (int(mid_zero[0]), int(mid_zero[1])),
                                 (int(y_vector.end_point.x), int(y_vector.end_point.y)), (0, 200, 0), 3)
                        # print(f"Y: {y_vector.end_point}")

        if y_vector is not None and x_vector is not None:
            for i in range(0, ids.size):
                strg += str(ids[i][0]) + ', '
                _id = ids[i][0]
                if _id not in zero_ids:
                    mid_val = ids_middle[ids[i][0]]
                    vect = Vector(mid_zero, mid_val)
                    vect_val = vect.copy()
                    vect_val.move_to_point((0, 0))
                    vect_val.set_length(vect.length()*ADAPTIVE_CONSTANT)
                    cv2.line(frame, (int(mid_zero[0]), int(mid_zero[1])),
                             (int(vect.end_point.x), int(vect.end_point.y)), (0, 0, 0), 3)
                    cv2.putText(frame, f"pos:{int(vect_val.end_point.x), -int(vect_val.end_point.y)}", (int(vect.end_point.x),
                                              int(vect.end_point.y)), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 0))
                    print(f"pos:{int(vect_val.end_point.x), -int(vect_val.end_point.y)}")
                    vect.set_length(vect.length()/2)
                    # cv2.putText(frame, f"len:{vect_val.length()}", (int(vect.end_point.x),
                    #                           int(vect.end_point.y)), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 0))
                    cv2.imshow("check", frame)
    cv2.imshow('frame', frame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break