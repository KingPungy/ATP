## TODO:
- Edit comments
- Delete compiler2.py
- test assembly



# Scolang

### Supports:
- Loops
- Conditional Statements
- Printing Strings and Numbers
- Functions
- Recursion

## Syntax

|Identifier|Explanation|C equivalent|
|:-:|:-:|:-:|
|<b>plus</b> var1 var2| Adds var2 to var1| var1 = var1 + var2|
|<b>min</b> var1 var2| Subtracts var2 from var1| var1 = var1 - var2|
|<b>divide</b> var1 var2| Divides var1 by var2 and floors the result to nearest interger| var1 = floor(var1 / var2)|
|<b>times</b> var1 var2| Multiplies var1 by var2 and stores the result in var1| var1 = var1 * var2|
|<b>make</b> name value/variable| Assigns the value or the value stored in a variable to the variable with the given name | [ int name = 2 ] or [ int name = name2 ] |
|<b>show</b> var1 | Prints the value stored in var1 | printf( var1 ) |
|<b>show</b> "string" "string2" var1 | Prints all following strings and variables with a space in between | printf( "string" + " " + "string2" + " "+ var1 )  |
|<b>if</b> var1 var2 | If the two variables are equal will execute block between <b>if</b> and <b>endif</b> | if (var1 == var2){block} |
|<b>while</b> {block} <b>endwhile</b> var1 var2 | <b>while</b> signals the start of the loop. <b>endwhile</b> signals the end and contains the condition. The condition gets checked at the start of the loop. the while functions as a while not | whileNot(var1 == var2){block} |
| <b>defunc</b> funcName filename| <b>defunc</b> defines signals a function call. The first word after <b>defunc</b> is the name of the function with wich you call the function later on. the third word is the name of the file containing the function code. Note that the filename does not need the extension of ".sco" this is done automatically  | int funcName(var1,var2,var3,var4) |
|funcName returnVar var1 var2 var3 var4| Calls the function with the name funcName and stores the return value in the returnVar. All following variables are function arguments that can be accessed within the function | returnVar = funcName(var1, var2, var3, var4) |

### Function definition and call Example:         
Lets say this function returns a 1 or a 0 if var1 is bigger than var2
```python
make var1 1                     # Variable Assigment
make var2 2


defunc funcName FuncFilename    # function definition filename is without extension

                                # function call
funcName Return var1 var2       # Return = funcName(var1,var2)
show Return                     # printf( Return )

plus var1 var2                  # Add var2 to var1 

funcName Return2 var1 var2
show Return2

==============Terminal===============
0
1
```

### Example of loops and if statements:

```python
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

==============Terminal===============
max = 3
loop iter = 0
loop iter = 1
loop iter = 2
wow iter has reached 3
iter == max
loop2 iter = 2
loop2 iter = 1
loop2 iter = 0
```




# ATP
Gekozen taal: Eigen taal  
Turing-compleet omdat:

Code is geschreven in functionele stijl.

Taal ondersteunt:
Loops? Voorbeeld: [helloworld.sco] - [11]  
Goto-statements? Voorbeeld: [file] - [regel]  
Lambda-calculus? Voorbeeld: [files] - [regels]  

## Bevat: 
Classes met inheritance: bijvoorbeeld [AST.py](AST.py) - [Regel 12-47]  
Object-printing voor elke class: [ja]  
Decorator: functiedefinitie op [lex.py](lex.py) - [regel 150], toegepast op [main.py](main.py) - [regel 53]  
Type-annotatie: Haskell-stijl in comments: [ja/nee]; Python-stijl in functiedefinities: [ja, maar nog niet volledig]   
Minstens drie toepassingen van hogere-orde functies:  
1. [lex.py](lex.py) - [regel 47,147]
2. [AST.py](AST.py) - [regel 120,208,216]
3. [interpreter.py](interpreter.py) - [regel 35,36,78]

## Interpreter-functionaliteit Must-have:  
Functies: [één per file / meer per file]  

meerdere functies kunnen via 1 file worden aangeroepen
maar de functie zelf staat in zijn eentje in een file

Functie-parameter kan aan de interpreter meegegeven worden door:

Deze achter de functie call te zetten. Voorbeeld:
```
{FunctionName}{ReturnVarName}{Argument1}{Argument2}{Argument3}{Argument4} 

```

Functies kunnen andere functies aanroepen: zie voorbeeld [even.sco](even.sco) - [regel 15]  

Functie resultaat wordt op de volgende manier weergegeven: 

```python
make fibIn 9
#def  function function file#
defunc fibonacci fib

fibonacci resfib fibIn
#This funtion calculates the total of all numbers up until the {n}th number in the fibonacci sequence #
show resfib #fibonacci 9 = 34#

even resEven resfib # even resfib[34] = even#

```
Het resultaat kan in de functie getoond worden of via de return variabele terug gegeven worden en in de main getoond worden. Als er geen return waarde nodig is omdat deze in de funtie al getoond word dan kan "void" als return variabele gegeen worden dan word er niks mee gedaan

## Interpreter-functionaliteit (should/could-have):  
[Gekozen functionaliteit] geïmplementeerd door middel van de volgende functies: a) [functie] in [file] op regel [regel]  
[Extra functionaliteit overlegd met docent, goedkeuring: datum e-mail; overeengekomen max. aantal punten: X]  
