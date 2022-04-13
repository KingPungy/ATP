make num args 0
make tmp 1
make result 0

if num 0
    # show "odd"
    minus tmp 1
endif

if tmp 1
    minus num 1
    even tmp2 num
    plus result tmp2
endif


