import re,sys,os


class Token : 
    def __init__(self, type, value, column, lineno):
        self.type = type
        self.value = value
        self.lineno = lineno
        self.column = column
    def __str__(self):
        return f'Token({self.type}, {self.value}, {self.lineno}, {self.column})'

def tokenize(source) :
    line = 1
    column = 1
    tokens = []
    keywords = {'if', 'else', 'while', 'for', 'return', 'function', 'int', 'const','main', 'void', 'float', 'char', 'bool'}
    token_specification = [
        ('NUMBER',   r'\d+(\.\d*)?'),
        ('IDENTIFIER', r'[A-Za-z_][A-Za-z_0-9]*'),
        ('ASSIGN',   r'='),
        ('OPERATOR', r'[+\-*/]'),
        ('SEPARATOR', r'[;,\(\)\[\]\{\}]'),
        ('NEWLINE',  r'\n'),
        ('WHITESPACE', r'[ \t]+'),
        ('Unknown', r'.'),
        ('END', r'$')
    ]
    source = re.sub(r'/\*.*?\*/', '', source, flags=re.DOTALL)
    source = re.sub(r'//.*?$', '', source, flags=re.MULTILINE)
    regex = "|".join(f"(?P<{pair[0]}>{pair[1]})" for pair in token_specification)
    for match in re.finditer(regex,source):
        type = match.lastgroup
        value = match.group(type)
        if type == 'NEWLINE': 
            line +=1
            column = 1
            continue
        if type == 'WHITESPACE':
            column += len(value)
            continue
        if type == 'IDENTIFIER' and value in keywords:
            type = value.upper()
        if type == 'NUMBER':
            if '.' in value:
                type = 'FLOAT'
            else:
                type = 'INT'
        if type =='Unkown':
            raise ValueError(f"Unknown token: {value} at line {line}, column {column}")
            break
        if type == 'END':
            break
        tokens.append(Token(type, value, column, line))
        column += len(value)
    return tokens


def test_tokenize():
    test_source = """
    int main() {
        float x = 3.14;
        int y = 42;
        char c = 'a';
        /* Multi-line
           comment */
        if (x > y) {
            x = x + y;
        } else {
            x = x - y;
        }
    }
    """
    tokens = tokenize(test_source)
    for token in tokens:
        print(token)

if __name__ == "__main__":
    test_tokenize()
