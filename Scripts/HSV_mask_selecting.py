import cv2 as cv
import numpy as np


def nothing(*arg):
    pass


if __name__ == '__main__':
    try:
        cv.namedWindow("Set HSV mask")  # создаем окно настроек
        photo = input("Please input path to the photo:\n")
        img = cv.imread(photo)
        # создаем 6 бегунков для настройки начального и конечного цвета фильтра
        cv.createTrackbar('h1', 'Set HSV mask', 0, 255, nothing)
        cv.createTrackbar('s1', 'Set HSV mask', 0, 255, nothing)
        cv.createTrackbar('v1', 'Set HSV mask', 0, 255, nothing)
        cv.createTrackbar('h2', 'Set HSV mask', 255, 255, nothing)
        cv.createTrackbar('s2', 'Set HSV mask', 255, 255, nothing)
        cv.createTrackbar('v2', 'Set HSV mask', 255, 255, nothing)
        crange = [0, 0, 0, 0, 0, 0]

        while True:
            img = cv.imread(photo)
            hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

            # считываем значения бегунков
            h1 = cv.getTrackbarPos('h1', 'Set HSV mask')
            s1 = cv.getTrackbarPos('s1', 'Set HSV mask')
            v1 = cv.getTrackbarPos('v1', 'Set HSV mask')
            h2 = cv.getTrackbarPos('h2', 'Set HSV mask')
            s2 = cv.getTrackbarPos('s2', 'Set HSV mask')
            v2 = cv.getTrackbarPos('v2', 'Set HSV mask')

            # формируем начальный и конечный цвет фильтра
            h_min = np.array((h1, s1, v1), np.uint8)
            h_max = np.array((h2, s2, v2), np.uint8)

            # накладываем фильтр на кадр в модели HSV
            thresh = cv.inRange(hsv, h_min, h_max)

            cv.imshow('Set HSV mask', thresh)

            k = cv.waitKey(27)
            if k != -1:
                exit(0)

    finally:
        cv.destroyAllWindows()
