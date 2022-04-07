make para args 0
make temp 1
make result 1

# show "in functie even" #

if para 0
show "even"
minus temp 1
endif

if temp 1
# show "in else even" #
minus para 1
odd temp2 para
minus result 1
plus result temp2
endif