tex=1
do for [x=1:50] {
    fn = sprintf('fw-eigu-v=-%1.2f',x*0.01)
    output = sprintf('fw-v=%1.2f',x*0.01)
    print(sprintf('plotting v = %1.2f', x*0.01))
    load 'fw.gp'
}
