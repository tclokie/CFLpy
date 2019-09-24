import queue
import random


def int_to_bin(x):
    return x.__format__('b')

def b_count(x):
    return int_to_bin(x).count('1')

def is_k_flimsy(x, k):
    return b_count(x) > b_count(k*x)







class PDA:
    '''Pushdown Automata'''
    def __init__ (self, states, alphabet, stack_alphabet, start_state, start_stack, transitions):
        self.states = states
        self.alphabet = alphabet
        self.stack_alphabet = stack_alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.start_stack = start_stack # assume list of length 1

    def to_CFG (self):
        # return CFG(self)
        cfg = CFG()
        cfg.init_variables(self)
        cfg.add_to_alphabet(self.alphabet)
        cfg.set_start_variable((self.start_state, self.start_stack[0], 'END')) # TODO: Generalize this!
        cfg.init_productions()
        cfg.populate_productions(self)
        cfg.eliminate_useless_productions()
        return cfg






class CFG:
    '''Context-Free Grammar'''
    # Default constructor; creates empty CFG
    def __init__ (self):
        self.variables = set()
        self.alphabet = {""}
        self.productions = dict()
        self.start = "" # MUST BE a member of {variables}

    # def __init__(self, pda): # Constructor that takes PDA as input
    #     self = pda.to_CFG()

    # Create V: set of variables from PDA
    def init_variables (self, pda):
        self.variables = set()
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

    # Create S: start variable
    def set_start_variable (self, start):
        assert (start in self.variables)
        self.start = start


    # Instantiate P: set of productions given a set of variables
    def init_productions (self):
        self.productions = dict()
        for v in self.variables:
            self.productions[v] = []

    # Fill in P
    def populate_productions (self, pda):
        for q in pda.states:
            for a in pda.alphabet:
                for A in pda.stack_alphabet:
                    if ((q, a, A) in pda.transitions):
                        for (q_1, B) in pda.transitions[(q, a, A)]: # Generalize this part!
                            m = len(B)
                            if (m == 0):
                                self.productions[(q, A, q_1)].append([a])
                            elif (m == 1):
                                B_1 = B[0]
                                for q_2 in pda.states:
                                    self.productions[(q, A, q_2)].append([a, (q_1, B_1, q_2)])
                            else:
                                assert (m == 2) # Sanity check
                                B_1 = B[0]
                                B_2 = B[1]
                                for q_2 in pda.states:
                                    for q_3 in pda.states:
                                        self.productions[(q, A, q_3)].append([a, (q_1, B_1, q_2), (q_2, B_2, q_3)])

    # using DFS, return set of variables reachable from parameter
    def find_reachable_vars (self):
        seen = {self.start}
        stack = [self.start]
        while (len(stack) > 0):
            current = stack.pop()
            goes_to = self.productions[current]
            for var in goes_to:
                for i in range (1, len(var)):
                    next = var[i]
                    if (not next in seen):
                        seen.add(next)
                        stack.append(next)
        return seen

    # using DFS, return set of variables that can produce an all-terminal string
    def rfind_reachable_vars (self):
        good = set()
        for v in self.productions.keys():
            for w in self.productions[v]:
                if (len(w) < 2): # w has a production of just a terminal
                    assert (len(w) == 1)
                    if not (w[0] in self.alphabet):
                        print("ERROR REACHED")
                        print(w[0])
                        print(w)
                        print(self.alphabet)
                        assert(False)
                    good.add(v)
                    print('\t\t', v)
        change = True    
        while (change): # Find variables that lead to such productions
            change = False
            for v in self.productions.keys():
                if (not v in good): # don't revisit variables
                    for v_p in self.productions[v]: # v_p is a single production of v
                        flag = True
                        for p in v_p: # p is either a variable or a terminal
                            if ((not p in self.alphabet) and (not p in good)):
                                flag = False
                        if flag:
                            good.add(v)
                            change = True
                            print('\t\t\t', v)
        return good


    # Eliminate dead production rules
    def eliminate_useless_productions (self):
        flag = True
        while (flag):
            count = 0
            for p in self.productions.values():
                count += len(p)
            print(len(self.variables), 'variables, and', count, 'production rules')
            
            print("DELETING...")
            flag = False
            to_remove_from_V = set()
            to_remove_from_P = []
            reachable_vars = self.find_reachable_vars()
            produceable_vars = self.rfind_reachable_vars()
            for v in self.variables:
                if (len(self.productions[v]) == 0 or (not v in reachable_vars) or (not v in produceable_vars)):
                    flag = True
                    to_remove_from_V.add(v)
            
            for v in to_remove_from_V:
                #print('\t', v)
                self.variables.remove(v)
                del self.productions[v]
                for (left, right) in self.productions.items():
                    for production in right:
                        if (v in production):
                            #print('\t\t', left, '\t', production)
                            to_remove_from_P.append((right, production))
            
            for (right, production) in to_remove_from_P:
                if (production in right):
                    right.remove(production)




    # def generate_CFG_from_PDA (self, pda):
    #     return CFG(pda)



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
                output.append(next)
        return output

    # Generate some values to test; using leftmost derivations only
    def generate_flimsy_values (self, limit):
        q = queue.PriorityQueue()
        q.put((1,[self.start]))
        flimsy_numbers = set()
        while len(flimsy_numbers) < limit and not q.empty():
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
                x = ''
                for a in next[::-1]:    # concatenate symbols in reverse order
                    x += a
                x = int(x,2) # convert to integer
                assert (x not in flimsy_numbers) # confirm that x doesn't have multiple derivations
                flimsy_numbers.add(x)
                if (b_count(x) <= b_count(3*x)): # confirm that x is 3-flimsy
                    print(x)
                    assert (False)

        del q
        flimsy = []
        for n in flimsy_numbers:
            flimsy.append(n)
        flimsy.sort()
        return flimsy





def create_palindrome_pda ():
    states = {"S", "END"}
    alphabet = {'', 'a', 'b'}
    stack_alphabet = {'Z','a','b'}
    start_state = "S"
    start_stack = ['Z']
    delta = {
        ('S', 'a', 'Z'): [('S', 'aZ'), ('END', 'Z')],
        ('S', 'a', 'a'): [('S', 'aa'), ('END', 'a')],
        ('S', 'a', 'b'): [('S', 'ab'), ('END', 'b')],
        ('S', 'b', 'Z'): [('S', 'bZ'), ('END', 'Z')],
        ('S', 'b', 'a'): [('S', 'ba'), ('END', 'a')],
        ('S', 'b', 'b'): [('S', 'bb'), ('END', 'b')],
        ('S', '', 'Z'): [('END', 'Z')],
        ('S', '', 'a'): [('END', 'a')],
        ('S', '', 'b'): [('END', 'b')],
        ('END', '', 'Z'): [('END', '')],
        ('END', 'a', 'a'): [('END', '')],
        ('END', 'b', 'b'): [('END', '')]
    }
    return PDA(states, alphabet, stack_alphabet, start_state, start_stack, delta)


def create_flimsy_PDA (k): # Only works for k=3 so far
    assert (k == 3)
    states = {'-0', '-1', '-2', '+2', '+1', '+0', 'END'}
    alphabet = {'0', '1', ''}
    stack_alphabet = {'Z', 'X'}
    start_state = '-0'
    start_stack = ['Z']
    delta = {
        ('-0', '0', 'Z'): [('-0',  'Z')],
        ('-0', '0', 'X'): [('-0',  'X')],
        ('-0', '1', 'Z'): [('-1',  'Z')],
        ('-0', '1', 'X'): [('-1',  'X')],
        ('-1', '0', 'Z'): [('-0', 'XZ')],
        ('-1', '0', 'X'): [('-0', 'XX')],
        ('-1', '1', 'Z'): [('+2',  'Z')],
        ('-1', '1', 'X'): [('-2',   '')],
        ('-2', '0', 'Z'): [('-1',  'Z')],
        ('-2', '0', 'X'): [('-1',  'X')],
        ('-2', '1', 'Z'): [('-2',  'Z')],
        ('-2', '1', 'X'): [('-2',  'X')],
        ('+2', '0', 'Z'): [('+1',  'Z')],
        ('+2', '0', 'X'): [('+1',  'X')],
        ('+2', '1', 'Z'): [('+2',  'Z')],
        ('+2', '1', 'X'): [('+2',  'X'), ('END', '')],
        ('+1', '0', 'Z'): [('-0',  'Z')],
        ('+1', '0', 'X'): [('+0',   '')],
        ('+1', '1', 'Z'): [('+2', 'XZ'), ('END', '')],
        ('+1', '1', 'X'): [('+2', 'XX'), ('END', '')],
        ('+0', '0', 'Z'): [('+0',  'Z')],
        ('+0', '0', 'X'): [('+0',  'X')],
        ('+0', '1', 'Z'): [('+1',  'Z')],
        ('+0', '1', 'X'): [('+1',  'X'), ('END', '')],
        ('END', '', 'Z'): [('END', '')],
        ('END', '', 'X'): [('END', '')]
    }
    return PDA(states, alphabet, stack_alphabet, start_state, start_stack, delta)


def find_first_k_flimsies (k, limit): # Finds the k-flimsy integers in [1..limit]
    output = []
    for i in range (1, limit):
        if (is_k_flimsy(i,k)):
            output.append(i)
    return output




# Make a PDA for 3-flimsy numbers
pda = create_flimsy_PDA (3)

# Turn it into a CFG
cfg = pda.to_CFG()

print(cfg.variables, '\n')
print(cfg.productions, '\n')
print(cfg.start, '\n')
print(cfg.alphabet)






pal_pda = create_palindrome_pda()
pal_cfg = pal_pda.to_CFG()
pals = pal_cfg.generate_values(100)
for p in pals:
    x = ''
    for a in p:
        x += a
    print(x)



cfg_output = cfg.generate_flimsy_values(100000)
assert(len(cfg_output) > 10000)

correct_output = find_first_k_flimsies(3, 10000)

for i in range (len(correct_output)):
    if cfg_output[i] != correct_output[i]:
        print (i, "\t", cfg_output[i], "!=", correct_output[i])
        break
print("DONE")

'''
f = open("new_flimsy_CFG_generated.txt", 'w')
for n in cfg_output:
    f.write(str(n) + '\n')
f.close()
'''