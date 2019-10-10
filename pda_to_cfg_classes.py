import queue
import random
import math
import sys

def int_to_bin(x):
    return x.__format__('b')

def bin_to_int(s):
    return int(s, 2) # interpret s as an int in base 2

def b_count(x):
    return int_to_bin(x).count('1')

def is_k_flimsy(x, k):
    return b_count(x) > b_count(k*x)

def reverse_string (s):
    return s[::-1]

def concat_string_array (A):
    result = ''
    for a in A:
        result += a
    return result

def print_array (A):
    for a in A:
        print(a)





class PDA:
    '''Pushdown Automata (accepting on empty stack only)'''
    def __init__ (self, states, alphabet, stack_alphabet, start_state, start_stack, transitions, accept_state):
        self.states = states
        self.alphabet = alphabet
        self.stack_alphabet = stack_alphabet
        self.start_state = start_state
        self.accept_state = accept_state # The ONLY accepting state; stops reading and pops whole stack
        self.start_stack = start_stack # assume list of length 1
        self.transitions = transitions # here the top of the stack is on the RIGHT of the stack_after string
        # TODO: verify that there are no infinite epsilon loops

    def to_CFG (self):
        # return CFG(self)
        cfg = CFG()
        cfg.init_variables(self)
        cfg.add_to_alphabet(self.alphabet)
        cfg.set_start_variable((self.start_state, self.start_stack[0], self.accept_state)) # TODO: Generalize this!
        cfg.init_productions()
        cfg.populate_productions(self)
        cfg.eliminate_useless_productions()
        return cfg

    def simulate (self, x): # boolean: does this PDA accept input x?
        return self._simulate_(self.start_state, self.start_stack[0], x)

    def _simulate_ (self, current_state, current_stack, x): # takes current stack as string with top as right
        if current_stack == '':
            return x == ""

        if (len(x) > 0):
            key = (current_state, x[0], current_stack[-1])
            if (key in self.transitions):
                next_steps = self.transitions[key]
                for (new_state, new_stack) in next_steps:
                    if self._simulate_(new_state, current_stack[0:-1]+new_stack, x[1:]):
                        return True

        key = (current_state, '', current_stack[-1])
        if (key in self.transitions):
            next_epsilon_steps = self.transitions[key]
            for (new_state, new_stack) in next_epsilon_steps:
                if self._simulate_(new_state, current_stack[0:-1]+new_stack, x):
                    return True

        return False

    def output_gv (self):
        # TODO: return valid output for .gv dot file
        return ""












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
                                B_1 = B[1]
                                B_2 = B[0]
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
            for prod_list in goes_to:
                for i in range (1, len(prod_list)): # TODO: How does this work? I don't remember
                    next = prod_list[i]
                    # if type(next) == list:
                    #     print(next)
                    #     print(prod_list[i])
                    #     print(prod_list)
                    if (next in self.variables) and (not next in seen):
                        seen.add(next)
                        stack.append(next)
        return seen

    # using DFS, return set of variables that can produce an all-terminal string
    def rfind_reachable_vars (self):
        good = set() # first, find the set of productions that have terminal-only outputs
        for v in self.productions.keys():
            for w in self.productions[v]:
                all_terminals = True
                for x in w:
                    if (x in self.variables):
                        all_terminals = False
                    else:
                        assert (x in self.alphabet)
                if (all_terminals):
                    good.add(v)

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
                            # print('\t\t\t', v)
        return good


    # Eliminate dead production rules
    def eliminate_useless_productions (self):
        flag = True
        while (flag): # Now iterate through, removing all bad variables
            flag = False
            to_remove_from_V = set()
            to_remove_from_P = []

            reachable_vars = self.find_reachable_vars()
            produceable_vars = self.rfind_reachable_vars()
            for v in self.variables:
                if (len(self.productions[v]) == 0 or (not v in reachable_vars) or (not v in produceable_vars)):
                    to_remove_from_V.add(v)
                    flag = True

            # remove useless variables,
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

            del to_remove_from_V
            del to_remove_from_P

            vars_to_replace = {}

            # now we simplify variables with exactly one production
            for v in self.variables:
                if len(self.productions[v]) == 1: # replace instances of v with P[v]
                    vars_to_replace[v] = self.productions[v][0]
                    flag = True
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
            # TODO: check that this is safe?


            # now we remove empty strings from non-empty productions; combine multiple empties into one
            for prod_list in self.productions.values():
                for production in prod_list:
                    empty_indices = []
                    for i in range (len(production)):
                        if production[i] == '':
                            empty_indices.insert(0,i) # prepend
                    for i in empty_indices:
                        production.pop(i)
                    if len(production) == 0:
                        production.append('')




    # Count number of variables
    def count_variables (self):
        return len(self.variables)

    # Count number of productions
    def count_productions (self):
        count = 0
        for arr in self.productions.values():
            count += len(arr)
        return count 

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

    # Convert CFG to PDA
    def to_PDA (self):
        # TODO: Write this
        return

    # A helper function to make variable names "pretty" (i.e. V_i)
    def _pretty_names_ (self):
        nice_names = {self.start : "V_0"}
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
            for p in self.productions[V[i]]:
                for x in p:
                    if x in self.alphabet:
                        if x == "":
                            s += "_"
                        else:
                            s += x
                    else:
                        assert x in self.variables
                        s += nice_names[x]
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
                        if x == "":
                            s += "1*"
                        else:
                            s += "x*"
                    else:
                        assert x in self.variables
                        s += nice_names[x]+"*"
                s = s[:-1] + " + " # remove the last '*'
            output.append(s[:-3] + ",") # remove the last three characters (should be an extra " + ")
        output[-1] = output[-1][:-1] # remove the last ','
        output.append("];")

        s = "Groebner[Basis](eqs, lexdeg(["
        for i in range (1, len(V)):
            s += nice_names[V[i]] + ", "
        if (len(V) > 1):
            s = s[:-2] + "], [" # Remove the last ", "
        s += nice_names[V[0]] + "]));"
        output.append(s)

        output.append("algeq := %[1];")
        output.append("map(series, [solve(algeq, "+nice_names[self.start]+")], x);")
        output.append("f := solve(algeq, "+nice_names[self.start]+");")
        output.append("ps := f[1];")
        output.append("series(ps, x, 40);")

        return output

'''
eqs:=[];
Groebner[Basis](eqs, lexdeg([V_A, V_B, V_C, V_D, V_E, V_F, V_G, V_H,
V_I, V_J, V_K, V_L, V_M, V_N], [S]));
algeq := %[1];
map(series, [solve(algeq, S)], x);
f := solve(algeq,S);
ps := f[1];
series(ps, x, 40);
libname:="<insert library name>",libname:
combine(equivalent(ps,x,n,5));
'''






def create_palindrome_PDA ():
    states = {'S', 'END'}
    alphabet = {'', 'a', 'b'}
    stack_alphabet = {'Z','a','b'}
    start_state = 'S'
    final_state = 'END'
    start_stack = ['Z']
    delta = {
        ('S', 'a', 'Z'): [('S', 'Za'), ('END', 'Z')],
        ('S', 'a', 'a'): [('S', 'aa'), ('END', 'a')],
        ('S', 'a', 'b'): [('S', 'ba'), ('END', 'b')],
        ('S', 'b', 'Z'): [('S', 'Zb'), ('END', 'Z')],
        ('S', 'b', 'a'): [('S', 'ab'), ('END', 'a')],
        ('S', 'b', 'b'): [('S', 'bb'), ('END', 'b')],
        ('S', '', 'Z'): [('END', 'Z')],
        ('S', '', 'a'): [('END', 'a')],
        ('S', '', 'b'): [('END', 'b')],
        ('END', '', 'Z'): [('END', '')],
        ('END', 'a', 'a'): [('END', '')],
        ('END', 'b', 'b'): [('END', '')]
    }
    return PDA(states, alphabet, stack_alphabet, start_state, start_stack, delta, final_state)


def create_equal_as_bs_PDA ():
    states = {'S', 'END'}
    alphabet = {'', 'a', 'b'}
    stack_alphabet = {'Z','a'}
    start_state = 'S'
    final_state = 'END'
    start_stack = ['Z']
    delta = {
        ('S', '', 'Z'): [('END', '')],
        ('S', 'a', 'Z'): [('S', 'Za')],
        ('S', 'a', 'a'): [('S', 'aa')],
        ('S', 'b', 'a'): [('END', '')],
        ('END', '', 'Z'): [('END', '')],
        ('END', 'b', 'a'): [('END', '')]
    }
    return PDA(states, alphabet, stack_alphabet, start_state, start_stack, delta, final_state)

def create_dyck_PDA (): # TODO: Test this
    states = {'S', 'END'}
    alphabet = {'', '(', ')'}
    stack_alphabet = {'Z', '('}
    start_state = 'S'
    final_state = 'END'
    start_stack = ['Z']
    delta = {
        ('S', '(', 'Z'): [('S', 'Z(')],
        ('S', '(', '('): [('S', '((')],
        ('S', ')', '('): [('S', '')],
        ('S', '', 'Z'): [('END', '')]
    }
    return PDA(states, alphabet, stack_alphabet, start_state, start_stack, delta, final_state)

# Create a PDA to accept all 3-flimsy binary numbers
def create_3flimsy_PDA ():
    states = {'-0', '-1', '-2', '+2', '+1', '+0', 'END'}
    alphabet = {'0', '1', ''}
    stack_alphabet = {'Z', 'X'}
    start_state = '-0'
    final_state = 'END'
    start_stack = ['Z']
    delta = {
        ('-0', '0', 'Z'): [('-0',  'Z')],
        ('-0', '0', 'X'): [('-0',  'X')],
        ('-0', '1', 'Z'): [('-1',  'Z')],
        ('-0', '1', 'X'): [('-1',  'X')],
        ('-1', '0', 'Z'): [('-0', 'ZX')],
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
        ('+1', '1', 'Z'): [('+2', 'ZX'), ('END', '')],
        ('+1', '1', 'X'): [('+2', 'XX'), ('END', '')],
        ('+0', '0', 'Z'): [('+0',  'Z')],
        ('+0', '0', 'X'): [('+0',  'X')],
        ('+0', '1', 'Z'): [('+1',  'Z')],
        ('+0', '1', 'X'): [('+1',  'X'), ('END', '')],
        ('END', '', 'Z'): [('END', '')],
        ('END', '', 'X'): [('END', '')]
    }
    return PDA(states, alphabet, stack_alphabet, start_state, start_stack, delta, final_state)

def create_3flimsy_PDA_alternate ():
    states = {'-0', '-1', '-2', '+2', '+1', '+0', 'END_0', 'END_1'}
    alphabet = {'0', '1', ''}
    stack_alphabet = {'Z', 'X'}
    start_state = '-0'
    final_state = 'END_0'
    start_stack = ['Z']
    delta = {
        ('-0', '0', 'Z'): [('-0',  'Z')],
        ('-0', '0', 'X'): [('-0',  'X')],
        ('-0', '1', 'Z'): [('-1',  'Z')],
        ('-0', '1', 'X'): [('-1',  'X')],
        ('-1', '0', 'Z'): [('-0', 'ZX')],
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
        ('+2', '1', 'X'): [('+2',  'X'), ('END_1', 'X')],
        ('+1', '0', 'Z'): [('-0',  'Z')],
        ('+1', '0', 'X'): [('+0',   '')],
        ('+1', '1', 'Z'): [('+2', 'ZX'), ('END_0', 'Z')],
        ('+1', '1', 'X'): [('+2', 'XX'), ('END_0', 'X')],
        ('+0', '0', 'Z'): [('+0',  'Z')],
        ('+0', '0', 'X'): [('+0',  'X')],
        ('+0', '1', 'Z'): [('+1',  'Z')],
        ('+0', '1', 'X'): [('+1',  'X'), ('END_1', 'X')],
        ('END_0', '', 'Z'): [('END_0', '')],
        ('END_0', '', 'X'): [('END_0', '')],
        ('END_1', '', 'X'): [('END_0', '')]
    }
    return PDA(states, alphabet, stack_alphabet, start_state, start_stack, delta, final_state)

# Create a PDA to accept all k-flimsy binary numbers
def create_flimsy_PDA (k): # Only works for k=3 so far
    assert (type(k) == int) and (k > 1) and (k % 2 == 1)
    states = {'END_0'}
    alphabet = {'0', '1', ''}
    stack_alphabet = {'Z', 'X'}
    start_state = '-0'
    final_state = 'END_0'
    start_stack = ['Z']
    delta = {('END_0', '', 'Z'): [('END_0', '')],
             ('END_0', '', 'X'): [('END_0', '')]}

    for carry in range (k):
        s = str(carry)
        states.add('-'+s)
        states.add('+'+s)
        for si in alphabet:
            if si != '':
                i = int(si)
                for z in stack_alphabet:
                    added = i*k + carry
                    new_kn_digit = added % 2
                    new_carry = str(added // 2)
                    if (new_kn_digit % 2 == i):
                        delta[('-'+s, si, z)] = [('-'+new_carry, z)]
                        delta[('+'+s, si, z)] = [('+'+new_carry, z)]
                    elif (new_kn_digit % 2 == 1):
                        assert (i == 0) # n goes up by 0, kn goes up by 1
                        delta[('-'+s, si, z)] = [('-'+new_carry, z+'X')]
                        if (z == 'X'):
                            delta[('+'+s, si, z)] = [('+'+new_carry, '')]
                        else:
                            delta[('+'+s, si, z)] = [('-'+new_carry, z)]
                    else:
                        assert (new_kn_digit % 2 == 0)
                        assert (i == 1)  # n goes up by 1, kn goes up by 0
                        delta[('+'+s, si, z)] = [('+'+new_carry, z+'X')]
                        if (z == 'X'):
                            delta[('-'+s, si, z)] = [('-'+new_carry, '')]
                        else:
                            delta[('-'+s, si, z)] = [('+'+new_carry, z)]

    # Add new end states
    # Transitions from END_{i+1} to END_{i} that read nothing but pop an X
    for i in range (int(math.log2(k))):
        new_state = 'END_'+str(i+1)
        states.add(new_state)
        one_less = 'END_'+str(i)
        delta[(new_state, '', 'X')] = [(one_less, '')]

    # 1-transitions that pop nothing from final states to END_x for some x?
    for carry in range (k):
        current_state = '+'+str(carry)
        required_pops = b_count(k+carry)-1
        delta[(current_state, '1', 'X')].append(('END_'+str(required_pops), 'X'))
        if required_pops == 0:
            delta[(current_state, '1', 'Z')].append(('END_'+str(required_pops), 'Z'))

    return PDA(states, alphabet, stack_alphabet, start_state, start_stack, delta, final_state)




def find_first_k_flimsies (k, limit): # Finds the k-flimsy integers in [1..limit]
    output = []
    for i in range (1, limit):
        if (is_k_flimsy(i,k)):
            output.append(i)
    return output





if (len(sys.argv) > 1) and (sys.argv):
    k = int(sys.argv[1])
    fname = "./maple_files/" + ("{:02d}".format(k)) + "_cfg.maple"

    pda = create_flimsy_PDA(k)
    cfg = pda.to_CFG()
    output = cfg.to_Maple() # String array

    f = open(fname, 'w')
    for line in output:
        f.write(line + '\n')
    f.close()

'''
k = 3
test = create_flimsy_PDA (k)
print(test.states)
print(test.alphabet)
print(test.stack_alphabet)
print(test.start_state)
print(test.start_stack)
for (left,right) in test.transitions.items():
    print(left, "->", right)
test_cfg = test.to_CFG()
print(test_cfg.variables)
print(test_cfg.alphabet)
print(test_cfg.start)
print_array(test_cfg.to_string_array())
gen = test_cfg.generate_values(10000)
A = []
for x in gen:
    y = bin_to_int(reverse_string(concat_string_array(x)))
    A.append(y)
    assert (is_k_flimsy(y, k))
A.sort()

B = find_first_k_flimsies (k, 1000)

for i in range (len(B)):
    assert A[i] == B[i]
'''

# for k in range (41, 90, 2):
#     cfg = create_flimsy_PDA(k).to_CFG()
#     print("For k =",k,"we have",cfg.count_variables(),"variables and",cfg.count_productions(),"productions.")


# flimsy3_pda = create_3flimsy_PDA_alternate()
# print("states:", flimsy3_pda.states == test.states)
# print("alphabet:", flimsy3_pda.alphabet == test.alphabet)
# print("stack_alphabet:", flimsy3_pda.stack_alphabet == test.stack_alphabet)
# print("start_state:", flimsy3_pda.start_state == test.start_state)
# print("start_stack:", flimsy3_pda.start_stack == test.start_stack)
# for (left,right) in flimsy3_pda.transitions.items():
#     if (test.transitions[left] != flimsy3_pda.transitions[left]):
#         print (left, "->", right)

'''
# Turn it into a CFG
cfg = pda.to_CFG()

print(cfg.variables, '\n')
print(cfg.productions, '\n')
print(cfg.start, '\n')
print(cfg.alphabet)
'''


'''
def test_all_strings (max_length, alphabet, pda, base):
    assert len(base) <= max_length
    print (base, "is a palindrome:", pal_pda.simulate(base))
    if (len(base) < max_length):
        for a in alphabet:
            if len(a) > 0:
                test_all_strings(max_length, alphabet, pda, base+a)

test_all_strings(5, ['a','b'], pal_pda, "")
'''
'''
pal_pda = create_palindrome_PDA()
pal_cfg = pal_pda.to_CFG()
pals = pal_cfg.generate_values(50)
for p in pals:
    x = ''
    for a in p:
        x += a
    print(x)
for s in pal_cfg.to_string_array():
    print(s)
for s in pal_cfg.to_Maple():
    print(s)
'''


'''
equal_cfg = create_equal_as_bs_PDA().to_CFG()
equal_as_bs = equal_cfg.generate_values(50)
for w in equal_as_bs:
    s = ''
    for a in w:
        s += a
    print(s)
for s in equal_cfg.to_string_array():
    print(s)
for s in equal_cfg.to_Maple():
    print(s)
'''

'''
cfg_output = cfg.generate_flimsy_values(100000)
assert(len(cfg_output) > 10000)

correct_output = find_first_k_flimsies(3, 10000)

for i in range (len(correct_output)):
    if cfg_output[i] != correct_output[i]:
        print (i, "\t", cfg_output[i], "!=", correct_output[i])
        break
print("DONE")
'''

'''
f = open("new_flimsy_CFG_generated.txt", 'w')
for n in cfg_output:
    f.write(str(n) + '\n')
f.close()
'''
