make num args 0
make tmp 1
make result 1

if num 0
    # show "even"
    minus tmp 1
endif

if tmp 1
    minus num 1
    odd tmp2 num
    minus result 1
    plus result tmp2
endif