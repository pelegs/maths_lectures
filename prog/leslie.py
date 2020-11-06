#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

from drawlib import *

#-----------#
# Functions #
#-----------#

def draw_axes(w, h, center=np.zeros(2), bgcolor=WHITE, axescolor=BLACK):
    surface = pygame.Surface((w, h))
    surface.fill(bgcolor)

    x_axis_minus = Vector((-w/2,0), color=axescolor, center=center, width=1)
    x_axis_plus = Vector((w/2,0), color=axescolor, center=center, width=1)
    y_axis_minus = Vector((0,-h/2), color=axescolor, center=center, width=1)
    y_axis_plus = Vector((0,h/2), color=axescolor, center=center, width=1)

    x_axis_minus.draw(surface)
    x_axis_plus.draw(surface)
    y_axis_minus.draw(surface)
    y_axis_plus.draw(surface)

    return surface

def create_points(pos, matrix=I, N_max=100,
                  ext=(-300, 300, -300, 300)):
    xmin, xmax, ymin, ymax = ext
    points = np.copy(pos)
    points = np.vstack((points, points))
    for i in range(N_max):
        new_point = np.dot(matrix, points[-1])
        if (xmin <= new_point[0] <= xmax) and (ymin <= new_point[1] <= ymax):
            points = np.vstack((points, new_point))
        else:
            break
    return points[1:]

def draw_points(surface, points, center=np.zeros(2),
                radius=2, color=BLACK):
    for point in points:
        point[1] = -point[1]
        gfxdraw.aacircle(surface,
                         int(point[0]+center[0]),
                         int(point[1]+center[1]),
                         radius, color)
        gfxdraw.filled_circle(surface,
                              int(point[0]+center[0]),
                              int(point[1]+center[1]),
                              radius, color)


#------#
# Main #
#------#

if __name__ == '__main__':
    pygame.init()

    width, height = 1000, 1000
    screen = pygame.display.set_mode((width, height))
    screen_center = np.array([width//2, height//2])

    axes = draw_axes(width, height, screen_center)

    points_surface = pygame.Surface((width, height))
    points_surface.fill(BLACK)
    points_surface.set_colorkey(BLACK)

    A = np.array([[0.86, 0.08],
                  [-0.12, 1.14]])

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                trans_pos = np.array(pos)
                trans_pos[1] = height - trans_pos[1]
                trans_pos -= screen_center
                points = create_points(trans_pos, A, ext=(-width/2, width/2,
                                                          -height/2, height/2))
                draw_points(points_surface, points,
                            center=screen_center,
                            color=np.random.randint(0, 200, 3))

        # Draw stuff
        screen.blit(axes, (0,0))
        screen.blit(points_surface, (0,0))
        pygame.display.update()

    # Finish
    pygame.quit()
    print('Goodbye!')
