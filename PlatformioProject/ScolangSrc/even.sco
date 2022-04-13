make para args 0
make tempo 1
make result 1



if para 0
# show "even"
minus tempo 1
endif

if tempo 1

minus para 1
odd tempo2 para
minus result 1
plus result tempo2
endif