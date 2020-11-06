f1(x) = x**2
f2(x) = x**3
f3(x) = sin(x)
f4(x) = log(x)
f5(x) = abs(x)
f6(x) = sqrt(x)

set xlabel "$x$"
set ylabel "$y$"
set grid
set sample 1000

set style line 1 lw 11
set style line 2 dt "-" lw 4 lc "#444444"

XAXIS = "set xtics; set xlabel '\\Huge$x$'"
YAXIS = "set ytics; set ylabel '\\Huge$y$' rotate by 0"
NOXAXIS = "unset xlabel"
NOYAXIS = "unset ylabel"

set terminal cairolatex standalone pdf color colortext size 30cm, 20cm
set output "func_graphs.tex"

set multiplot layout 2,3
set size square

unset arrow
@YAXIS; @NOXAXIS
set xrange [-5:5]
set yrange [-3:10]
set arrow from -5,0 to 5,0 nohead ls 2
set arrow from 0,-3 to 0,10 nohead ls 2
unset label; set label "\\Huge $x^{2}$" at graph 0.05,0.9
plot f1(x) notitle ls 1 lc "#FF0000"

unset arrow
@NOXAXIS; @NOYAXIS
unset label; set label "\\Huge $x^{3}$" at graph 0.05,0.9
set xrange [-3:3]
set yrange [-5:5]
set arrow from -3,0 to 3,0 nohead ls 2
set arrow from 0,-10 to 0,10 nohead ls 2
plot f2(x) notitle ls 1 lc "#0077FF"

unset arrow
@NOXAXIS; @NOYAXIS
unset label; set label "\\Huge $\\sin\\left(x\\right)$" at graph 0.05,0.9
set xrange [-15:15]
set yrange [-4:4]
set arrow from -15,0 to 15,0 nohead ls 2
set arrow from 0,-4 to 0,4 nohead ls 2
plot f3(x) notitle ls 1 lc "#2AD200"

unset arrow
@YAXIS; @XAXIS
unset label; set label "\\Huge $\\log\\left(x\\right)$" at graph 0.02,0.9
set xrange [-4.5:10]
set yrange [-4:4]
set arrow from -4.5,0 to 10,0 nohead ls 2
set arrow from 0,-4 to 0,4 nohead ls 2
plot f4(x) notitle ls 1 lc "#AA11FF"

unset arrow
@NOYAXIS; @XAXIS
unset label; set label "\\Huge $\\left|x\\right|$" at graph 0.05,0.9
set xrange [-6:6]
set yrange [-1:4]
set arrow from -6,0 to 6,0 nohead ls 2
set arrow from 0,-1 to 0,4 nohead ls 2
plot f5(x) notitle ls 1 lc "#FF9700"

unset arrow
@NOYAXIS; @XAXIS
unset label; set label "\\Huge $\\sqrt{x}$" at graph 0.05,0.9
set xrange [-3:10]
set yrange [-1:5]
set arrow from -3,0 to 10,0 nohead ls 2
set arrow from 0,-1 to 0,5 nohead ls 2
plot f6(x) notitle ls 1 lc "#00A9FF"
