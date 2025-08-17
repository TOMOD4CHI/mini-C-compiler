import re,asyncio
class Token : 
    def __init__(self, type, value, column, lineno):
        self.type = type
        self.value = value
        self.lineno = lineno
        self.column = column
    def __str__(self):
        return f'Token({self.type}, {self.value}, {self.lineno}, {self.column})'

    class Lexer:
        def __init__(self,keywords, token_specification):
            self.keywords = keywords
            self.token_specification = token_specification
        def tokenize(self,source) :
            line = 1
            column = 1
            source = re.sub(r'/\*.*?\*/', '', source, flags=re.DOTALL)
            source = re.sub(r'//.*?$', '', source, flags=re.MULTILINE)
            regex = "|".join(f"(?P<{pair[0]}>{pair[1]})" for pair in self.token_specification)
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
                if type =='Unkown':
                    raise ValueError(f"Unknown token: {value} at line {line}, column {column}")
                    break
                if type == 'END':
                    yield(Token(type, '#', column, line))
                    break
                yield(Token(type, value, column, line))
                column += len(value)


        def c_test_tokenize(self):
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
            for token in self.tokenize(test_source):
                print(token)

