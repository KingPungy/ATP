show "=====Begin====="
show "Hello World!" "vergeet de spaties niet" "woorden tussen haakjes"

make abra -2
make b 4
show abra

# commentaar werkt zo #

while
plus abra 1
show "=loop abra=" abra "  b=" b  # en commentaar #
endwhile abra 0


defunc tweedeFunctie functiontwo
defunc eersteFunctie function
defunc hallo hallo

eersteFunctie Scott "de eerste parameter is de variabele naam waar de teruggave in wordt opgeslagen"
tweedeFunctie void "hallo vanuit tweede functie"
hallo void "wowie"

show "Regel 24 "
show abra Scott b "even tussendoor" b b

show "Regel 27"
if abra 0 
show "nul!"
make b 0
endif

if abra abra
show "If true"; make b 0
endif

if b 0
show "iets anders!"
endif


make y 2
times y -5  # 2 x -5 = -10 #
show y "y"


make test 4
while
show "test" test
minus test 1
endwhile test 0
