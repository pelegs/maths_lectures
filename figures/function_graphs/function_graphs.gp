f1(x) = x
f2(x) = x**2
f3(x) = x**3
f4(x) = cos(x)

load "../gnuplot-palettes/pastel1.pal"
LW = 10

set terminal cairolatex standalone pdf color colortext size 10cm, 10cm

set grid
set size square
set sample 1000
set border 0

set style arrow 1 lw 3 heads filled

# ------ f(x) = x ------ #

set xrange [-5:5]
set xtics axis
set arrow arrowstyle 1 from -5,0 to 5,0
set label "$x$" at graph 1.01, 0.5

set yrange [-5:5]
set ytics axis
set arrow arrowstyle 1 from 0,-5 to 0,5
set label "$y$" at graph 0.5, 1.03 center

set output "f1.tex"
plot f1(x) ls 1 lw LW notitle

# ------ f(x) = x^2 ------ #

unset arrow
unset label

set xrange [-5:5]
set xtics axis
set arrow arrowstyle 1 from -5,0 to 5,0
set label "$x$" at 5.1, 0

set yrange [-1:24]
set ytics axis
set arrow arrowstyle 1 from 0,-2.5 to 0,24
set label "$y$" at 0, 24.5 center

set output "f2.tex"
plot f2(x) ls 2 lw LW notitle

# ------ f(x) = x^3 ------ #

unset arrow
unset label

set xrange [-2.7:2.7]
set xtics axis
set arrow arrowstyle 1 from -2.7,0 to 2.7,0
set label "$x$" at 2.8, 0

set yrange [-25:25]
set ytics axis
set arrow arrowstyle 1 from 0,-25 to 0,25
set label "$y$" at 0, 26.5 center

set output "f3.tex"
plot f3(x) ls 3 lw LW notitle

# ------ f(x) = cos(x) ------ #

unset arrow
unset label

set xrange [-3*pi:3*pi]
set xtics axis ("$-3\\pi$" -3*pi, "$-2\\pi$" -2*pi, "$-\\pi$" -pi, "$\\pi$" pi, "$2\\pi$" 2*pi, "$3\\pi$" 3*pi)
set arrow arrowstyle 1 from -3*pi,0 to 3*pi,0
set label "$x$" at 3*pi+0.1, 0

set yrange [-2:2]
set ytics axis -2, 1, 2
set arrow arrowstyle 1 from 0,-2 to 0,2
set label "$y$" at 0, 2.5 center

set output "f4.tex"
plot f4(x) ls 4 lw LW notitle
