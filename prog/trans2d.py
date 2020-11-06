#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

from copy import deepcopy
from drawlib import *

#-----------------#
# Other constants #
#-----------------#

NUM_FRAMES = 60

#------------------#
# Helper Functions #
#------------------#

def init():
    pygame.init()

    global width, height
    width, height = 1000, 1000

    global screen
    screen = pygame.display.set_mode((width, height))

    global screen_center
    screen_center = (width//2, height//2)

def finish():
    print('Exiting')
    pygame.quit()


def loop(static_surface, trans_grid, axes,
         vectors=[], shapes=[], labels=[]):
    run = True
    frame = 0
    TRANSFORMING = False

    trans_surface = create_trans_surface(trans_grid, axes,
                                         vectors, shapes, labels)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == KEYDOWN:
                if event.key == pygame.K_q:
                    run = False
                if event.key == pygame.K_t and not TRANSFORMING:
                    TRANSFORMING = True
                    frame = 0
                    trans_grid2 = deepcopy(trans_grid)
                    axes2 = deepcopy(axes)
                    vectors2 = deepcopy(vectors)
                    shapes2 = deepcopy(shapes)
                    labels2 = deepcopy(labels)
                    dT = dT1
                if event.key == pygame.K_r and not TRANSFORMING:
                    TRANSFORMING = True
                    frame = 0
                    trans_grid2 = deepcopy(trans_grid)
                    axes2 = deepcopy(axes)
                    vectors2 = deepcopy(vectors)
                    shapes2 = deepcopy(shapes)
                    labels2 = deepcopy(labels)
                    dT = dT2


        if TRANSFORMING:
            if np.linalg.det(dT[frame]) != 0.0:
                # Copy back from original
                trans_grid = deepcopy(trans_grid2)
                axes = deepcopy(axes2)
                vectors = deepcopy(vectors2)
                shapes = deepcopy(shapes2)
                labels = deepcopy(labels2)

                # Perform transformations
                trans_grid, axes, vectors, shapes, labels = transform_objects(trans_grid, axes,
                                                                              vectors, shapes, labels,
                                                                              dT[frame])
                # Create transformed surface
                trans_surface = create_trans_surface(trans_grid, axes,
                                                     vectors, shapes, labels)

            # Adavance frames
            frame += 1
            if frame == NUM_FRAMES+1:
                TRANSFORMING = False

        # Show stuff
        screen.fill(BLACK)
        screen.blit(static_surface, (0,0))
        screen.blit(trans_surface, (0,0))
        pygame.display.update()

def transform_objects(grid, axes,
                      vectors=[], shapes=[], labels=[],
                      transformation=I):

    # Transform objects
    grid.transform(transformation)
    for axis in axes:
        axis.transform(transformation)
    for vector in vectors:
        vector.transform(transformation)
    for shape in shapes:
        shape.transform(transformation)
    return grid, axes, vectors, shapes, labels


def create_trans_surface(trans_grid, axes,
                         vectors=[], shapes=[], labels=[]):
    # Create transforming surface
    trans_surface = screen.copy()
    trans_surface.fill(BLACK)
    trans_surface.set_colorkey(BLACK)

    # Draw objects to surface
    trans_grid.draw(trans_surface)
    for axis in axes:
        axis.draw(trans_surface)
    for vector in vectors:
        vector.draw(trans_surface)
    for shape in shapes:
        shape.draw(trans_surface)

    # Vertically flip transf_surface because
    # PyGame uses top-left corner as origin
    trans_surface = pygame.transform.flip(trans_surface, False, True)

    return trans_surface


#------#
# Main #
#------#

if __name__ == '__main__':
    init()

    # Transformations
    global T1, T2, dT1, dT2
    T1 = rotate(np.pi/3).dot(skew(kx=0.4, ky=-0.1))
    T1 = np.random.uniform(-1.5, 1.5, (2,2))
    T2 = np.linalg.inv(T1)
    dT1 = linear_interpolation(I, T1, NUM_FRAMES)
    dT2 = linear_interpolation(I, T2, NUM_FRAMES)
    eigvals, eigvecs = np.linalg.eig(T1)
    print(eigvals, eigvecs)

    # Setup static (non-transforming) grid
    static_screen = screen.copy()
    static_grid = Grid((-800,800,100), (-800, 800, 100), screen_center,
                       linecolor=MAJOR_GRAY, pointcolor=WHITE,
                       linewidth=1)
    static_grid.draw(static_screen)

    # Setup transforming grid
    trans_grid = Grid((-800,800,100), (-800, 800, 100), screen_center,
                      linecolor=MAJOR_BLUE, pointcolor=WHITE,
                      linewidth=2)

    # Setup transforming axes
    xaxis_right = Vector((800, 0), center=screen_center, arrow=False)
    xaxis_left = Vector((-800, 0), center=screen_center, arrow=False)
    yaxis_top = Vector((0, 800), center=screen_center, arrow=False)
    yaxis_bottom = Vector((0, -800), center=screen_center, arrow=False)
    axes = [xaxis_right, xaxis_left, yaxis_top, yaxis_bottom]

    # Base vectors
    ex = Vector((100, 0), color=LIGHT_RED, center=screen_center, width=3)
    ey = Vector((0, 100), color=LIGHT_GREEN, center=screen_center, width=3)

    # Other vectors
    v = Vector((200,300), color=ORANGE, center=screen_center, width=3)

    all_vecs = []
    for val, vec in zip(eigvals, eigvecs.T):
        if np.all(np.isreal([val].extend(vec))):
            all_vecs.append(Vector(300*vec, color=LIGHT_PURPLE, center=screen_center, width=3))
    all_vecs.extend([ex, ey, v])

    # Shapes
    shape = Shape([(200, 200), (200,300), (300,300), (300, 200)],
                  center=screen_center,
                  color=WHITE, alpha=200)

    # Hat labels
#    ihat_label = pygame.transform.flip(Label('$\\hat{i}$', color='ff7464', size=25).get_image(),
#                                       False, True)
#    jhat_label = pygame.transform.flip(Label('$\\hat{j}$', color='8cbc78', size=25).get_image(),
#                                       False, True)
#    ihat_coords = (ex.coords*(1.1)+np.array(screen_center)).astype(int)
#    jhat_coords = (ey.coords*(1.2)+np.array(screen_center)).astype(int)

    # Main stuff
    loop(static_screen, trans_grid, axes,
         all_vecs, [shape])
    finish()
    print('Goodbye!')
