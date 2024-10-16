# Compiler


[![DijkstraFTW - Compiler](https://img.shields.io/badge/DijkstraFTW-Compiler-2ea44f)](https://github.com/DijkstraFTW)  [![Made with Python](https://img.shields.io/badge/Python->=3.6-blue?logo=python&logoColor=white)](https://python.org "Go to Python homepage")

**General Introduction**

As part of my study in compilers and programming languages, I took on the challenge of building a simplified compiler from scratch. This project implements the core phases of a typical compiler: lexical analysis, parsing, semantic analysis, and code generation. The entire compiler is written in Python, with the final output being generated as x86 Assembly code.

While this is a simplified version of a full-fledged compiler, it effectively demonstrates the key concepts I learned in my Theory of Compilers course.

<br />
<br />


**The Compiler**

The program starts by allowing the user to choose either one of the following inputs :

*Command Line*

    >_

*Text file*
    
    VAR index = 5 
    LET a = 0
    LET b = 1
    VAR d = 56
    WHILE index > 0 REPEAT
	    LET c = 46 * 75
	    VAR d = d + 5
	    VAR index = index - 1
    ENDWHILE
    LET e = c * d

<br />

**Tokens used**

    UL = { "UL_INT" : "INTEGER", "UL_PLUS" : "PLUS", "UL_MINUS" : "MINUS",
    "UL_MUL" : "MULTIPLY", "UL_DIV" : "DIVIDE", "UL_NL" : "NEWLINE",
    "UL_IDF" : "IDENTIFIER", "UL_LET" : "LET", "UL_VAR" : "VAR",
    "UL_WHILE" : "WHILE", "UL_REP" : "REPEAT", "UL_ENDW" : "ENDWHILE",
    "UL_EQ" : "IS_EQUAL_TO", "UL_EQEQ" : "EQUALS", "UL_NTEQ" : "NOT_EQUAL",
    "UL_LT" : "LESS_THAN", "UL_LTEQ" : "LESS_THAN_EQUAL", 
    "UL_GT" : "GREATER_THAN", "UL_GTEQ" : "GREATER_THAN_EQUAL",
     "UL_EOF" : "END_OF_FILE" }
    
    + - * / = == != > >= < <= \n \0 VAR LET WHILE REPEAT ENDWHILE
    
    
<br />

**Execution examples** 
	
	> 45 / 89
    
    LOADC 45
    LOADC 89
    DIV
    
    Génération de code valide !



    > LET a = 678
	
	Analyse Sémantique :
    
    Table des Symboles :
    a  :  ['type: CONSTANTE', 'valeur: 678', 'taille : 3']
    
	Analyse Sémantique valide !




    > VAR b = 4
    
    Analyse Sémantique :
    
    Table des Symboles :
    
    b  :  ['type: VARIABLE', 'valeur: 4', 'taille : 1']
    
    Analyse Sémantique valide !



	# text file	
    VAR index = 6
    WHILE index > 0 REPEAT
	    LET c = 46 * 75
	    VAR index = index - 1
    ENDWHILE


		LOADC 6
		STORE @index
		
    e1: LOAD @ index
        LOADC 0
        CMP
        JG e2

        LOADC 46
        LOADC 75
        MUL
        STORE @ c

        LOAD @ index
        LOADC 1
        SUB
        STORE @ index

        JUMP e1
    e2 :

<br />

**Examples of errors**

    > 5/0
    < Sémantique invalide : 'Division par 0 '>

    > VAR a = 0
    > LET a = 56
    < Sémantique invalide : 'Changement de valeur des constantes impossible (a) '>

    > LET a s
    < Syntaxe invalide : 'IS_EQUAL_TO attendu, IDENTIFIER trouvé '


<br />

**Further improvements**

 - More functionnalities ( IF Statement / PRINT Statement / Data structures )
 - Interpreter
 - Code optimization
 - ...
