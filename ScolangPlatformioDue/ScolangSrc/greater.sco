make a args 0
make b args 1
make result 0

while
    minus a 1
    if a b
        plus result 1
    endif
endwhile a 0