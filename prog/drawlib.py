#!/usr/bin/env python3.6
# -*- coding: iso-8859-15 -*-

import numpy as np
import pygame
from pygame import gfxdraw
from pygame.locals import *
from copy import deepcopy


#-----------------#
# Color constants #
#-----------------#

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
MAJOR_BLUE = (74, 160, 186)
MINOR_BLUE = (0, 0, 0)
MAJOR_GRAY = (39, 39, 39)
MINOR_GRAY = (0, 0, 0)
RED = (255, 0, 0)
LIGHT_RED = (255, 116, 100)
LIGHT_GREEN = (140, 188, 120)
ORANGE = (215, 146, 78)
LIGHT_PURPLE = (178, 117, 190)


#------------------------#
# Mathematical constants #
#------------------------#

PI2 = np.pi*2.0
PI_2 = np.pi/2.0
S2 = np.sqrt(2)
S2_2 = S2/2.0
S3 = np.sqrt(3)
S3_2 = S3/2.0

#------------------#
# Helper Functions #
#------------------#

def vec_to_polygon(vec, width=1, shift=(0,0)):
    shift = np.array(shift)
    normal = normal_dir(vec) * width
    p1 = normal + shift
    p2 = -normal + shift
    p4 = vec + normal + shift
    p3 = vec - normal + shift
    return (p1, p2, p3, p4)

def draw_vector(surface, vec, width=1, center=(0,0), color=WHITE):
    rect = vec_to_polygon(vec, width, shift=center)
    gfxdraw.filled_polygon(surface, rect, color)

def get_eqtriangle(center, theta=0, r=1):
    """
    Returns the vertices of an equilateral triangle
    centered at center, with center-to-vertex length
    of r, rotated by angle theta + the correspoinding
    box sides.
    """
    p1 = np.array([-S3_2*r, -r*0.5])
    p2 = np.array([+S3_2*r, -r*0.5])
    p3 = np.array([0, r])

    R = rotate(theta)
    p1 = (np.dot(R, p1) + center).astype(int)
    p2 = (np.dot(R, p2) + center).astype(int)
    p3 = (np.dot(R, p3) + center).astype(int)

    return (p1, p2, p3)

def linear_interpolation(A1, A2, N):
    dT = (A2-A1)/N
    return [A1+dT*i for i in range(N+1)]


#---------------------#
# 2x2 transformations #
#---------------------#

def scale(sx=1, sy=1):
    return np.array([[sx, 0], [0, sy]])

def rotate(theta=0):
    c = np.cos(theta)
    s = np.sin(theta)
    return np.array([[c, -s], [s, c]])

def skew(kx=0, ky=0):
    return np.array([[1, kx], [ky, 1]])

I = scale()

def normalized(vec):
    L = np.linalg.norm(vec)
    if L != 0:
        return 1.0/L * vec
    else:
        return vec
        #raise ValueError('Can\'t normalize the zero vector!')

def normal_dir(vec):
    orthogonal_vec = np.array([vec[1], -vec[0]])
    return normalized(orthogonal_vec)

def scale_vec(vec, s):
    return s * normalized(vec)


#---------#
# Classes #
#---------#

class Vector:
    def __init__(self, coords, color=WHITE, width=2,
                 start=(0,0), center=(0,0),
                 arrow=True, head_size=15):
        self.coords = np.array(coords)
        self.color = color
        self.width = width
        self.arrow = arrow
        self.head_size = head_size
        self.start = np.array(start)
        self.center = np.array(center)

        self.calc_length()
        self.calc_angle()
        self.head_center = self.coords - scale_vec(self.coords, self.head_size)

    def calc_length(self):
        self.length = np.linalg.norm(self.coords)

    def calc_angle(self):
        self.angle = np.arctan(self.coords[0]/self.coords[1])

    def draw(self, surface):
        draw_vector(surface, self.coords*(1-self.head_size/self.length),
                    self.width, self.center, self.color)
        if self.arrow:
            triangle = get_eqtriangle(self.head_center+self.center,
                                      -self.angle, r=self.head_size)
            gfxdraw.filled_polygon(surface, triangle, self.color)

    def transform(self, T):
        self.coords = np.dot(T, self.coords)
        self.calc_length()
        self.calc_angle()
        self.head_center = self.coords - scale_vec(self.coords, self.head_size)


class Shape:
    def __init__(self, points=[], center=(0,0),
                 color=WHITE, width=1, alpha=255):
        self.points = np.array(points)
        self.center = np.array(center)
        self.color = color
        self.width = width
        self.alpha = alpha

    def draw(self, surface):
        vertices = [(point+self.center).astype(int) for point in self.points]
        gfxdraw.filled_polygon(surface, vertices, self.color)

    def transform(self, T):
        for i, point in enumerate(self.points):
            self.points[i] = np.dot(T, point)


class Grid:
    def __init__(self, xs, ys, center=(0,0),
                 linecolor=WHITE, pointcolor=RED,
                 linewidth=2, pointsize=2):

        # Create points that will be connected by grid lines
        # Left and right sides
        self.xpoints = []
        for y in np.arange(ys[0], ys[1]+ys[2], ys[2]):
            self.xpoints.append(np.array([xs[0], y]))
            self.xpoints.append(np.array([xs[1], y]))
        # Lower and upper sides
        self.ypoints = []
        for x in np.arange(xs[0], xs[1]+xs[2], xs[2]):
            self.ypoints.append(np.array([x, ys[0]]))
            self.ypoints.append(np.array([x, ys[1]]))

        # Center
        self.center = np.array(center)

        # Color
        self.linecolor = linecolor
        self.pointcolor = pointcolor

        # Widths
        self.linewidth = linewidth
        self.pointsize = pointsize

    def draw(self, surface):
        for xp1, xp2 in zip(self.xpoints[0::2], self.xpoints[1::2]):
            pygame.draw.line(surface,
                             self.linecolor,
                             (xp1+self.center).astype(int),
                             (xp2+self.center).astype(int)
                             )
        for yp1, yp2 in zip(self.ypoints[0::2], self.ypoints[1::2]):
            pygame.draw.line(surface,
                             self.linecolor,
                             (yp1+self.center).astype(int),
                             (yp2+self.center).astype(int)
                             )


    def transform(self, T):
        for i, xpoint in enumerate(self.xpoints):
            self.xpoints[i] = np.dot(T, xpoint)
        for j, ypoint in enumerate(self.ypoints):
            self.ypoints[j] = np.dot(T, ypoint)
