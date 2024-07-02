import re
class Lexical_Analysis(object):
    def __init__(self,code):
        self.input_code=code
        self.tokens=[]
        self.class_part=[]
        self.language_specifications = {
            "operators": r'\+\+|--|!=|<=|>=|==|[-+*/%=<>🤝👐💢]',
            "special_keyword": r'✍|🖨|🤔|😅|➰|➿|✅|❌|💔|🧡',
            "special_characters": r'[\(\)\[\]\{\};,:]',
            "integer": r'\b[1-9][0-9]*\b',
            "string": r'"(?:\\.|[^"\\])*"',
            "ID": r'[🔤🔢]\s*[a-zA-Z_]+[a-zA-Z0-9_]*'
        }
        
        self.class_part_values={
            "✍": "INPUT",
            "🖨": "PRINT",
            "🤔": "IF",
            "😅":"ELSE",
            "➰": "FOR",
            "➿": "WHILE",
            "✅": "TRUE",
            "❌": "FALSE",
            "💔": "BREAK",
            "🧡": "CONTINUE",
            "🤝":"AND",
            "👐":"OR",
            "💢":"NOT",
            "<": "LT",
            ">": "GT",
            "<=":"LTE",
            ">=":"GTE",
            "=": "EQ",
            "+": "ADD",
            "-": "SUB",
            "*": "MUL",
            "/": "DIV",
            "%":"MOD",
            "++":"INC",
            "--":"DEC",
            "!=":"NEQ",
            "==":"EQT",
            "[": "OSB",
            "]": "CSB",
            "{": "OCB",
            "}": "CCB",
            "(": "ORB",
            ")": "CRB",
            ":": "COLON",
            ";": "SEMI COLON",
            ",": "COMMA",
            "?":"QM",
            }
        
    def get_tokens(self):
        position=1
        while (position<len(self.input_code)):
            for pattern in self.language_specifications.values():
                match=re.match(pattern,self.input_code[position::])
                if match:
                    token=match.group()
                    self.tokens.append(token)
                    position+=len(token)
                    break
            position+=1

    def class_parts(self):
        for token in self.tokens:
            for cls,pattern in self.language_specifications.items():
                if re.match(pattern,token):
                    if token in self.class_part_values:
                        self.class_part.append(self.class_part_values[token])
                    elif (re.match(self.language_specifications["ID"],token)):
                          self.class_part.append("ID")
                    elif (re.match(self.language_specifications["integer"],token)):
                        self.class_part.append("INT")
                    elif (re.match(self.language_specifications["string"],token)):
                        self.class_part.append("STRING")
                        

