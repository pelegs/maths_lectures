set terminal cairolatex standalone pdf color colortext size 10cm, 10cm
set output "leslie.tex"

set xrange [-300:300]
set yrange [-300:300]
unset tics
set border 0
unset colorbox

set style arrow 1 lw 2 heads front
set arrow arrowstyle 1 from -300,0 to 300, 0
set arrow arrowstyle 1 from 0,-300 to 0, 300
set label "$x$" at graph 1.02, 0.5 center front
set label "$y$" at graph 0.5, 1.02 center front

set palette rgb 33,13,10


plot "leslie.data" u 1:2:3 lt palette pt 7 ps 0.2 notitle
