import asyncio
class Grammar(): 
    def __init__(self,axiom,production):
        self.axiom = axiom
        self.production = production
        for p in self.production[self.axiom]:
            p.append("#")
        self.nonterminals = set(production.keys())
        self.terminals = set(token for production in self.production.values() for rule in production for token in rule if token not in self.nonterminals and token!="ε")
    
    # I assume between every token in the productions there is a space for now until i find better way
    # distinction between terminals and nonterminals
    def get_productions(self, nonterminal):
        return self.production.get(nonterminal, [])
    
class Parser:
    def __init__(self, grammar):
        self.grammar = grammar
        self.parse_table = {}

    def parse(self, input):
        pass  # Placeholder for the parse method, to be implemented in subclasses

class TopDownParser(Parser):
    def __init__(self, grammar):
        super().__init__(grammar)
        self.nullable = self.null()
        self.first = self.first_set()
        self.follow = self.follow_set()
        self.parse_table = self.build_parse_table()
    def null(self):
        nullable = set()
        changed = True
        while changed :
            changed = False
            for nt, productions in self.grammar.production.items():
                if nt in nullable:
                    continue
                for production in productions:
                    if production == ["ε"]:
                        nullable.add(nt)
                        changed = True
                    else:
                        test = list(symbol in nullable for symbol in production)
                        if all(test):
                            nullable.add(nt)
                            changed = True
        return nullable
        

    

#instead of using recusive first function we used iterative approach to avoid infinite recursion
# and to make it more efficient
#check markdown for more details
    def first_set(self):
        first_sets = {nt: set() for nt in self.grammar.nonterminals}
        changed = True

        while changed:
            changed = False
            for nt in self.grammar.nonterminals:
                for production in self.grammar.get_productions(nt):
                    if not production:  # Empty production
                        continue
                    first_of_production = self._first_of_sequence(production, first_sets)
                    old_size = len(first_sets[nt])
                    first_sets[nt].update(first_of_production)
                    if len(first_sets[nt]) > old_size:
                        changed = True
        return first_sets

    def _first_of_sequence(self, sequence, first_sets):
        result = set()
        for symbol in sequence:
            if symbol in self.grammar.terminals:
                result.add(symbol)
                break
            elif symbol in self.grammar.nonterminals:
                result.update(first_sets[symbol])
                if symbol not in self.nullable:
                    break
            else:
                break
        return result

                
    def follow_set(self):
        first = self.first_set()
        follow_sets = {nt: set() for nt in self.grammar.nonterminals}
        follow_sets[self.grammar.axiom].add('#')
        changed = True
        while changed:
            changed = False
            for nt , productions in self.grammar.production.items():
                for production in productions:
                    for i, symbol in enumerate(production):
                        if symbol in self.grammar.nonterminals:
                            if changed :
                                self.update_follow(follow_sets, i, symbol, production, nt, first)
                                continue
                            changed = self.update_follow(follow_sets, i, symbol, production, nt, first)
        return follow_sets
                            
    

    def update_follow(self, follow_sets, pos, symbol,production,nt,first):
        old_size = len(follow_sets[symbol])
        if pos +1 < len(production):
            for i in range(pos+1, len(production)):
                next = production[i]
                if next in self.grammar.terminals:
                    follow_sets[symbol].add(next)
                    break
                elif next in self.grammar.nonterminals:
                    follow_sets[symbol].update(first[next])
                    if next not in self.null():
                        break
                    else:
                        continue
        else:
            follow_sets[symbol].update(follow_sets[nt])
        if len(follow_sets[symbol]) != old_size:
            return True
        return False
    
    def is_nullable(self,sequence):
        if sequence == ["ε"]:
            return True
        for symbol in sequence:
            if symbol not in self.grammar.nonterminals or symbol not in self.null():
                return False
        return True

    def build_parse_table(self):
        table = {nt: {t : [] for t in self.grammar.terminals} for nt in self.grammar.nonterminals}
        for key in table.keys():
            table[key]['#'] = []
        for nt in self.grammar.nonterminals:
            for production in self.grammar.get_productions(nt):
                first_set = self._first_of_sequence(production, self.first)
                for terminal in first_set:
                    table[nt][terminal].append(production)
                if self.is_nullable(production):
                    for follow_terminal in self.follow[nt]:
                        table[nt][follow_terminal].append(production)
        return table
    
    def parse(self, input):
        input.append("#")
        stack = [self.grammar.axiom]
        while input:
            token = input[0]
            head = stack.pop()
            if head not in self.grammar.nonterminals:
                if head == token:
                    input.pop(0)
                    print(f"Matched terminal: {head}")
                    continue
                else:
                    print(f"Error: Expected '{head}' but found '{token}'")
                    return
            production = self.parse_table.get(head, {}).get(token)
            print("Debug : ")
            print(head)
            print(stack)
            print(production)
            if production != []:
                if production[0]==["ε"]:
                    print(f"Using ε-production for {head}")
                    continue
                else:
                    stack.extend(reversed(production[0]))
            else : 
                print(f"Error: Could not find production for token '{token}' with nonterminal '{head}'")
                return
        if stack:
            print(f"Error: Stack not empty after parsing: {stack}")
        else:
            print("Parsing completed successfully.")


#TODO : Figure out a way to make the lexer and parser work together
#TODO : Implement a way to handle errors in the parsing process
#Advanced TODOs:
#TODO : Implement a way to handle semantic actions during parsing
#TODO : Implement a way to handle syntax-directed translation
#TODO : Figure out how to make the IL (intermediate language) generation work with the parser

