

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

 
class AnalyseurLexicale:
    def __init__(self, input):
        self.source = input + '\n'
        self.char_courant = ''   
        self.pos_courant = -1    
        self.char_prochain()

    def char_prochain(self):
        self.pos_courant += 1
        if self.pos_courant >= len(self.source):
            self.char_courant = '\0'  
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
                ULex = ErreurCharIllegal(" '=' attendu, " + str(self.prochain()) + " trouvé")

        elif self.char_courant.isdigit():
            tempPos = self.pos_courant
            while self.prochain().isdigit():
                self.char_prochain()
            tokText = self.source[tempPos : self.pos_courant + 1] 
            ULex = UniteLexicale(tokText, UL["UL_INT"], self.pos_courant)
            
        elif self.char_courant.isalpha():
            tempPos = self.pos_courant
            while self.prochain().isalnum():
                self.char_prochain()

            tokText = self.source[tempPos : self.pos_courant + 1]
            
            idf = UniteLexicale.est_IDF(tokText)
            if idf == None: 
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
  

class AnalyseurSyntaxique:
    def __init__(self, AL, ASy, ASem, VIC):
        self.AL = AL
        self.ASy = ASy
        self.ASem = ASem
        self.VIC = VIC
        

        self.symbols = {}    
        self.UL_courante = None
        self.UL_prochaine = None
        self.ulProchaine()
        self.ulProchaine()    

    def test_UL(self, type):
        return type == self.UL_courante.type

    
    def test_UL_prochaine(self, type):
        return type == self.UL_prochaine.type

    def correspond(self, type):
        if not self.test_UL(type):
            self.ASy.append(ErreurSynIllegal(str(type) + " attendu, " + str(self.UL_courante.type) + " trouvé"))
        self.ulProchaine()

    def ulProchaine(self):
        self.UL_courante = self.UL_prochaine
        self.UL_prochaine = self.AL.UniteLexicale()

    def Comp_op(self):
        return self.test_UL(UL["UL_GT"]) or self.test_UL(UL["UL_GTEQ"]) or self.test_UL(UL["UL_LT"]) or self.test_UL(UL["UL_LTEQ"]) or self.test_UL(UL["UL_EQEQ"]) or self.test_UL(UL["UL_NTEQ"])
    
    
    # program ::= {instruction}
    def AnalyseSyntaxique(self):
        
        while self.test_UL(UL["UL_NL"]):
            self.ulProchaine()

        while not self.test_UL(UL["UL_EOF"]):
            self.instruction()     
    
    
    def instruction(self):
        
        if self.test_UL(UL["UL_INT"]):
            self.expression()
            self.nl()      

        # "WHILE" comparison "REPEAT" {instruction} "ENDWHILE"
        if self.test_UL(UL["UL_WHILE"]):
            self.ASy.append(self.UL_courante)
            self.ulProchaine()
        
            self.VIC.append("e1 :\t")
            self.VIC.append("while")        
            self.comparaison()
            
            self.correspond(UL["UL_REP"])
            
            self.nl()
            
            while not self.test_UL(UL["UL_ENDW"]):
                self.instruction()
                
            self.ASy.append(self.UL_courante)
            self.VIC.append("JUMP e1")
            self.VIC.append("e2 : ")
            self.VIC.append("\n")
            self.correspond(UL["UL_ENDW"])
            
        # "LET" ident "=" expression
        elif self.test_UL(UL["UL_LET"]):
            self.ASy.append(self.UL_courante)
            self.ulProchaine()
            
            nom_var = self.UL_courante.text 
            
            self.ASy.append(self.UL_courante)
            self.correspond(UL["UL_IDF"])
            
            self.ASy.append(self.UL_courante)
            self.correspond(UL["UL_EQ"])
            
            tempI = len(self.ASy)
            self.expression()
            tempF = len(self.ASy)
            
            temp = ''
            for i in range(tempI, tempF):
                if isinstance(self.ASy[i], ErreurSynIllegal) :
                    break;
                temp += self.ASy[i].text
                
            if nom_var in self.symbols.keys() :
                self.ASem.append(ErreurSemIllegal("Changement de valeur des constantes impossible (" + nom_var + ")"))
            else :            
                self.symbols[nom_var] = ["type: CONSTANTE", "valeur: " + str(temp), "taille : " + str(len(temp))]
                self.VIC.append("STORE @ " + nom_var)
                self.VIC.append("\n")
                
            
        elif self.test_UL(UL["UL_VAR"]):
            self.ASy.append(self.UL_courante)
            self.ulProchaine()
            
            nom_var = self.UL_courante.text 
            
            self.ASy.append(self.UL_courante)
            self.correspond(UL["UL_IDF"])
            
            self.ASy.append(self.UL_courante)
            self.correspond(UL["UL_EQ"])
            
            tempI = len(self.ASy)
            self.expression()
            tempF = len(self.ASy)
            
            temp = ''
            for i in range(tempI, tempF):
                temp += self.ASy[i].text
                        
            self.symbols[nom_var] = ["type: VARIABLE", "valeur: " + str(temp), "taille : " + str(len(temp))]
            self.VIC.append("STORE @ " + nom_var)
            self.VIC.append("\n")
            
        else:
            if self.UL_courante.type == UL["UL_EOF"] :
                return ""
            self.ASy.append(ErreurSynIllegal("Commande invalide à " + self.UL_courante.text + " (" + self.UL_courante.type + ")"))

        self.nl()


    # comparison ::= expression (("==" | "!=" | ">" | ">=" | "<" | "<=") expression)+
    def comparaison(self):

        self.expression()
        
        if self.Comp_op():
            self.ASy.append(self.UL_courante)
            temp = self.UL_courante
            self.ulProchaine()
            self.expression()
            if temp.type == (UL["UL_EQEQ"]) :
                self.VIC.append("JE e2")
            elif temp.type == (UL["UL_NTEQ"]) :
                self.VIC.append("JNE e2")
            elif temp.type == (UL["UL_GT"]) :
                self.VIC.append("JG e2")
            elif temp.type == (UL["UL_GTEQ"]) :
                self.VIC.append("JGE e2")
            elif temp.type == (UL["UL_LT"]) :
                self.VIC.append("JL e2")
            elif temp.type == (UL["UL_LTEQ"]) :
                self.VIC.append("JLE e2")
            self.VIC.append("\n")
        else:
            self.ASy.append(ErreurSynIllegal("Opérateur de comparaison attendu: " + self.UL_courante.text))

        while self.Comp_op():
            self.ulProchaine()
            self.expression()

    # expression ::= terme {( "-" | "+" ) terme}
    def expression(self):

        n = self.terme()     
             
        while self.test_UL(UL["UL_PLUS"]) or self.test_UL(UL["UL_MINUS"]):
            self.ASy.append(self.UL_courante)
            self.ulProchaine()
            self.terme()
            
        if n.type == (UL["UL_PLUS"]) :
            self.VIC.append("ADD " + self.UL_courante.text)
        elif n.type == (UL["UL_MINUS"]) :
            self.VIC.append("SUB " + self.UL_courante.text)
        if n.type == (UL["UL_MUL"]) :
            self.VIC.append("MUL " + self.UL_courante.text)
        elif n.type == (UL["UL_DIV"]) :
            self.VIC.append("DIV " + self.UL_courante.text) 


    # term ::= facteur {( "/" | "*" ) facteur}
    def terme(self):

        self.Sexpression()
        temp = self.UL_courante
        
        while self.test_UL(UL["UL_MUL"]) or self.test_UL(UL["UL_DIV"]):
            if self.test_UL(UL["UL_DIV"]) :
                self.ASy.append(self.UL_courante)
                self.ulProchaine()
                if self.UL_courante.text == '0' :
                    self.ASem.append(ErreurSemIllegal("Division par 0"))
                self.Sexpression()
            else : 
                self.ASy.append(self.UL_courante)
                self.ulProchaine()
                self.Sexpression()
        
        return temp


    # Sexpression ::= ["+" | "-"] facteur
    def Sexpression(self):
        if self.test_UL(UL["UL_PLUS"]) or self.test_UL(UL["UL_MINUS"]):
            self.ulProchaine()        
        self.facteur()


    # primary ::= number | ident
    def facteur(self):
        
        self.ASy.append(self.UL_courante)

        if self.test_UL(UL["UL_INT"]): 
            if len(self.VIC) == 0 or len(self.VIC) == 1:
                self.VIC.append("LOADC " + self.UL_courante.text)
            elif self.VIC[-2] == "while" :
                self.VIC.append("LOADC " + self.UL_courante.text)
                self.VIC.append("CMP")                                       
            else :
                self.VIC.append("LOADC " + self.UL_courante.text)
            self.ulProchaine()
        elif self.test_UL(UL["UL_IDF"]):
            if self.UL_courante.text not in self.symbols:
                self.ASem.append(ErreurSemIllegal("Variable référenciée avant affectation: " + self.UL_courante.text))
            else :
                self.VIC.append("LOAD @ " + self.UL_courante.text)
            self.ulProchaine()
        else:
            self.ASy.append(ErreurSynIllegal("Commande inattendue à " + self.UL_courante.text))

    # nl ::= '\n'+
    def nl(self):
        
        self.ASy.append(self.UL_courante)
        self.correspond(UL["UL_NL"])
        
        while self.test_UL(UL["UL_NL"]):
            self.ulProchaine()
            
            
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
        AL = AnalyseurLexicale(cmd)
        AL_result = AnalyseurLexicale(cmd)
        
        while (AL.prochain() != '\0') :
            Un_Lex.append(AL.UniteLexicale())
            AL.char_prochain()
        
        
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

        AS = AnalyseurSyntaxique(AL_result, [], [], [])
        AS.AnalyseSyntaxique()
           
        ASy_result = AS.ASy
        
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
        
        
        ASem_result = AS.ASem
        TableSymbols = AS.symbols
        
        
        print("Table des Symboles : \n")
        
        for o, p in TableSymbols.items() :
            print(o, ' : ', p, end="\n")  
        
        for k in ASem_result :
            if isinstance(k, ErreurSemIllegal) :
                print("\n" + str(k))
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
        
        
        VIC = AS.VIC
        
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