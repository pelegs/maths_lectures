#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

import sys
import numpy as np
import pygame
import re
import json


IGNORE = -1
FORWARD = 0
TURN = 1
PUSH = 2
POP = 3
LEAF = 4
NUM_KEYS = np.arange(48, 58, 1).astype(int)


def scale_vec(vec, scale):
    L = np.linalg.norm(vec)
    if L != 0:
        return vec/L * scale
    else:
        return vec*0.0

def rotate_vec(vec, angle):
    a = np.radians(angle)
    c = np.cos(a)
    s = np.sin(a)
    r = np.array([[c, -s],
                  [s, +c]])
    return np.dot(r, vec)

def heading2angle(heading):
    x = heading[0]
    y = heading[1]
    return np.degrees(np.arctan2(x, y))


class command:
    def __init__(self, string):
        self.type = None
        self.interpret(string)

    def interpret(self, string):
        if string == '(':
            self.type = PUSH
            return
        elif string == ')':
            self.type = POP
            return

        cmd = string[0]
        if cmd == 'T':
            self.type = TURN
        elif cmd == 'F':
            self.type = FORWARD
        elif cmd == 'L':
            self.type = LEAF
        elif cmd == 'X':
            self.type == IGNORE
            return
        else:
            raise ValueError('Command {} is unknown'.format(cmd))
            return

        v = re.findall('{(-?\d+\.?\d?)}', string)
        if v:
            self.val = float(v[0])


class turtle:
    def __init__(self,
                 pos=np.zeros(2),
                 angle=np.array([0, -1]),
                 rules=None,
                 convert=None,
                 axiom=None,
                 N=1,
                 color=[255]*3,
                 width=4):
        self.original_pos = pos
        self.original_angle = angle

        self.index = 0

        self.image = pygame.image.load('turtle.png')
        self.img_center = np.array([-25/2, -35/2])
        self.color = color
        self.width = width
        self.font_size = 40
        self.font = pygame.font.SysFont('Cabin', self.font_size)

        self.rules = rules
        self.axiom = axiom
        self.lsys_commands = None
        self.convert = convert
        self.commands = None
        self.N = N
        self.generate_commands(self.N)

        self.reset()

    def reset(self):
        self.set_status({'pos': self.original_pos,
                         'angle': self.original_angle})
        self.stack = [self.status]

    def get_num_cmds(self):
        return len(self.commands)

    def set_status(self, status):
        self.status = status

    def get_status(self):
        return self.status

    def generate_commands(self, runs=1):
        lst = self.axiom
        for i in range(runs):
            lst = ''.join([self.rules[x] for x in [*lst]])
        self.lsys_commands = lst
        self.lsys_draw = self.lsys_commands.replace('(', '( ').replace(')', ') ')
        cmds_text = ' '.join([self.convert[L] for L in self.lsys_commands]).split()
        self.commands = [command(cmd) for cmd in cmds_text]
        self.textsurfaces = [self.font.render(L, False, (255, 255, 255))
                                              for L in self.lsys_draw]

    def forward(self, surface, length=1, leaf=False):
        old_pos = self.status['pos']
        new_pos = old_pos + scale_vec(self.status['angle'], length)
        pygame.draw.line(surface, self.color, old_pos.astype(int), new_pos.astype(int), self.width)
        if leaf:
            pygame.draw.circle(surface, [0, 255, 0], new_pos.astype(int), 10)
        self.status['pos'] = new_pos

    def turn(self, angle=90):
        self.status['angle'] = rotate_vec(self.status['angle'], angle)

    def action(self, index, surface):
        cmd = self.commands[index]
        if cmd.type == IGNORE:
            pass
        if cmd.type == FORWARD:
            self.forward(surface, cmd.val)
        if cmd.type == LEAF:
            self.forward(surface, cmd.val, True)
        if cmd.type == TURN:
            self.turn(cmd.val)
        if cmd.type == PUSH:
            new_status = self.get_status().copy()
            self.stack.append(new_status)
        if cmd.type == POP:
            old_status = self.stack.pop().copy()
            self.set_status(old_status)

    def get_color(self, i):
        R = 255
        if i == self.index:
            G, B = 0, 0
        else:
            G, B = 255, 255
        return (R, G, B)

    def draw(self, surface, text=False):
        for i in range(self.index+1):
            self.action(i, surface)
        pos = self.status['pos']
        heading = heading2angle(self.status['angle'])
        self.active_image = pygame.transform.rotate(self.image, heading+180)
        surface.blit(self.active_image, pos+self.img_center)

        if text:
            self.textsurfaces = [self.font.render(L, False, self.get_color(i))
                                                  for i, L in enumerate(self.lsys_draw)]
            xpos, ypos = 10, 0
            xmax, ymax = surface.get_size()
            for letter in self.textsurfaces:
                surface.blit(letter, (xpos, ypos))
                xpos += self.font_size-5
                if xpos > xmax-10:
                    xpos = 0
                    ypos += self.font_size

    def change_index(self, change=0, mode='add'):
        if mode == 'add':
            self.index += change
        elif mode == 'min':
            self.index = 0
        elif mode == 'max':
            self.index = len(self.commands)-1
        else:
            raise ValueError('Mode {} is unknown'.format(mode))


# Read from config file
data_file = sys.argv[1]
with open(data_file, 'r') as f:
    configs = json.load(f)
rules = configs['rules']
convert = configs['convert']
axiom = configs['axiom']
pos0 = np.array(configs['pos0'])
N = configs['N']
text = False

if __name__ == '__main__':
    s = 800
    pygame.display.init()
    pygame.font.init()
    screen = pygame.display.set_mode((s, s))
    pygame.display.flip()

    t = turtle(pos=pos0,
               rules=rules,
               convert=convert,
               axiom=axiom,
               N=N)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_LEFT and t.index > 0:
                    t.change_index(-1)
                if event.key == pygame.K_RIGHT and t.index < t.get_num_cmds()-1:
                    t.change_index(+1)
                if event.key == pygame.K_DOWN:
                    t.change_index(mode='min')
                if event.key == pygame.K_UP:
                    t.change_index(mode='max')
                if event.key in NUM_KEYS:
                    t.N = event.key-48
                    t.generate_commands(t.N)
                    t.change_index(mode='min')
                    print('N =', t.N)
                if event.key == pygame.K_t:
                    text = not text

        screen.fill(3*[0])
        t.reset()
        t.draw(screen, text)
        pygame.display.update()
