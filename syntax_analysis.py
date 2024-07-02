from lexical_analysis import Lexical_Analysis

# input Code
code=''' 🔢number = 5 
         🔢ball = 10
         ➰ ( 🔢number = 6 , 🔢number <= 10 , 🔢number ++ ) {
                 🔢ball = 7
         }    
'''
#Analyze Code 
Lexemes=Lexical_Analysis(code)
#Give Tokens
Lexemes.get_tokens()
#Give Class Part
Lexemes.class_parts()

# Parser
class Parse_Tree(object):
    def __init__(self,grammar):
        #Input Grammar
        self.grammar=grammar
        self.terminals= [terminal for terminal in Lexemes.class_part_values.values()]
        self.terminals.append("DT")
        self.terminals.append("ID")
        self.terminals.append("INT")
        self.terminals.append("STRING")
        self.non_terminals= [non_terminals for non_terminals in self.grammar.keys()]
        self.first={}
        self.follow={}
        self.parse_table={}
        self.parser=[]
    
    #Get First Set For Each Non-terminal
    def first_set(self):
        for non_terminal in self.grammar:
            self.first.update({non_terminal:set()})
        global epsilon
        epsilon="null"

        def first_of(symbol):
            if symbol is epsilon:
                return {symbol}
            elif symbol in self.terminals:
                return {symbol}
            else:
                result=set()
                for production_values in self.grammar[symbol]:
                    if (production_values==epsilon):
                        result.add(epsilon)
                    else:
                        for production in production_values.split():
                            first_production=first_of(production)
                            result.update(first_production-{epsilon})
                            if epsilon not in first_production:
                                break
                        else:
                            result.add(epsilon)
            return result
        
        for i in self.non_terminals:
            self.first[i]=first_of(i)    

    #Get Follow Set For Each Non-Terminal
    def follow_set(self):
        for non_terminals in self.non_terminals:
            self.follow.update({non_terminals:set()})
        self.follow["<Start>"].add("$")
        while True:
            updated=False
            for head,production in self.grammar.items():
                for productions in production:
                    part=productions.split()
                    for single_word in range(0,len(part)):
                        if part[single_word] in self.non_terminals:
                            follow_before=self.follow[part[single_word]].copy()
                            if single_word+1 < len(part):
                                next_part=part[single_word+1]
                                if next_part in self.terminals:
                                    self.follow[part[single_word]].add(next_part)
                                else:
                                    self.follow[part[single_word]].update(self.first[next_part]-{"null"})
                                    if "null" in self.first[next_part]:
                                        self.follow[part[single_word]].update(self.follow[head])
                            else:
                                self.follow[part[single_word]].update(self.follow[head])
                            if follow_before != self.follow[part[single_word]]:
                                updated= True
            if not updated:
                break
        return self.follow
    
    # Get LL(1) Table
    def ll1_table(self):
        for non_terminals in self.grammar:
            self.parse_table[non_terminals]={}
            for terminals in self.terminals +["$"]:
                self.parse_table[non_terminals][terminals]=None
        
        epsilon="null"

        for non_terminals in self.grammar:
            for production in self.grammar[non_terminals]:
                first_production=self.first_of_string(production.split())
                for terminals in first_production:
                    if terminals!=epsilon:
                        self.parse_table[non_terminals][terminals]=production
                    if production==epsilon or epsilon in first_production:
                        for terminals in self.follow[non_terminals]:
                            self.parse_table[non_terminals][terminals]=production

    def first_of_string(self,symbols):
        result=set()
        for symbol in symbols:
            if symbol=="null":
                result.add("null")
                continue
            if symbol in self.terminals:
                result.add(symbol)
                break
            result.update(self.first[symbol]-{'null'})
            if "null" not in self.first[symbol]:
                break
        else:
            result.add("null")
        return result
    
    #Parser
    def parse_tree(self,input_code,start_symbol):
        stack=[start_symbol]
        input_tokens=input_code.split()+["$"]
        index=0

        while stack:
            top=stack.pop()
            if top in self.terminals or top=="$":
                if top==input_tokens[index]:
                    index+=1
                else:
                    raise ValueError(f"{top} Parsing Error:Unexpected tokens")
            elif top in self.non_terminals:
                production=self.parse_table[top].get(input_tokens[index],None)
                if not production:
                    raise ValueError(f"Parsing Error: no rule for {top} on {input_tokens[index]}")
                self.parser.append((top,production))
                production_symbols=production.split()
                for symbol in reversed(production_symbols):
                    if symbol!="null":
                        stack.append(symbol)
        if index==len(input_tokens)-1:
            return self.parser
        else:
            raise("Parsing Error: Incomplete Parser")

#Input Grammer
grammar={
    "<Start>": ["<init>","<for>","<while>","<if_st>", "<print>","<exp>","<input>"],
    "<init>": ["ID <init'>"],
    "<init'>": ["COMMA ID <init'>", "EQ <value>", "null"],
    "<value>": ["STRING <value'>", "INT <value'>", "TRUE <value'>", "FALSE <value'>"],
    "<value'>": ["COMMA <value>", "<Start>", "null"],
    "<for>": ["FOR ORB <init> COMMA <condition> COMMA <count> CRB OCB <Start> CCB"],
    "<condition>": ["ID <operators> <condition'>"],
    "<condition'>": ["ID", "INT", "STRING"],
    "<operators>": ["LT", "GT", "LTE", "GTE", "EQT", "NEQ"],
    "<count>": ["ID <count'>"],
    "<count'>": ["INC", "DEC"],
    "<while>" : ["WHILE ORB <condition> CRB OCB <start> CCB"],
    "<input>" : ["DT ID EQ INPUT ORB <message> <enter> CRB <start>"],
    "<message>" : ["STRING","null"],
    "<enter>" : ["INT","STRING","TRUE","FALSE"],
    "<print>": ["PRINT ORB <print'> CRB <Start>"],
    "<print'>": ["ID <exit>", "INT <exit>", "STRING <exit>"],
    "<exit>": ["COMMA <print>", "null"],
    "<if_st>" : ["IF ORB <condition> CRB COLON THEN <start> <else>"],
    "<else>": ["ELSE <start>","null"],
    "<exp>" : ["<term> <exp'>"],
    "<exp'>" : ["ADD <term> <exp'>","SUB <term> <exp'>","null"],
    "<term>" : ["<factor> <term'>"],
    "<term'>" : ["MUL <factor> <term'>","DIV <factor> <term'>","null"],
    "<factor>": ["ORB <exp> CRB", "INT"]
}
Code_Parser=Parse_Tree(grammar)
if __name__=="__main__":
    print("FIRST SET\n")
    Code_Parser.first_set()
    for non_terminal,sets in Code_Parser.first.items():
        print(f"{non_terminal} : {sets}")
    print("\n")
    print("FOLLOW SET\n")
    Code_Parser.follow_set()
    for non_terminal,sets in Code_Parser.follow.items():
        print(f"{non_terminal} : {sets}")
    print("\n")
    print("LL(1) TABLE")
    Code_Parser.ll1_table()
    for non_terminal,sets in Code_Parser.parse_table.items():
        print(non_terminal,"\n")
        for key,values in sets.items():
            print(f"{key}:{values}",end="    ")
        print("\n")

    print("\n")
    print("PARSER\n")
    parser=" "
    for i in Lexemes.class_part:
        parser+= " "+i
    Code_Parser.parse_tree(parser,"<Start>")
    for non_terminal, production in Code_Parser.parser:
        print(f"{non_terminal} -> {production}")
        