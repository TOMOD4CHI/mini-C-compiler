from parser import Parser, Grammar


productions = {
    "program": [
        ["function_declarations", "main_function"]
    ],
    "function_declarations": [
        ["function_declaration", "function_declarations"],
        []
    ],
    "function_declaration": [
        ["type", "IDENTIFIER", "(", "parameters", ")", "{", "statements", "}"]
    ],
    "main_function": [
        ["void", "main", "(", ")", "{", "statements", "}"],
        ["int", "main", "(", ")", "{", "statements", "return", "NUMBER", ";", "}"]
    ],
    "type": [
        ["int"],
        ["float"],
        ["char"],
        ["bool"],
        ["const", "int"],
        ["const", "float"],
        ["const", "char"],
        ["const", "bool"]
    ],
    "parameters": [
        ["parameter", ",", "parameters"],
        ["parameter"],
        []
    ],
    "parameter": [
        ["type", "IDENTIFIER"]
    ],
    "statements": [
        ["statement", "statements"],
        []
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
        ["if", "(", "expression", ")", "{", "statements", "}", "else", "{", "statements", "}"],
        ["if", "(", "expression", ")", "{", "statements", "}"]
    ],
    "while_statement": [
        ["while", "(", "expression", ")", "{", "statements", "}"]
    ],
    "for_statement": [
        ["for", "(", "declaration", ";", "expression", ";", "assignment", ")", "{", "statements", "}"]
    ],
    "return_statement": [
        ["return", "expression"],
        ["return"]
    ],
    "expression": [
        ["term", "OPERATOR", "expression"],
        ["term"]
    ],
    "term": [
        ["NUMBER"],
        ["IDENTIFIER"],
        ["(", "expression", ")"]
    ]
    }
grammar = Grammar("program", productions)
parser = Parser(grammar)
print(parser.first())