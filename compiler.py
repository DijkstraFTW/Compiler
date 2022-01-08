

# Imports

import sys


# Unités lexicales 


UL = {
    
    "UL_INT" : "INTEGER",
    "UL_PLUS" : "PLUS",
    "UL_MINUS" : "MINUS",
    "UL_MUL" : "MULTIPLY",
    "UL_DIV" : "DIVIDE",
    "UL_NL" : "NEWLINE",
    "UL_IDF" : "IDENTIFIER",
    "UL_LET" : "LET",
    "UL_VAR" : "VAR",
    "UL_THEN" : "THEN",
    "UL_WHILE" : "WHILE",
    "UL_REP" : "REPEAT",
    "UL_ENDW" : "ENDWHILE",
    "UL_EQ" : "IS_EQUAL_TO",
    "UL_EQEQ" : "EQUALS",
    "UL_NTEQ" : "NOT_EQUAL",
    "UL_LT" : "LESS_THAN",
    "UL_LTEQ" : "LESS_THAN_EQUAL",
    "UL_GT" : "GREATER_THAN",
    "UL_GTEQ" : "GREATER_THAN_EQUAL",
    "UL_EOF" : "END_OF_FILE"
    
}

# Classes

class UniteLexicale:   
    def __init__(self, text, type, pos):
        self.text = text  
        self.type = type
        self.pos = pos           
        
    def __repr__(self):        
        return "(" + str(self.type) + ":" + str(self.text) + ")"

    def est_IDF(textUL):
        for i in UL:
            if UL[i] == textUL :
                return UL[i]
        return None    

 
class AnalyseLexicale:
    def __init__(self, input):
        self.source = input + '\n'
        self.char_courant = ''   
        self.pos_courant = -1    
        self.char_prochain()

    def char_prochain(self):
        self.pos_courant += 1
        if self.pos_courant >= len(self.source):
            self.char_courant = '\0'  # EOF
        else:
            self.char_courant = self.source[self.pos_courant]

    def prochain(self):
        if self.pos_courant + 1 >= len(self.source):
            return '\0'
        return self.source[self.pos_courant+1]
    
    def sauter_vide(self):
        while self.char_courant == ' ' or self.char_courant == '\t':
            self.char_prochain()

    def UniteLexicale(self):
        self.sauter_vide()
        ULex = None

        if self.char_courant == '+':
            ULex = UniteLexicale(self.char_courant, UL["UL_PLUS"], self.pos_courant)
        elif self.char_courant == '-':
            ULex = UniteLexicale(self.char_courant, UL["UL_MINUS"], self.pos_courant)
        elif self.char_courant == '*':
            ULex = UniteLexicale(self.char_courant, UL["UL_MUL"], self.pos_courant)
        elif self.char_courant == '/':
            ULex = UniteLexicale(self.char_courant, UL["UL_DIV"], self.pos_courant)
        elif self.char_courant == '=':
            if self.prochain() == '=':
                temp = self.char_courant
                self.char_prochain()
                ULex = UniteLexicale(temp + self.char_courant, UL["UL_EQEQ"], self.pos_courant)
            else:
                ULex = UniteLexicale(self.char_courant, UL["UL_EQ"], self.pos_courant)
        elif self.char_courant == '>':
            if self.prochain() == '=':
                temp = self.char_courant
                self.char_prochain()
                ULex = UniteLexicale(temp + self.char_courant, UL["UL_GTEQ"], self.pos_courant)
            else:
                ULex = UniteLexicale(self.char_courant, UL["UL_GT"], self.pos_courant)
        elif self.char_courant == '<':
            if self.prochain() == '=':
                temp = self.char_courant
                self.char_prochain()
                ULex = UniteLexicale(temp + self.char_courant, UL["UL_LTEQ"], self.pos_courant)
            else:
                ULex = UniteLexicale(self.char_courant, UL["UL_LT"], self.pos_courant)
        elif self.char_courant == '!':
            if self.prochain() == '=':
                temp = self.char_courant
                self.char_prochain()
                ULex = UniteLexicale(temp + self.char_courant, UL["UL_NTEQ"], self.pos_courant)
            else:
                ULex = ErreurCharIllegal("Expected !=, got !" + self.peek())

        elif self.char_courant.isdigit():
            tempPos = self.pos_courant
            while self.prochain().isdigit():
                self.char_prochain()
            tokText = self.source[tempPos : self.pos_courant + 1] # Get the substring.
            ULex = UniteLexicale(tokText, UL["UL_INT"], self.pos_courant)
            
        elif self.char_courant.isalpha():
            tempPos = self.pos_courant
            while self.prochain().isalnum():
                self.char_prochain()

            tokText = self.source[tempPos : self.pos_courant + 1] # Get the substring.
            
            idf = UniteLexicale.est_IDF(tokText)
            if idf == None: # Identifier
                ULex = UniteLexicale(tokText, UL["UL_IDF"], self.pos_courant)
            else:   
                ULex = UniteLexicale(tokText, idf, self.pos_courant)
        elif self.char_courant == '\n':
            ULex = UniteLexicale('\n', UL["UL_NL"], self.pos_courant)
        elif self.char_courant == '\0':
            ULex = UniteLexicale('', UL["UL_EOF"], self.pos_courant)
        else:
            ULex = ErreurCharIllegal("Charactère inconnu: " + self.char_courant)

        self.char_prochain()
        return ULex
  

class Parser:
    def __init__(self, lexer, ASy, ASem, VIC):
        self.lexer = lexer
        self.ASy = ASy
        self.ASem = ASem
        self.VIC = VIC
        

        self.symbols = {}    # All variables we have declared so far.
        self.curToken = None
        self.peekToken = None
        self.nextToken()
        self.nextToken()    # Call this twice to initialize current and peek.

    # Return true if the current token matches.
    def checkToken(self, kind):
        return kind == self.curToken.type

    # Return true if the next token matches.
    def checkPeek(self, kind):
        return kind == self.peekToken.type

    # Try to match current token. If not, error. Advances the current token.
    def match(self, kind):
        if not self.checkToken(kind):
            self.ASy.append(ErreurSynIllegal("Expected " + str(kind) + ", got " + str(self.curToken.type)))
        self.nextToken()

    # Advances the current token.
    def nextToken(self):
        self.curToken = self.peekToken
        self.peekToken = self.lexer.UniteLexicale()
        # No need to worry about passing the EOF, lexer handles that.

    # Return true if the current token is a comparison operator.
    def isComparisonOperator(self):
        return self.checkToken(UL["UL_GT"]) or self.checkToken(UL["UL_GTEQ"]) or self.checkToken(UL["UL_LT"]) or self.checkToken(UL["UL_LTEQ"]) or self.checkToken(UL["UL_EQEQ"]) or self.checkToken(UL["UL_NTEQ"])
    
    # Production rules.

    # program ::= {statement}
    def program(self):
        
        # Since some newlines are required in our grammar, need to skip the excess.
        while self.checkToken(UL["UL_NL"]):
            self.nextToken()

        # Parse all the statements in the program.
        while not self.checkToken(UL["UL_EOF"]):
            self.statement()     
    
    # One of the following statements...
    def statement(self):
        # Check the first token to see what kind of statement this is.
        
        if self.checkToken(UL["UL_INT"]):
            self.expression()
            self.nl()      

        # "WHILE" comparison "REPEAT" {statement} "ENDWHILE"
        if self.checkToken(UL["UL_WHILE"]):
            self.ASy.append(self.curToken)
            self.nextToken()
        
            self.VIC.append("e1 :\t")
            self.VIC.append("while")        
            self.comparison()
            
            self.match(UL["UL_REP"])
            
            self.nl()
            
            # Zero or more statements in the loop body.
            while not self.checkToken(UL["UL_ENDW"]):
                self.statement()
                
            self.ASy.append(self.curToken)
            self.VIC.append("JUMP e1")
            self.VIC.append("e2 : ")
            self.VIC.append("\n")
            self.match(UL["UL_ENDW"])
            
        # "LET" ident "=" expression
        elif self.checkToken(UL["UL_LET"]):
            self.ASy.append(self.curToken)
            self.nextToken()
            
            var_name = self.curToken.text 
            
            self.ASy.append(self.curToken)
            self.match(UL["UL_IDF"])
            
            self.ASy.append(self.curToken)
            self.match(UL["UL_EQ"])
            
            tempI = len(self.ASy)
            self.expression()
            tempF = len(self.ASy)
            
            temp = ''
            for i in range(tempI, tempF):
                if isinstance(self.ASy[i], ErreurSynIllegal) :
                    break;
                temp += self.ASy[i].text
                
            if var_name in self.symbols.keys() :
                self.ASem.append(ErreurSemIllegal("Changement de valeur des constantes impossible (" + var_name + ")"))
            else :            
                self.symbols[var_name] = ["type: CONSTANTE", "valeur: " + str(temp), "taille : " + str(len(temp))]
                self.VIC.append("STORE @ " + var_name)
                self.VIC.append("\n")
                
            
        elif self.checkToken(UL["UL_VAR"]):
            self.ASy.append(self.curToken)
            self.nextToken()

            #  Check if ident exists in symbol table. If not, declare it.
            
            var_name = self.curToken.text 
            
            self.ASy.append(self.curToken)
            self.match(UL["UL_IDF"])
            
            self.ASy.append(self.curToken)
            self.match(UL["UL_EQ"])
            
            tempI = len(self.ASy)
            self.expression()
            tempF = len(self.ASy)
            
            temp = ''
            for i in range(tempI, tempF):
                temp += self.ASy[i].text
                        
            self.symbols[var_name] = ["type: VARIABLE", "valeur: " + str(temp), "taille : " + str(len(temp))]
            self.VIC.append("STORE @ " + var_name)
            self.VIC.append("\n")
            

        # This is not a valid statement. Error!
        else:
            if self.curToken.type == UL["UL_EOF"] :
                return ""
            self.ASy.append(ErreurSynIllegal("Invalid statement at " + self.curToken.text + " (" + self.curToken.type + ")"))

        # Newline.
        self.nl()


    # comparison ::= expression (("==" | "!=" | ">" | ">=" | "<" | "<=") expression)+
    def comparison(self):

        self.expression()
        
        if self.curToken.type == (UL["UL_EQEQ"]) :
            self.VIC.append("JEQ ")
        elif self.curToken.type == (UL["UL_NTEQ"]) :
            self.VIC.append("JNEQ ")
        elif self.curToken.type == (UL["UL_GT"]) :
            self.VIC.append("JGT ")
        elif self.curToken.type == (UL["UL_GTEQ"]) :
            self.VIC.append("JGEQ ")
        elif self.curToken.type == (UL["UL_LT"]) :
            self.VIC.append("JLR ")
        elif self.curToken.type == (UL["UL_LTEQ"]) :
            self.VIC.append("JLEQ ")
        
        
        # Must be at least one comparison operator and another expression.
        if self.isComparisonOperator():
            self.ASy.append(self.curToken)
            self.nextToken()
            self.expression()
        else:
            self.ASy.append(ErreurSynIllegal("Expected comparison operator at: " + self.curToken.text))

        while self.isComparisonOperator():
            self.nextToken()
            self.expression()


    # expression ::= term {( "-" | "+" ) term}
    def expression(self):

        n = self.term()     
             
        # Can have 0 or more +/- and expressions.
        while self.checkToken(UL["UL_PLUS"]) or self.checkToken(UL["UL_MINUS"]):
            self.ASy.append(self.curToken)
            self.nextToken()
            self.term()
            
        if n.type == (UL["UL_PLUS"]) :
            self.VIC.append("ADD " + self.curToken.text)
        elif n.type == (UL["UL_MINUS"]) :
            self.VIC.append("SUB " + self.curToken.text)
        if n.type == (UL["UL_MUL"]) :
            self.VIC.append("MUL " + self.curToken.text)
        elif n.type == (UL["UL_DIV"]) :
            self.VIC.append("DIV " + self.curToken.text) 


    # term ::= unary {( "/" | "*" ) unary}
    def term(self):

        self.unary()
        temp = self.curToken
        # Can have 0 or more *// and expressions.
        while self.checkToken(UL["UL_MUL"]) or self.checkToken(UL["UL_DIV"]):
            if self.checkToken(UL["UL_DIV"]) :
                self.ASy.append(self.curToken)
                self.nextToken()
                if self.curToken.text == '0' :
                    self.ASem.append(ErreurSemIllegal("Division par 0"))
                self.unary()
            else : 
                self.ASy.append(self.curToken)
                self.nextToken()
                self.unary()
        
        return temp


    # unary ::= ["+" | "-"] primary
    def unary(self):
        # Optional unary +/-
        if self.checkToken(UL["UL_PLUS"]) or self.checkToken(UL["UL_MINUS"]):
            self.nextToken()        
        self.primary()


    # primary ::= number | ident
    def primary(self):
        self.ASy.append(self.curToken)

        if self.checkToken(UL["UL_INT"]): 
            if len(self.VIC) == 0 or len(self.VIC) == 1:
                self.VIC.append("LOADC " + self.curToken.text)
            elif self.VIC[-1] in ("JEQ ", "JNEQ ", "JGT ", "JGEQ ", "JLR ", "JLEQ "):
                self.VIC[-1] = self.VIC[-1] + self.curToken.text + " e2" +"\n"
            else :
                self.VIC.append("LOADC " + self.curToken.text)
            self.nextToken()
        elif self.checkToken(UL["UL_IDF"]):
            if self.curToken.text not in self.symbols:
                self.ASem.append(ErreurSemIllegal("Referencing variable before assignment: " + self.curToken.text))
            else :
                self.VIC.append("LOAD @ " + self.curToken.text)
            self.nextToken()
        else:
            self.ASy.append(ErreurSynIllegal("Unexpected token at " + self.curToken.text))

    # nl ::= '\n'+
    def nl(self):
        self.ASy.append(self.curToken)
        self.match(UL["UL_NL"])
        
        while self.checkToken(UL["UL_NL"]):
            self.nextToken()
            
            
# Erreurs

class ErreurCharIllegal:
    
    def __init__(self, char_erreur) :
        self.char_erreur = char_erreur
        
    def __repr__(self):
        return "< Charactère illégal : '" + self.char_erreur + " '"
    
class ErreurSynIllegal:
    
    def __init__(self, syn_erreur) :
        self.syn_erreur = syn_erreur
        
    def __repr__(self):
        return "< Syntaxe invalide : '" + self.syn_erreur + " '"
    
class ErreurSemIllegal:
    
    def __init__(self, sem_erreur) :
        self.sem_erreur = sem_erreur
        
    def __repr__(self):
        return "< Sémantique invalide : '" + str(self.sem_erreur) + " '"
            

# Compilation & Execution

def compilation(cmd) :
                   
        AL_erreur = False
        ASy_erreur = False
        ASem_erreur = False
        GenCode_erreur = True
        

        # Analyse lexicale
        print("\nAnalyse Lexicale :", end="\n\n")

        Un_Lex = []
        lexer = AnalyseLexicale(cmd)
        AL_result = AnalyseLexicale(cmd)
        
        while (lexer.prochain() != '\0') :
            Un_Lex.append(lexer.UniteLexicale())
            lexer.char_prochain()
        
        
        for i in Un_Lex :
            if isinstance(i, ErreurCharIllegal) :
                print(i)
                AL_erreur = True
                break
            print("UniteLexicale ( type = '" + str(i.type) + "', valeur = '" + str(i.text) + "', position = '" + str(i.pos - len(i.text) + 1) + "' )", end="\n") 
        
        if AL_erreur :
            print()
        else :
            print("\nAnalyse Lexicale valide !") 
            
        print("\n################################################################################################################", end="\n")  
    
        # Analyse syntaxique
        

        print("\nAnalyse Syntaxique :", end="\n\n")

        parser = Parser(AL_result, [], [], [])
        parser.program()
           
        ASy_result = parser.ASy
        
        for k in ASy_result :
            if isinstance(k, ErreurSynIllegal) :
                print(k)
                ASy_erreur = True
                break
        
        
        if not ASy_erreur :
            for i in ASy_result :
                if i.type == UL["UL_NL"] :
                    print("\nNEWLINE", end = "\n")
                else :
                    print("(" + str(i.type) + ": " + str(i.text) + ")", end=" ")
        
        
        
        if ASy_erreur :
            sys.exit()
        else :
            print("\nAnalyse Syntaxique valide !")
        
        print("\n################################################################################################################", end="\n")
        
        
        
        # Analyse sémantique
        
        print("\nAnalyse Sémantique :", end="\n\n")
        
        
        ASem_result = parser.ASem
        TableSymbols = parser.symbols
        
        
        print("Table des Symboles : \n")
        
        for o, p in TableSymbols.items() :
            print(o, ' : ', p, end="\n")  
        
        for k in ASem_result :
            if isinstance(k, ErreurSemIllegal) :
                print(k, end="\n")
                ASem_erreur = True
                break
            
        if not ASem_erreur :
            for i in ASem_result :
                print(i)
        
        if ASem_erreur :
            pass
        else :
            print("\nAnalyse Sémantique valide !")
        
        
        print("\n################################################################################################################", end="\n")
        
        
        
        
        # Génération de code
        
        print("\nGénération de code :", end="\n\n")
        
        
        VIC = parser.VIC
        
        if not ASy_erreur :
            GenCode_erreur = False

            for k in range(len(VIC) - 1) :
                if VIC[k] == "while" :
                    for i in range(k, len(VIC) - 1) :
                        if VIC [i] == "e2 : " :
                            break
                        VIC[i] = "\t" + VIC[i]



            for i in VIC :
                if i == "\twhile":
                    continue
                print(i, end="\n")
        if GenCode_erreur :
            print("Erreur de génération de code")
            sys.exit()
        else :
            print("Génération de code valide !")
            
        print("\n################################################################################################################", end="\n")
        
    

if __name__ == '__main__' :

    print("################################################################################################################", end="\n")
    print("\t\t\t\t\t\tCompilateur\t\t\t\t\t", end="\n")
    print("\t\t\t\tProjet 3 :  Al Amrani Youssef - Akherraz Hajar\t\t\t", end="\n")
    print("################################################################################################################", end="\n\n")



    # print("Choisissez votre méthode de saisie : 1- Commande   2- Fichier ")
    # choix = int(input("---> "))
    
    
    # if choix == 1 :
        
    #     cond = True
    #     while cond:
    #         cmd = input('> ')
    #         compilation(cmd)
            
    # elif choix == 2 :
        
    #     with open("final/program.txt", "r") as inputFile:
    #         cmd = inputFile.read()
            
    #     compilation(cmd)
        
    with open("program.txt", "r") as inputFile:
        cmd = inputFile.read()
            
    compilation(cmd)
    
    
    # cond = True
    # while cond:
    #     cmd = input('> ')
    #     compilation(cmd)