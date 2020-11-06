#!/usr/bin/env python3.6
# -*- coding: iso-8859-15 -*-

import numpy as np


A = np.array([[0.86, 0.08],
              [-0.12, 1.14]])

start_points = np.array([[10, 50],
                         [100, 200],
                         [50, 100],
                         [70, 120]])

start_points = np.random.randint(0, 300, (300, 2))

max_points = 100
xmin, xmax = -300, 300
ymin, ymax = -300, 300

for i, start_point in enumerate(start_points):
    current_point = start_point
    next_point = current_point
    for _ in range(max_points):
        current_point = next_point
        next_point = np.dot(A, current_point)
        if (xmin <= next_point[0] <= xmax) and (ymin <= next_point[1] <= ymax):
            print(' '.join(map(str, next_point)), i)
        else:
            break
