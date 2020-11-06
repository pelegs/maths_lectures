#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

import numpy as np

def rotate(theta):
	c = np.cos(theta)
	s = np.sin(theta)
	return np.array([[c,-s],[s,c]])

def rotate_deg(theta):
	return rotate(np.radians(theta))

def print_mat(m):
	for row in m:
		print('&'.join(map(str, row)), '\\\\')

if __name__ == '__main__':
	print('hi and bye!')
