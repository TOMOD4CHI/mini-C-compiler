# Mini C-like Compiler

## Overview
This project is a work-in-progress implementation of a compiler for a simplified C-like programming language. The compiler is designed to process a subset of C-like syntax, including basic constructs such as variable declarations, assignments, conditionals (if-else), loops (while and for), and function declarations. The goal is to create a functional compiler that can tokenize, parse, and eventually generate code for this custom language.

## Current Features
- **Lexical Analysis**: The lexer processes input source code, recognizes tokens (e.g., keywords, identifiers, numbers, operators), and handles both single-line (`//`) and multi-line (`/* */`) comments.
- **Grammar Definition**: A context-free grammar is defined to describe the syntax of the language, including support for function declarations, main function, variable declarations, assignments, and control flow statements.
- **Parsing Infrastructure**: The parser calculates FIRST, FOLLOW, and NULLABLE sets to support predictive parsing. It uses an iterative approach to avoid infinite recursion in FIRST set computation.

## Planned Features
The compiler is still under development, with plans to implement both **top-down** and **bottom-up** parsing techniques, as studied in my compiler design course.
- Future phases will include semantic analysis, intermediate code (IL) generation, and basic code optimization.

## Project Structure
- `lexer.py`: Implements the lexical analyzer to tokenize input source code.
- `parser.py`: Contains the core parsing logic, including grammar processing and FIRST/FOLLOW set computation.
- `Test.py`: Defines the grammar for the C-like language and includes a test script to demonstrate parsing capabilities.

## Future Work
- Complete the implementation of top-down and bottom-up parsers.
- Add semantic analysis to check for type correctness and variable scoping.
- Generate intermediate code and target executable code.
- Enhance error handling and reporting for better user feedback.

## Acknowledgments
This project is inspired by concepts learned in my compiler design course, with a focus on applying theoretical knowledge to practical implementation.
