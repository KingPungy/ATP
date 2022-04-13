make n args 0

make f3 0
make f1 1
make f2 1
make result 0
    greater grtr f3 n

while 
    greater grtr2 f3 n
    make grtr grtr2
    if f3 n 
        make result 1
    endif
endwhile grtr 1