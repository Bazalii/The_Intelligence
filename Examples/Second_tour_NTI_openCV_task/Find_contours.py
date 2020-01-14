import cv2 as cv
import os
from Examples.Second_tour_NTI_openCV_task.FlatVector_class import *
from Examples.Second_tour_NTI_openCV_task.Point_class import *
from Examples.Second_tour_NTI_openCV_task.Geometry_functions import *
import numpy as np
import urllib.request


def url_to_image(url):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv.imdecode(image, cv.IMREAD_COLOR)

    # return the image
    return image


# fv - flat vector
# p - point
# c - coefficient
photos = os.listdir("Photo")

photo = photos[0]
src = cv.imread("Photo/" + photo)
_, threshold = cv.threshold(cv.cvtColor(src, cv.COLOR_BGR2GRAY), 200, 255, cv.THRESH_BINARY)
threshold = cv.GaussianBlur(threshold, (5, 5), 3)
# cv.imshow(f"Original", src)
# cv.imshow("Threshold", threshold)

contours, _ = cv.findContours(threshold, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
cv.drawContours(src, contours, -1, (0, 100, 0), 2)
prev_rect_flag = False
prev_rect = []
need_rect_cent = []
zero_p = (0, 0)
need_to_find_p = (0, 0)
zero_contour = []

for contour in contours:
    approx = cv.approxPolyDP(contour, 0.04 * cv.arcLength(contour, True), True)

    if cv.contourArea(approx) > 100:
        # cv.drawContours(src, [approx], 0, (0, 100, 0), 2)
        x = approx.ravel()[0]
        y = approx.ravel()[1]
        cent = find_center(approx)
        pix = src[cent[1]][cent[0]]
        r = pix[2]
        g = pix[1]
        b = pix[0]

        if len(approx) == 4:
            # low red 150 190 255
            # upper red 0 0 255

            # low black 0 0 0
            # upper black 120 120 120
            # if 0 <= b <= 150 and 0 <= g <= 190 and 240 <= r <= 255:
            # cv.putText(src, "Need_Rectangle", (x, y), cv.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 200, 0))
            if 0 <= b <= 170 and 0 <= g <= 170 and 0 <= r <= 170:
                if len(prev_rect) > 0 and cv.pointPolygonTest(prev_rect, cent, False) >= 0:
                    need_rect_cent.append(cent)
                    # print(cent)
                # cv.putText(src, "Need_Rectangle", (x, y), cv.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 200, 0))
                prev_rect = approx
            prev_rect_flag = True

        elif len(approx) >= 5:
            if 0 <= b <= 150 and 0 <= g <= 190 and 240 <= r <= 255 and prev_rect_flag:
                # cv.putText(src, "Need_circle", (x, y), cv.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 200, 0))
                need_to_find_p = cent
            if 0 <= b <= 170 and 0 <= g <= 170 and 0 <= r <= 170 and prev_rect_flag:
                # cv.putText(src, "Need_circle", (x, y), cv.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 200, 0))
                zero_p = cent
                zero_contour = prev_rect
            prev_rect_flag = False

# for p in need_rect_cent:
#     cv.putText(src, "&", p, cv.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 200))


# Find vector 0X and 0Y

# fv - flat vector
# p - point
# c - coefficient pix to mm
measurement_error = 15

# rect_fv = FlatVector(need_rect_cent[0], need_rect_cent[1])
check_fv = FlatVector(zero_p, need_rect_cent[0])
# cv.rectangle(src, form_start_rect_to_zero_fv.end_point.tuple_format(),
#              (form_start_rect_to_zero_fv.end_point + (10, 10)).tuple_format(), (50, 50, 50), 3)
# cv.rectangle(src, rect_fv.end_point.tuple_format(), (rect_fv.end_point + (10, 10)).tuple_format(), (100, 0, 100), 3)

check_len_1 = 0
check_len_2 = 0

# print(zero_contour)
for i in range(len(zero_contour) - 1):
    inter_point = line_intersection_point(FlatVector(zero_contour[i][0], zero_contour[i + 1][0]), check_fv)
    if type(inter_point) != bool:
        check_len_1 = distance_between_two_point(zero_contour[i][0], inter_point)
        check_len_2 = distance_between_two_point(zero_contour[i + 1][0], inter_point)
        break

if abs(check_len_1 - check_len_2) < measurement_error:
    ox_end_p = need_rect_cent[0]
    oy_end_p = need_rect_cent[1]
else:
    ox_end_p = need_rect_cent[1]
    oy_end_p = need_rect_cent[0]
# if dist2 - measurement_error < dist1 < dist2 + measurement_error:
#     ox_end_p = rect_fv.end_point
#     oy_end_p = rect_fv.start_point
# else:
#     ox_end_p = rect_fv.start_point
#     oy_end_p = rect_fv.end_point
ox_fv = FlatVector(zero_p, ox_end_p)
oy_fv = FlatVector(ox_end_p, oy_end_p)
oy_fv.move_to_point(zero_p)
check_fv = ox_fv + oy_fv

find_fv = FlatVector(zero_p, need_to_find_p)

ox_translate_to_real_c = 250 / ox_fv.length()
oy_translate_to_real_c = 250 / oy_fv.length()

a_c, b_c = find_collinear_coefficients(find_fv, ox_fv, oy_fv)

i_fv = ox_fv * (a_c, a_c)
j_fv = oy_fv * (b_c, b_c)

real_x = i_fv.length() * ox_translate_to_real_c
real_y = j_fv.length() * oy_translate_to_real_c

if a_c < 0:
    real_x *= -1
if b_c < 0:
    real_y *= -1

cv.line(src, ox_fv.start_point.tuple_format(), ox_fv.end_point.tuple_format(), (0, 0, 200), 3)
# cv.rectangle(src,ox_fv.end_point.tuple_format() , (ox_fv.end_point + (10, 10)).tuple_format(), (0, 100, 200), 3)
cv.line(src, oy_fv.start_point.tuple_format(), oy_fv.end_point.tuple_format(), (0, 0, 200), 3)
# cv.rectangle(src, oy_fv.end_point.tuple_format() , (oy_fv.end_point + (10, 10)).tuple_format(), (0, 100, 200), 3)
cv.line(src, find_fv.start_point.tuple_format(), find_fv.end_point.tuple_format(), (0, 200, 0), 3)

# cv.line(src, i_fv.end_point.to_int().tuple_format(), find_fv.end_point.tuple_format(), (0, 200, 0), 1)
# cv.line(src, j_fv.end_point.to_int().tuple_format(), find_fv.end_point.tuple_format(), (0, 200, 0), 1)

# cv.putText(src, "(0,0)", zero_p, cv.FONT_HERSHEY_COMPLEX_SMALL, 1, (200, 0, 0))
# cv.putText(src, f"({real_x},{real_y})", need_to_find_p, cv.FONT_HERSHEY_COMPLEX_SMALL, 1, (200, 0, 0))
# cv.putText(src, "(0,250)", ox_end_p.tuple_format(), cv.FONT_HERSHEY_COMPLEX_SMALL, 1, (200, 0, 0))
# cv.putText(src, "(250,250)", oy_end_p.tuple_format(), cv.FONT_HERSHEY_COMPLEX_SMALL, 1, (200, 0, 0))

print(f"({real_x},{real_y})")
# cv.imshow(f"Original(contours)", src)
cv.waitKey(0)
cv.destroyAllWindows()
