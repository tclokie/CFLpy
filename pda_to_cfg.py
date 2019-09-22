# Create V: set of variables
def init_variables (states, stack_alphabet):
    V = set()
    for q in states:
        for A in stack_alphabet:
            for p in states:
                V.add((q, A, p))
    return V


# Instantiate P: set of productions given a set of variables
def init_productions (variables):
    P = {}
    for v in variables:
        P[v] = []
    return P

# Fill in P
def populate_productions (states, alphabet, stack_alphabet, transitions, P):
    for q in states:
        for a in alphabet:
            for A in stack_alphabet:
                if ((q, a, A) in transitions):
                    for (q_1, B) in transitions[(q, a, A)]:
                        m = len(B)
                        if (m == 0):
                            P[(q, A, q_1)].append([a])
                        elif (m == 1):
                            B_1 = B[0]
                            for q_2 in states:
                                P[(q, A, q_2)].append([a, (q_1, B_1, q_2)])
                        else:
                            assert (m == 2) # Sanity check
                            B_1 = B[0]
                            B_2 = B[1]
                            for q_2 in states:
                                for q_3 in states:
                                    P[(q, A, q_3)].append([a, (q_1, B_1, q_2), (q_2, B_2, q_3)])
    return P


# using DFS, return set of variables reachable from parameter
def find_reachable_vars (start, productions):
    seen = {start}
    stack = [start]
    while (len(stack) > 0):
        current = stack.pop()
        goes_to = productions[current]
        for var in goes_to:
            for i in range (1, len(var)):
                next = var[i]
                if (not next in seen):
                    seen.add(next)
                    stack.append(next)
    return seen

# using DFS, return set of variables that can produce an all-terminal string
def rfind_reachable_vars (productions, alphabet):
    good = set()
    for v in productions.keys():
        for w in productions[v]:
            if (len(w) < 2): # w has a production of just a terminal
                assert (len(w) == 1)
                assert (w[0] in alphabet)
                good.add(v)
                print('\t\t', v)
    change = True    
    while (change): # Find variables that lead to such productions
        change = False
        for v in productions.keys():
            if (not v in good): # don't revisit variables
                for v_p in productions[v]: # v_p is a single production of v
                    flag = True
                    for p in v_p: # p is either a variable or a terminal
                        if ((not p in alphabet) and (not p in good)):
                            flag = False
                    if flag:
                        good.add(v)
                        change = True
                        print('\t\t\t', v)
    return good


# Eliminate dead production rules
def eliminate_useless_productions (V, alphabet, P, S):
    flag = True
    while (flag):
        count = 0
        for p in P.values():
            count += len(p)
        print(len(V), 'variables, and', count, 'production rules')
        
        print("DELETING...")
        flag = False
        to_remove_from_V = set()
        to_remove_from_P = []
        reachable_vars = find_reachable_vars(S, P)
        produceable_vars = rfind_reachable_vars(P, alphabet)
        for v in V:
            if (len(P[v]) == 0 or (not v in reachable_vars) or (not v in produceable_vars)):
                flag = True
                to_remove_from_V.add(v)
        
        for v in to_remove_from_V:
            #print('\t', v)
            V.remove(v)
            del P[v]
            for (left, right) in P.items():
                for production in right:
                    if (v in production):
                        #print('\t\t', left, '\t', production)
                        to_remove_from_P.append((right, production))
        
        for (right, production) in to_remove_from_P:
            if (production in right):
                right.remove(production)
    return (V, P)




def generate_CFG (states, alphabet, stack_alphabet, transitions, start_state, start_stack):
    V = init_variables(states, stack_alphabet)
    S = ('-0', 'Z', 'END')
    assert (S in V) # Sanity check

    P = init_productions(V)
    P = populate_productions(states, alphabet, stack_alphabet, transitions, P)
    (V, P) = eliminate_useless_productions(V, alphabet, P, S)
    return (V, alphabet, P, S)


# PDA info
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

# Turn it into a PDA
(V, alphabet, P, S) = generate_CFG(states, alphabet, stack_alphabet, delta, start_state, start_stack)


print(V)
print("\n")

print(P)
print("\n")

print(S)
print(alphabet)











'''
def int_to_bin(x):
    return x.__format__('b')

def b_count(x):
    return int_to_bin(x).count('1')


# Generate some values to test; using leftmost derivations only
import queue
import random
q = queue.PriorityQueue()
q.put((1,[S]))
flimsy_numbers = set()
while (len(flimsy_numbers) < 1048576 and not q.empty()):
    next = q.get()[1]
    contains_var = False
    i = 0
    while (i < len(next) and not contains_var):
        part = next[i]
        if (part in V):
            contains_var = True
            for production in P[part]:
                new_array = next[0:i] + production + next[i+1:]
                new_tuple = (len(new_array) + random.random(), new_array)
                q.put(new_tuple)
        else:
            assert part in alphabet
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

f = open("flimsy_CFG_generated.txt", 'w')
for n in flimsy:
    f.write(str(n) + '\n')
f.close()
'''