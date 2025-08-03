class Grammar(): 
    def __init__(self,axiom,production):
        self.axiom = axiom
        self.production = production
        self.nonterminals = set(production.keys())
        self.terminals = set(token for production in self.production.values() for rule in production for token in rule if token not in self.nonterminals)
    
    #I assume between every token in the productions there is a space for now until i find better way
    # distinction between terminals and nonterminals
    def get_productions(self, nonterminal):
        return self.production.get(nonterminal, [])
    
class Parser:
    def __init__(self, grammar):
        self.grammar = grammar
        self.tokens = []
        self.current_token_index = 0
        self.first = self.first_set()
        self.follow = self.follow_set()
        self.nullable = self.null()

    def null(self):
        return [nt for nt in self.grammar.nonterminals if [] in self.grammar.get_productions(nt)]

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
                if symbol not in self.null():
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
                            self.update_follow(follow_sets, i, symbol, changed, production, nt, first)
        return follow_sets
                            
    

    def update_follow(self, follow_sets, pos, symbol,changed,production,nt,first):
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
        if len(follow_sets[symbol]) > old_size:
            changed = True
        

    
