import math
from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def get_left_point(points: List[Point]) -> Point:
    min_by_x = 0
    for i in range(1, len(points)):
        if points[i].x < points[min_by_x].x:
            min_by_x = i
        elif points[i].x == points[min_by_x].x:
            if points[i].y > points[min_by_x].y:
                min_by_x = i
    return points[min_by_x]


def is_counterclockwise(p: Point, q: Point, r: Point) -> bool:
    val = (q.y - p.y) * (r.x - q.x) - \
          (q.x - p.x) * (r.y - q.y)

    return val < 0


def jarvis_hull(points: List[Point]) -> List[Point]:
    result = []
    length = len(points)

    first_hull_point = get_left_point(points)
    result.append(first_hull_point)

    while True:
        last_hull_point = result[-1]
        potential_hull_point = points[(points.index(last_hull_point) + 1) % length]

        for point in points:
            if is_counterclockwise(last_hull_point, point, potential_hull_point):
                potential_hull_point = point

        if potential_hull_point == first_hull_point:
            break

        result.append(potential_hull_point)

    return result


def find_farthest_points(points: List[Point]) -> Tuple[Point, Point]:
    max_distance = 0
    p1, p2 = points[0], points[1]
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            distance = math.sqrt(math.pow(points[i].x - points[j].x, 2) + math.pow(points[i].y - points[j].y, 2))
            if distance > max_distance:
                max_distance = distance
                p1, p2 = points[i], points[j]
    return p1, p2


def draw_result(points: List[Point], hull: List[Point], farthest_points: Tuple[Point, Point]):
    plt.figure()
    plt.title(f'Points count = {len(points):,}, Hull count = {len(hull)}')

    plt.plot(list(map(lambda p: p.x, points)), list(map(lambda p: p.y, points)), 'o')

    hull.append(hull[0])
    plt.plot(list(map(lambda p: p.x, hull)), list(map(lambda p: p.y, hull)), '-')
    plt.plot(list(map(lambda p: p.x, hull)), list(map(lambda p: p.y, hull)), 'o')

    [p1, p2] = farthest_points
    plt.plot([p1.x, p2.x], [p1.y, p2.y], '-')

    plt.show()


if __name__ == '__main__':
    points_count = 1_000

    generated_points = list(map(lambda x: Point(x[0], x[1]), np.random.rand(points_count, 2)))
    generated_hull = jarvis_hull(generated_points)
    generated_farthest_points = find_farthest_points(generated_hull)

    draw_result(generated_points, generated_hull, generated_farthest_points)
