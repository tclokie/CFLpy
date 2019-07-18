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







# Make a CFG

V = set()
P = {}
S = ('-0', 'Z', 'END')

# Create V: set of variables
for q in states:
    for A in stack_alphabet:
        for p in states:
            V.add((q, A, p))

assert (S in V) # Sanity check

# Instantiate P: set of productions
for v in V:
    P[v] = []

# Fill in P
for q in states:
    for a in alphabet:
        for A in stack_alphabet:
            if ((q, a, A) in delta):
                for (q_1, B) in delta[(q, a, A)]:
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



# using DFS, return set of variables reachable from parameter
def find_reachable_vars (start):
    seen = {start}
    stack = [start]
    while (len(stack) > 0):
        current = stack.pop()
        goes_to = P[current]
        for var in goes_to:
            for i in range (1, len(var)):
                next = var[i]
                if (not next in seen):
                    seen.add(next)
                    stack.append(next)
    return seen


# Eliminate dead production rules
flag = True
while (flag):
    count = 0
    for p in P.values():
        count += len(p)
    #print(len(V), 'variables, and', count, 'production rules')
    
    #print("DELETING...")
    flag = False
    to_remove_from_V = set()
    to_remove_from_P = []
    reachable_vars = find_reachable_vars(S)
    for v in V:
        if (P[v] == [] or (not v in reachable_vars)):
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
        right.remove(production)



















# Print code for Maple: Groebner Basis

names = {S: "S", '': '1', '0':'x', '1': 'x'}

arr = [('-2', 'Z', 'END'),
('-1', 'Z', 'END'),
('+0', 'X', 'END'),
('+0', 'X', '+0'),
('+2', 'X', '+0'),
('+2', 'X', 'END'),
('+1', 'X', 'END'),
('+2', 'Z', 'END'),
('+0', 'X', '-2'),
('-2', 'X', '-2'),
('-0', 'X', 'END'),
('+1', 'X', '+0'),
('+1', 'Z', 'END'),
('-0', 'X', '+0'),
('-2', 'X', '+0'),
('-1', 'X', '+0'),
('-1', 'X', 'END'),
('-1', 'X', '-2'),
('+1', 'X', '-2'),
('+0', 'Z', 'END'),
('+2', 'X', '-2'),
('-2', 'X', 'END'),
('-0', 'X', '-2'),
('-0', 'X', '+2'),
('-1', 'X', '+1'),
('-1', 'X', '+2'),
('+0', 'X', '-1'),
('+0', 'X', '+1'),
('-2', 'X', '+2'),
('+1', 'X', '+2'),
('-1', 'X', '-0'),
('+0', 'X', '-0'),
('-1', 'X', '-1'),
('-0', 'X', '-0'),
('+2', 'X', '-1'),
('-0', 'X', '+1'),
('END', 'Z', 'END'),
('-2', 'X', '-0'),
('-0', 'X', '-1'),
('+1', 'X', '-1'),
('END', 'X', 'END'),
('+0', 'X', '+2'),
('+1', 'X', '+1'),
('-2', 'X', '+1'),
('-2', 'X', '-1'),
('+2', 'X', '-0'),
('+1', 'X', '-0'),
('+2', 'X', '+2'),
('+2', 'X', '+1')]

for v in V:
    if v != S:
        assert (v in arr)
        counter = arr.index(v)
        names[v] = "V_"+str(counter)
        counter += 1
        print(names[v], ":=", v)
print("\n\n\n")

print('eqs := [')
for v in V:
    print('-' + names[v], end='')
    for ps in P[v]:
        print(' + ', end='')
        for j in range(len(ps)):
            p = ps[j]
            if (j > 0):
                print('*', end='')
            print(names[p], end='')
    print(', ') # NOTE: manually remove the last comma
print('];')

print('Groebner[Basis](eqs, lexdeg([', end='')
for i in range(len(arr)):
    print('V_'+str(i), end=', ') # NOTE: manually remove the last comma
print('], [S]));')

print("algeq := %[1];")
#print("map(series, [solve(algeq, S)], x);")

'''     Test validity of CFG by generating samples:

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
while (len(flimsy_numbers) < 8192 and not q.empty()):
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
