from syntax_analysis import Code_Parser,Lexemes

class LL1(object):
    def __init__(self):
        self.parse_table={}
        self.terminals=Code_Parser.terminals
        self.non_terminals=Code_Parser.non_terminals
    def arrange(self):
        for key,value in Code_Parser.parse_table.items():
            for i in value:
                if value[i] is not None:
                    self.parse_table[(key,i)]=[value[i]]
                        
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
table=LL1()
table.arrange()
for key,value in table.parse_table.items():
    print(f"{key} : {value}")
print("\n")
print("PARSER\n")
parser=" "
for i in Lexemes.class_part:
    parser+= " "+i
Code_Parser.parse_tree(parser,"<Start>")
for non_terminal, production in Code_Parser.parser:
    print(f"{non_terminal} -> {production}")