show "=======[Begin]======="

defunc fibonacci fib
defunc even even
defunc odd odd 
defunc multi multi
defunc sommig sommig
defunc greater greater
defunc power power
defunc divF divF

defunc add add
defunc subtract subtract


make iter 0
make max 3
show "max =" max

if iter max
    show "iter == max"
endif

while
    show "loop iter =" iter
    plus iter 1
    if iter 3                          # Nested if statements  
        show "wow iter has reached 3"
    endif
endwhile iter max

if iter max
    show "iter == max"
    while                              # Nested while statements 
        minus iter 1
        show "loop2 iter =" iter
    endwhile iter 0
endif

show "=======[End]======="
