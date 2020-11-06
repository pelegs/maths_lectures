set terminal cairolatex standalone pdf color colortext header "\\usepackage{bm}"
set output "normal_distribution.tex"

set sample 1500
set xlabel "\\Large$x$"
set ylabel "\\Large$f(x)$" rotate by 0 offset 2, 0
set xrange [-4:4]
set yrange [0:0.5]

load "../gnuplot-palettes/paired.pal"

#set label "$f(x)=\\frac{1}{\\sqrt{2\\pi}}e^{-\\frac{x^{2}}{2}}$" at 0, 0.45 tc ls 2 center front
f(x) = 1/sqrt(2*pi)*exp(-x**2/2) 
plot f(x) ls 1 with filledcurve above y=0 notitle,\
     f(x) ls 2 lw 4 notitle
