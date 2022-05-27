unset multiplot
reset
load 'moreland.gp'
eval setdef('tex','0')

output='fw'
if (tex == 1) {
  set lmargin at screen 0
  set rmargin at screen 1
  set bmargin at screen 0
  set tmargin at screen 1
  set term lua tikz standalone createstyle size 4in,2in  #fontscale 0.6
  set output output.'.tex'
}

fn='fw-eigu'
dat=fn.'.dat'
par=fn.'.par'
load par

###
# do stuff

wf_zoom=0.2

set xrange [-nwell*1.5:nwell*1.5]
#set yrange [-1:0.2]
#set yrange [-v:v*0.2]
set yrange [-0.55:0.1]
set ytics -0.5,0.1,0

#p dat every :::0::0 u ($3-nsys/2):(-$4/v) w l lc -1 notit, \
   #  '' every :1 u ($3-nsys/2):($5*wf_zoom + $2/(-v)) w l notit

set label sprintf('$V=%1.2f$', v) at first nwell*0.5, first 0.05
p dat every :::0::0 u ($3-nsys/2):4 w l lc -1 notit, \
  for [n=0:nbound-1] '' every :::n::n u ($3-nsys/2):($5*wf_zoom + $2) w l lc n+1 notit
#
###

if (tex == 1){
  unset output
  set term wxt
  build = buildtex(output)
  print '"eval build" to build and preview'
} else {
  #print "press enter to continue"
  #pause -1
}
