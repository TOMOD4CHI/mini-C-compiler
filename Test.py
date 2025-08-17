from parser import *
from lexer import Lexer, Token

keywords = {'if', 'else', 'while', 'for', 'return', 'function', 'int', 'const','main', 'void', 'float', 'char', 'bool'}
token_specification = [
    ('KEYWORD', r'\b(?:' + '|'.join(keywords) + r')\b'),
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

#Simple C-like LL(1) grammar for testing
productions = {
    "program": [
        ["function_declarations", "main_function"]
    ],
    "function_declarations": [
        ["function_declaration", "function_declarations"],
        ["ε"]
    ],
    "function_declaration": [
        ["types", "IDENTIFIER", "(", "parameters", ")", "{", "statements", "}"]
    ],
    "main_function": [
        ["void", "main", "(", ")", "{", "statements", "}"],
        ["int", "main", "(", ")", "{", "statements", "return", "NUMBER", ";", "}"]
    ],
    "type": [
        ["types"],
        ["const", "types"]
    ],
    "types": [
        ["int"],
        ["float"],
        ["char"],
        ["bool"],
        ["void"]
    ],
    "parameters": [
        ["parameter", "more_parameters"],
        ["ε"]
    ],
    "more_parameters": [
        [",", "parameter", "more_parameters"],
        ["ε"]
    ],
    "parameter": [
        ["types", "IDENTIFIER"],
    ],
    "statements": [
        ["statement", "statements"],
        ["ε"]
    ],
    "statement": [
        ["declaration", ";"],
        ["assignment", ";"],
        ["if_statement"],
        ["while_statement"],
        ["for_statement"],
        ["return_statement", ";"],
        ["expression", ";"],
        [";"]
    ],
    "declaration": [
        ["type", "IDENTIFIER"],
        ["type", "IDENTIFIER", "=", "expression"]
    ],
    "assignment": [
        ["IDENTIFIER", "=", "expression"]
    ],
    "if_statement": [
        ["if", "(", "expression", ")", "{", "statements", "}", "else_statement"],
    ],
    "else_statement": [
        ["else", "{", "statements", "}"],
        ["ε"]
    ],
    "while_statement": [
        ["while", "(", "expression", ")", "{", "statements", "}"]
    ],
    "for_statement": [
        ["for", "(", "declaration", ";", "expression", ";", "assignment", ")", "{", "statements", "}"]
    ],
    "return_statement": [
        ["return", "return_value"],
    ],
    "return_value": [
        ["expression"],
        ["ε"]
    ],
    "expression": [
        ["term", "after"],
    ],
    "after": [
        ["OPERATOR", "expression"],
        ["ε"]
    ],
    "term": [
        ["NUMBER"],
        ["IDENTIFIER"],
        ["(", "expression", ")"]
    ]
    }

lexer = Lexer(keywords, token_specification)
grammar = Grammar("program", productions)
parser = TopDownParser(grammar)
print("Nullable Set :", parser.null())
print('------------------------------')
print("First Set :", parser.first)
print('------------------------------')
print("Follow Set :", parser.follow)
print('------------------------------')
print("Parse Table:")
for nt, rules in parser.parse_table.items():
    print(f"{nt}:")
    for t, production in rules.items():
        print(f"  {t} -> {production}") 


