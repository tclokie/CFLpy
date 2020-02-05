from PDA import PDA
import queue # TODO: just import PriorityQueue
import random # TODO: just import random.random

EMPTY_STRING = ''

def concat_string_array (A):
    result = ''
    for a in A:
        result += a
    return result



class CFG:
    '''Context-Free Grammar'''
    # Default constructor; creates empty CFG
    def __init__ (self):
        self.variables = set()
        self.alphabet = {EMPTY_STRING}
        self.productions = dict()
        self.start = 'S' # MUST BE a member of {variables}

    # Create V: set of variables from PDA
    def init_variables (self, pda):
        self.variables = {self.start}
        
        # Define triple variables
        for q in pda.states:
            for A in pda.stack_alphabet:
                for p in pda.states:
                    self.variables.add((q, A, p))

    # Create alphabet
    def add_to_alphabet (self, a): # a can be a string, a set (of strings), or a list/array (of strings)
        if type(a) == str:
            self.alphabet.add(a)
        elif type(a) == set:
            self.alphabet = self.alphabet.union(a)
        else:
            assert type(a) == list
            for x in a:
                self.alphabet.add(a)

    # Initialize the productions structure, based on the variables
    def init_productions (self):
        self.productions = dict()
        for v in self.variables:
            self.productions[v] = []


    # Fill in P
    def populate_productions (self, pda):
        for q in pda.states:
            # Productions for the start variable
            self.productions[self.start].append([(pda.start_state, pda.start_stack, q)])

            # Productions for the triple variables
            for a in pda.alphabet:
                for A in pda.stack_alphabet:
                    if ((q, a, A) in pda.transitions):
                        for (q_1, B) in pda.transitions[(q, a, A)]:
                            m = len(B)
                            if (m == 0): # pop top of stack
                                self.productions[(q, A, q_1)].append([a])
                            elif (m == 1):
                                B_1 = B[0]
                                for q_2 in pda.states:
                                    self.productions[(q, A, q_2)].append([a, (q_1, B_1, q_2)])
                            else: # push onto stack
                                assert (m == 2) # Sanity check that we never push more than one symbol at a time
                                B_1 = B[0]
                                B_2 = B[1]
                                for q_2 in pda.states:
                                    for q_3 in pda.states:
                                        self.productions[(q, A, q_3)].append([a, (q_1, B_1, q_2), (q_2, B_2, q_3)])

    # using DFS, return set of variables reachable from parameter
    def _find_reachable_vars (self):
        seen = {self.start}
        stack = [self.start]
        while (len(stack) > 0):
            current = stack.pop()
            goes_to = self.productions[current]
            for prod_list in goes_to:
                for i in range (len(prod_list)):
                    next = prod_list[i]
                    if (next in self.variables) and (not next in seen):
                        seen.add(next)
                        stack.append(next)
        return seen

    # using DFS, return set of variables that can produce an all-terminal string
    def _find_productive_vars (self):
        productive_vars = set() # first, find the set of productions that have terminal-only outputs
        for v in self.variables:
            for prod in self.productions[v]:
                all_terminals = True
                for elem in prod:
                    if (elem in self.variables):
                        all_terminals = False
                    else:
                        assert (elem in self.alphabet)
                if (all_terminals):
                    productive_vars.add(v)

        change = True
        while (change): # add variables that lead to such productions
            change = False
            for v in self.productions.keys():
                if (not v in productive_vars): # don't revisit variables
                    for v_p in self.productions[v]: # v_p is a single production of v
                        flag = True
                        for p in v_p: # p is either a variable or a terminal
                            if ((not p in self.alphabet) and (not p in productive_vars)):
                                flag = False
                        if flag:
                            productive_vars.add(v)
                            change = True

        assert(self.start in productive_vars)
        return productive_vars


    # Eliminate dead production rules
    def _eliminate_useless_productions (self):
        unproductive_vars = self.variables.difference(self._find_productive_vars())
        self._remove_variables(unproductive_vars)
        del unproductive_vars

        unreachable_vars = self.variables.difference(self._find_reachable_vars())
        self._remove_variables(unreachable_vars)

    def _remove_variables (self, to_remove_from_V):
        to_remove_from_P = []

        # remove useless variables
        for v in to_remove_from_V:
            self.variables.remove(v)
            self.productions.pop(v)
            for prod_list in self.productions.values():
                for production in prod_list:
                    if (v in production):
                        to_remove_from_P.append((prod_list, production))
        # remove useless productions
        for (prod_list, production) in to_remove_from_P:
            if (production in prod_list):
                prod_list.remove(production)

    def _replace_simple_productions (self):
        vars_to_replace = {}

        # now we simplify variables with exactly one production
        for v in self.variables:
            if len(self.productions[v]) == 1: # replace instances of v with P[v]
                if (v != self.start):
                    vars_to_replace[v] = self.productions[v][0]
                elif len(self.productions[v][0]) == 1 and self.productions[v][0][0] in self.variables:
                    vars_to_replace[self.productions[v][0][0]] = v
                    self.productions[v] = self.productions[self.productions[v][0][0]]
        for prod_list in self.productions.values():
            for production in prod_list:
                for index in range(len(production)):
                    if production[index] in vars_to_replace:
                        replacements = vars_to_replace[production[index]]
                        production.pop(index)
                        i = index
                        for s in replacements:
                            production.insert(i, s)
                            i += 1

        for v in vars_to_replace:
            self.variables.remove(v)

        # now we remove empty strings from non-empty productions; combine multiple empties into one
        for prod_list in self.productions.values():
            for production in prod_list:
                empty_indices = []
                for i in range (len(production)):
                    if production[i] == EMPTY_STRING:
                        empty_indices.insert(0,i) # prepend
                for i in empty_indices:
                    production.pop(i)
                if len(production) == 0:
                    production.append(EMPTY_STRING)

    def simplify(self):
        self._eliminate_useless_productions()
        self._replace_simple_productions()


    # Count number of variables
    def count_variables (self):
        return len(self.variables)

    # Count number of productions
    def count_productions (self):
        count = 0
        for arr in self.productions.values():
            count += len(arr)
        return count 

    # Generate $limit values to test; using leftmost derivations only
    def generate_values (self, limit):
        q = queue.PriorityQueue()
        q.put((1,[self.start]))
        output = []
        while len(output) < limit and not q.empty():
            next = q.get()[1]
            contains_var = False
            i = 0
            while (i < len(next) and not contains_var):
                part = next[i]
                if (part in self.variables):
                    contains_var = True
                    for production in self.productions[part]:
                        new_array = next[0:i] + production + next[i+1:]
                        new_tuple = (len(new_array) + random.random(), new_array)
                        q.put(new_tuple)
                else:
                    assert part in self.alphabet

                i += 1

            if (not contains_var):
                output.append(concat_string_array(next))
        # output.sort()
        return output

    # # Generate some values to test; using leftmost derivations only; assuming flimsy CFG
    # def generate_flimsy_values (self, limit):
    #     q = queue.PriorityQueue()
    #     q.put((1,[self.start]))
    #     flimsy_numbers = set()
    #     while len(flimsy_numbers) < limit and not q.empty():
    #         next = q.get()[1]
    #         contains_var = False
    #         i = 0
    #         while (i < len(next) and not contains_var):
    #             part = next[i]
    #             if (part in self.variables):
    #                 contains_var = True
    #                 for production in self.productions[part]:
    #                     new_array = next[0:i] + production + next[i+1:]
    #                     new_tuple = (len(new_array) + random.random(), new_array)
    #                     q.put(new_tuple)
    #             else:
    #                 assert part in self.alphabet
    #             i += 1

    #         if (not contains_var):
    #             x = ''
    #             for a in next[::-1]:    # concatenate symbols in reverse order
    #                 x += a
    #             x = int(x,2) # convert to integer
    #             assert (x not in flimsy_numbers) # confirm that x doesn't have multiple derivations
    #             flimsy_numbers.add(x)
    #             if (b_count(x) <= b_count(3*x)): # confirm that x is 3-flimsy
    #                 print(x)
    #                 assert (False)

    #     del q
    #     flimsy = []
    #     for n in flimsy_numbers:
    #         flimsy.append(n)
    #     flimsy.sort()
    #     return flimsy

    # Convert CFG to PDA
    def to_PDA (self):
        # TODO: Write this
        return

    # A helper function to make variable names more readable (i.e. V_i) and compatible with Maple and LaTeX
    def _pretty_names_ (self):
        nice_names = {self.start : "S"}
        V = [self.start]
        for v in self.variables:
            if v != self.start:
                nice_names[v] = "V_" + str(len(V))
                V.append(v)
        return (nice_names, V)

    # Print CFG in "nice" form
    def to_string_array (self):
        (nice_names, V) = self._pretty_names_()
        output = []
        for i in range (len(V)):
            s = nice_names[V[i]] + "\t->\t"
            for prod_list in self.productions[V[i]]:
                for prod in prod_list:
                    if prod in self.alphabet:
                        if prod == EMPTY_STRING:
                            s += "_"
                        else:
                            s += prod
                    else:
                        assert prod in self.variables
                        s += nice_names[prod]
                    s += ' '
                s += "| "
            output.append(s[:-3]) # remove the last three characters (should be an extra " | ")
        return output

    # Convert CFG to Maple code for analysis
    def to_Maple (self):
        (nice_names, V) = self._pretty_names_()
        output = ["eqs := ["]
        for i in range (len(V)):
            s = '-' + nice_names[V[i]] + ' + '
            for p in self.productions[V[i]]:
                for x in p:
                    if x in self.alphabet:
                        if x == EMPTY_STRING:
                            s += "1*"
                        else:
                            s += "x*"
                    else:
                        assert x in self.variables
                        s += nice_names[x]+"*"
                s = s[:-1] + " + " # remove the last '*'
            output.append(s[:-3] + ",") # remove the last three characters (should be an extra " + ")
        output[-1] = output[-1][:-1] # remove the last ','
        output.append("]:")

        s = "Groebner[Basis](eqs, lexdeg(["
        for i in range (1, len(V)):
            s += nice_names[V[i]] + ", "
        if (len(V) > 1):
            s = s[:-2] + "], [" # Remove the last ", "
        s += nice_names[V[0]] + "])):"
        output.append(s)

        output.append("algeq := %[1]:")
        output.append("assume(x, positive):")
        # output.append("map(series, [solve(algeq, "+nice_names[self.start]+")], x);")
        output.append("f := solve(algeq, "+nice_names[self.start]+"):")
        output.append("ps := f[1]; # You may need to change the value in here to get the correct root.")
        output.append("series(ps, x, 41);")
        
        lib_path = '"/u3/twaclokie/Flimsy/PDAWESOME/maple_files"'
        output.append("libname := "+lib_path+",libname:")
        output.append("combine(equivalent(ps, x, n, 1));")
        output.append("combine(equivalent(ps, x, n, 2));")
        output.append("combine(equivalent(ps, x, n, 3));")
        output.append("combine(equivalent(ps, x, n, 4));")
        output.append("combine(equivalent(ps, x, n, 5));")

        return output
