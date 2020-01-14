from Point_class import Point
from FlatVector_class import FlatVector


def find_center(cont):
    point_sum = [0, 0]
    for point in cont:
        point_sum[0] += point[0][0]
        point_sum[1] += point[0][1]
    return tuple([int(point_sum[0] / len(cont)), int(point_sum[1] / len(cont))])


def line_intersection_point(vector1: FlatVector, vector2: FlatVector):
    # составляем формулы двух прямых
    x1_1 = vector1.start_point.x
    y1_1 = vector1.start_point.y
    x1_2 = vector1.end_point.x
    y1_2 = vector1.end_point.y
    x2_1 = vector2.start_point.x
    y2_1 = vector2.start_point.y
    x2_2 = vector2.end_point.x
    y2_2 = vector2.end_point.y
    A1 = y1_1 - y1_2
    B1 = x1_2 - x1_1
    C1 = x1_1 * y1_2 - x1_2 * y1_1
    A2 = y2_1 - y2_2
    B2 = x2_2 - x2_1
    C2 = x2_1 * y2_2 - x2_2 * y2_1
    # решаем систему двух уравнений
    if B1 * A2 - B2 * A1 != 0:
        y = (C2 * A1 - C1 * A2) / (B1 * A2 - B2 * A1)
        if B1 * A2 - B2 * A1 == 0:
            return False
        if A1 == 0:
            x = 0
        else:
            x = (-C1 - B1 * y) / A1
        # проверяем, находится ли решение системы (точка пересечения) на первом отрезке, min/max - потому
        # что координаты точки могут быть заданы не по порядку возрастания
        if min(x1_1, x1_2) <= x <= max(x1_1, x1_2) and min(y1_1, y1_2) <= y <= max(y1_1, y1_2):
            return Point(x, y)
        else:
            return False
    # случай деления на ноль, то есть параллельность
