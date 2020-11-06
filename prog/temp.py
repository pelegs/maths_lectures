#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

import numpy as np


N = 10
A = np.array([[0.86,0.08],[-0.12,1.14]])
v1 = np.zeros((N,2))
v1[0] = np.array([3.5,1])
v1[:N] = np.array([np.dot(np.linalg.matrix_power(A,i), v1[0]) for i in range(N)])
v2 = np.zeros((N,2))
v2[0] = np.array([1,3.7])
v2[:N] = np.array([np.dot(np.linalg.matrix_power(A,i), v2[0]) for i in range(N)])
print(v1)
print(v2)
