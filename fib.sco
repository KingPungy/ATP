make nOne args 0
make temp 1
make result 0

#If n <= 1   return n #
#===============================================#

if nOne 0
make result nOne
minus temp 1
endif

if nOne 1
make result nOne
minus temp 1
endif

#===============================================#



#Else return fib(n-1) + fib(n-2)#
#===============================================#

if temp 1

minus nOne 1
fibonacci res1 nOne
minus nOne 1
fibonacci res2 nOne

plus res1 res2
make result res1

endif
#===============================================#