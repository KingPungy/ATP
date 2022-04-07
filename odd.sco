make para args 0
make temp 1
make result 0

#show "in functie oneven"#

if para 0
show "odd"
minus temp 1
endif

if temp 1
#show "in else oneven"#
minus para 1
even temp2 para
plus result temp2
endif


