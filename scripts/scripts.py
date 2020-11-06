#!/usr/bin/env python3.6
# -*- coding: iso-8859-15 -*-

from sys import argv

def identity_matrix(n):
    print('\\begin{pmatrix}')
    for i in range(n):
        row = [0] * n
        row[i] = 1
        print('&'.join(map(str, row)), '\\\\')
    print('\\end{pmatrix}')


if __name__ == '__main__':
    identity_matrix(int(argv[1]))
