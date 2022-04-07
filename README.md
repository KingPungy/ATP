
TODO:


RESTRICTIONS:
 only ONE argument per function



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

Deze achter de functie call te zetten bijv. {Functie} {ReturnVar} {Argument} 

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
