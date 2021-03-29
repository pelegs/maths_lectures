import struct
import numpy as np


def vlen(vec):
    t = r'\sqrt{'
    for x in vec:
        if x==0:
            t += '\\cancel{{ {}^{{2}}}}+'.format(x)
        else:
            t += '{}^{{2}}+'.format(x)
    t = t[:-1]
    norm2 = np.sum([x**2 for x in vec])
    norm = np.linalg.norm(vec)
    t += '}}=\\sqrt{{ {0}}}\\approx {1:.5f}'.format(norm2, norm)
    return t


def convert(num, base):
    print('${}_{{10}} \\rightarrow \\text{{base-}}{{{}}}$\\hspace{{1cm}}'.format(num, base))
    print('\\begin{tabular}{ l l l }')
    print('Result & Quotient & Remainder~\\\\')
    print('\\hline')

    b = n = num
    base_num = ''
    while n > 0:
        b = n % base
        d = n // base
        base_num += str(b)
        print('{} & {} & {}\\\\'.format(n, d, b))
        n = n // base

    print('\\hline')
    print('\\end{tabular}')
    print('\\hspace{{1cm}}Answer: ${}_{{10}}={}_{{{}}}$'.format(num, base_num[::-1], base))
    print('')


def binary(num):
    return ''.join(bin(c)[2:].rjust(8, '0') for c in struct.pack('!f', num))


def show_fp(num, scale=1.0):
    f_num = binary(num)
    print('\\begin{{tikzpicture}}[scale={}]'.format(scale))
    print('\\draw[fill=red!20](0,0) rectangle (0.5,1);')
    print('\\draw[fill=blue!20](0.5,0) rectangle (4.5,1);')
    print('\\draw[fill=green!20](4.5,0) rectangle (16,1);')
    print('\\draw[thick] (0,0) rectangle (16,1);')
    for i, digit in enumerate(f_num):
        print('\\node[] () at ({},0.5) {{{}}};'.format(i*0.5+0.25, digit))
        print('\\draw[thick,-] ({},{}) to ({},{});'.format(i*0.5, 0, i*0.5, 1))
    print('\\end{tikzpicture}')


def twos(num, bits):
    num2 = format(num, '#010b')[2:]
    flip = ''.join([str(int(d)^1) for d in num2])
    add1 = int(flip, 2) + 1
    print('${} \\xrightarrow[\\text{{8 bit}}]{{\\text{{binary}}}} {} \\xrightarrow[\\text{{}}]{{\\text{{invert}}}} {} \\xrightarrow[\\text{{}}]{{\\text{{add 1}}}} {}={}_{{{}}}$'.format(num, num2, flip, bin(add1)[2:], -1*num, 10))

def draw(m):
    print('\\begin{pmatrix}')
    M = np.array(m)
    for row in M:
        print('&'.join(map(str, row)), '\\\\')
    print('\\end{pmatrix}.')

def draw_add(A, B):
    try:
        draw_matrix(A+B)
    except:
        print('\\textbf{undefined}')

def draw_prod(A, B):
    try:
        draw_matrix(np.dot(A,B))
    except:
        print('\\textbf{undefined}')

def draw_det(A):
    try:
        print(int(np.linalg.det(A)))
    except:
        print('\\textbf{undefined}')

def vdot(i, j, u, v, alone=False):
    if alone:
        print(r'\begin{align*}')
        print(r'\bm{C}&=')
    else:
        print('c_{{{}{}}}&='.format(i+1, j+1))
    line = ''
    for a, b in zip(u, v):
        line += '\\left({}\\cdot{}\\right)+'.format(a, b)
    print(line[:-1])
    prod = np.dot(u, v)
    if alone:
        print(r'={}\\'.format(prod))
    else:
        print(r'={}\\'.format(prod))
    if alone:
        print(r'\end{align*}')

def mdot(A, B):
    print(r'\begin{minipage}{0.4\textwidth}')
    print(r'\begin{align*}')
    for i, a in enumerate(A):
        for j, b in enumerate(np.transpose(B)):
            vdot(i, j, a, b)
    print(r'\end{align*}')
    print(r'\end{minipage}')
    print(r'\begin{minipage}{0.1\textwidth}')
    print(r'$\Longrightarrow$')
    print(r'\end{minipage}')
    print(r'\begin{minipage}{0.5\textwidth}$\bm{C}=')
    draw(np.dot(A,B))
    print(r'$\end{minipage}')

def colordot(A, B, a, b, col1, col2):
	A_cols = A.shape[1]
	B_cols = B.shape[1]
	Acs = 'c'*A_cols
	Bcs0 = 'c'*B_cols
	Bcs = Bcs0[:b] + '>{{\columncolor{{{}!25}}}}'.format(col2) + Bcs0[b:]
	print('\\scriptsize$\\begin{{array}}{{l}}\colorbox{{{}!25}}{{\\text{{row}}={}}}\\\\ \\colorbox{{{}!25}}{{\\text{{col}}={}}}\\end{{array}}$'.format(col1, a+1, col2, b+1))
	print('& \\scriptsize$\\left(\\begin{{array}}{{{}}}'.format(Acs))
	for i, row in enumerate(A):
		if i==a:
			print('\\rowcolor{{{}!25}}'.format(col1))
		else:
			print(r'\rowcolor{light-gray}')
		elements = '&'.join(map(str, row))
		print(elements, r'\\')
	print(r'\end{array}\right)$')
	print('& \\scriptsize $\\left(\\begin{{array}}{{{}}}'.format(Bcs))
	for i, row in enumerate(B):
		elements = '&'.join(map(str, row))
		print(elements, r'\\')
	print(r'\end{array}\right)$')
	print('& \\scriptsize $\\Rightarrow c_{{\\colorbox{{{}!25}}{{{}}}\\colorbox{{{}!25}}{{{}}}}}=$'.format(col1, a+1, col2, b+1))
	sum = ''
	for i,z in enumerate(A[a]):
		sum += '\\scriptsize $\\left[\\colorbox{{{}!25}}{{{}}}\\times\\colorbox{{{}!25}}{{{}}}\\right] +$'.format(col1, A[a][i], col2, B[:,b][i])
	print(sum[:-2], '$')
	print('& \\scriptsize = \\scriptsize {}& \\\\'.format(np.dot(A[a], B[:,b])))

def draw_matrix(m):
	print(r'\begin{pmatrix}')
	for row in m:
		elements = '&'.join(map(str, row))
		print(elements, r'\\')
	print(r'\end{pmatrix}')

def vspace(size=1):
    print('\\vspace{{{}cm}}'.format(size))

def Lsys(axiom, rules, runs=1):
    lst = axiom
    for i in range(runs):
        lst = ''.join([rules[x] for x in [*lst]])
    return lst

def print_Lsys(lst):
    for i, l in enumerate(lst):
        print('$n={}$: {} \\\\'.format(i, l))

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

class turtle:
    def __init__(self, pos=np.zeros(2), angle=np.array([0, 1]),
                       LEAF=1.5, LINE=1.0,
                       LEFT=-45,RIGHT=45):
        self.original_pos = pos
        self.original_angle = angle
        self.LEAF = LEAF
        self.LINE = LINE
        self.LEFT = LEFT
        self.RIGHT = RIGHT
        self.reset()

    def reset(self):
        self.set_status({'pos': self.original_pos,
                         'angle': self.original_angle})
        self.stack = [self.status]

    def set_status(self, status):
        self.status = status

    def get_status(self):
        return self.status

    def create(self, type, style='thick', color='black'):
        if type == 'line':
            length = self.LINE
        elif type == 'leaf':
            length = self.LEAF
        old_pos = self.status['pos']
        new_pos = old_pos + scale_vec(self.status['angle'], length)
        print('\\draw[{}, {}] ({},{}) to ({},{});'.format(style, color,
                                                          old_pos[0], old_pos[1],
                                                          new_pos[0], new_pos[1]))
        if type == 'leaf':
            print('\\draw[fill=green] ({},{}) circle (0.5);'.format(new_pos[0], new_pos[1]))
        self.status['pos'] = new_pos

    def turn(self, angle):
        self.status['angle'] = rotate_vec(self.status['angle'], angle)

    def draw(self, string):
        for cmd in string:
            if cmd == 'A':
                self.create('line')
            if cmd == 'B':
                self.create('leaf')
            if cmd == '(':
                new_status = self.get_status().copy()
                self.stack.append(new_status)
                self.turn(self.LEFT)
            if cmd == ')':
                old_status = self.stack.pop().copy()
                self.set_status(old_status)
                self.turn(self.RIGHT)

    def draw2(self, string):
        for cmd in string:
            if cmd == 'R':
                self.turn(self.LEFT)
            if cmd == 'F':
                self.create('line')
            if cmd == '(':
                new_status = self.get_status().copy()
                self.stack.append(new_status)
            if cmd == ')':
                old_status = self.stack.pop().copy()
                self.set_status(old_status)


def turtle_draw(start=[0,0], lst='A'):
    t = turtle(np.array(start))
    t.draw(lst)

def turtle_draw2(start=[0,0], lst='x'):
    t = turtle(np.array(start))
    t.draw2(lst)

if __name__ == '__main__':
    rules = {'A': 'AB',
             'B': 'A'}
    Ls = [(Lsys('A', rules, i)) for i in range(8)]
    test = ['A', 'AB','ABA','ABAAB','ABAABABA','ABAABABAABAAB','ABAABABAABAABABAABABA','ABAABABAABAABABAABABAABAABABAABAAB']
    check = [l==t for l,t in zip(Ls, test)]
    print(check)
    print('')
    turtle_draw('AAAA(AA(A(B)B)A(B)B)AA(A(B)B)A(B)B')
