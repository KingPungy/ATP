make nOne args 0
make tempo 0
make result 0

#If n <= 1   return n 
#===============================================

if nOne 0
    make tempo 1
    make result nOne
endif

if nOne 1
    make tempo 1
    make result nOne
endif

#===============================================

#Else return fib(n-1) + fib(n-2)
#===============================================

if tempo 0
    while
        minus nOne 1
        fibonacci res1 nOne
        plus result res1
        plus tempo 1
    endwhile tempo 2
endif
#===============================================