#!/usr/bin/env python3.6
# -*- coding: iso-8859-15 -*-

import pygame
from pygame.locals import *

from OpenGL.GL import *
#from OpenGL.GLUT import *
from OpenGL.GLU import *

import numpy as np


BLACK = (0.0, 0.0, 0.0)
WHITE = (1.0, 1.0, 1.0)
MAJOR_BLUE = (0.290198, 0.627456, 0.729418)
MINOR_BLUE = (0.078432, 0.203923, 0.207845)
MAJOR_GRAY = (0.388238, 0.388238, 0.388238)
MINOR_GRAY = (0.12157, 0.12157, 0.12157)
RED = (1.0, 0.0, 0.0)
LIGH_RED = (1.0, 0.454906, 0.39216)
LIGH_GREEN = (0.549024, 0.737261, 0.470592)
ORANGE = (0.843144, 0.572554, 0.305885)


def scale(sx=1.0, sy=1.0, sz=1.0):
    return np.array([[sx, 0, 0],
                     [0, sy, 0],
                     [0, 0, sz]])

def rotate(tx=0.0, ty=0.0, tz=0.0):
    cx = np.cos(tx)
    sx = np.sin(tx)
    cy = np.cos(ty)
    sy = np.sin(ty)
    cz = np.cos(tz)
    sz = np.sin(tz)

    Rx = np.array([[1,0,0],
                   [0,cx,-sx],
                   [0,sx,cx]])

    Ry = np.array([[cy,0,sy],
                   [0,1,0],
                   [-sy,0,cy]])

    Rz = np.array([[cz,-sz,0],
                   [sz,cz,0],
                   [0,0,1]])

    return Rx.dot(Ry).dot(Rz)


class Grid:
    def __init__(self, xs, ys, zs,
                 linecolor=WHITE, pointcolor=RED,
                 linewidth=1):
        # Define edge points for grid lines

        # x-axis
        self.xpoints = np.empty((1,3))
        yzpoints = np.mgrid[ys[0]:ys[1]+ys[2]:ys[2],
                            zs[0]:zs[1]+zs[2]:zs[2]].reshape(2,-1).T
        for yzpoint in yzpoints:
            y = yzpoint[0]
            z = yzpoint[1]
            xp0 = np.array([xs[0], y, z])
            xp1 = np.array([xs[1], y, z])
            self.xpoints = np.vstack((self.xpoints, xp0))
            self.xpoints = np.vstack((self.xpoints, xp1))
        self.xpoints = self.xpoints[1:]

        # y-axis
        self.ypoints = np.empty((1,3))
        xzpoints = np.mgrid[xs[0]:xs[1]+xs[2]:xs[2],
                            zs[0]:zs[1]+zs[2]:zs[2]].reshape(2,-1).T
        for xzpoint in xzpoints:
            x = xzpoint[0]
            z = xzpoint[1]
            yp0 = np.array([x, ys[0], z])
            yp1 = np.array([x, ys[1], z])
            self.ypoints = np.vstack((self.ypoints, yp0))
            self.ypoints = np.vstack((self.ypoints, yp1))
        self.ypoints = self.ypoints[1:]

        # z-axis
        self.zpoints = np.empty((1,3))
        xypoints = np.mgrid[xs[0]:xs[1]+xs[2]:xs[2],
                            ys[0]:ys[1]+ys[2]:ys[2]].reshape(2,-1).T
        for xypoint in xypoints:
            x = xypoint[0]
            y = xypoint[1]
            zp0 = np.array([x, y, zs[0]])
            zp1 = np.array([x, y, zs[1]])
            self.zpoints = np.vstack((self.zpoints, zp0))
            self.zpoints = np.vstack((self.zpoints, zp1))
        self.zpoints = self.zpoints[1:]

        # Color
        self.linecolor = linecolor
        self.pointcolor = pointcolor
        self.linewidth = linewidth

    def draw(self):
        r, g, b = self.linecolor
        #glLineWidth(self.linewidth)
        glColor3f(r, g, b)
        for xp0, xp1 in zip(self.xpoints[0::2], self.xpoints[1::2]):
            glVertex3fv(xp0)
            glVertex3fv(xp1)
        for yp0, yp1 in zip(self.ypoints[0::2], self.ypoints[1::2]):
            glVertex3fv(yp0)
            glVertex3fv(yp1)
        for zp0, zp1 in zip(self.zpoints[0::2], self.zpoints[1::2]):
            glVertex3fv(zp0)
            glVertex3fv(zp1)

    def transform(self, T):
        for axis in [self.xpoints, self.ypoints, self.zpoints]:
            for i, point in enumerate(axis):
                axis[i] = np.dot(T, point)


def main():
    pygame.init()
    width, height = 1000, 1000
    display = (width, height)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (width/height), 0, 150.0)
    glTranslatef(0, 0, -50)

    main_grid_major = Grid((-10, 10, 4), (-10, 10, 4), (-10, 10, 4),
                            linecolor=MAJOR_BLUE)

    T1 = rotate(0.01, 0.001, -0.01)
    T2 = np.random.uniform(-1, 1, (3,3)) * 1E-1
    T = T2 + np.identity(3)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    run = False
                if event.key == pygame.K_LEFT:
                    #glTranslatef(-1, 0, 0)
                    glRotatef(1, 0, 1, 0)
                if event.key == pygame.K_RIGHT:
                    #glTranslatef(1, 0, 0)
                    glRotatef(1, 0, -1, 0)
                if event.key == pygame.K_UP:
                    glTranslatef(0, 1, 0)
                if event.key == pygame.K_DOWN:
                    glTranslatef(0, -1, 0)
                if event.key == pygame.K_r:
                    main_grid_major = Grid((-10, 10, 4), (-10, 10, 4), (-10, 10, 4),
                                            linecolor=MAJOR_BLUE)
                    T1 = rotate(0.01, 0.001, -0.01)
                    T2 = np.random.uniform(-1, 1, (3,3)) * 1E-3
                    T = T2 + np.identity(3)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    glTranslatef(0, 0, 1.0)
                if event.button == 5:
                    glTranslatef(0, 0, -1.0)

        # Do stuff
        main_grid_major.transform(T)

        # Draw stuff
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glBegin(GL_LINES)
        main_grid_major.draw()
        glEnd()

        pygame.display.flip()
        pygame.time.wait(10)

    print('Exiting')
    pygame.quit()

if __name__ == '__main__':
    main()
    print('Goodbye!')
