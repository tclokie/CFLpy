states = {'-0', '-1', '-2', '+2', '+1(1)', '+1(10)', '+0(100)', '+0(10)', '+0(000)', 'END'}
alphabet = {'0', '1'}
stack_alphabet = {'Z', 'X'}
start_state = '-0'
start_stack = ['Z']
delta = {
    ('-0', '0', 'Z'): ('-0', 'Z'),
    ('-0', '0', 'X'): ('-0', 'X'),
    ('-0', '1', 'Z'): ('-1', 'Z'),
    ('-0', '1', 'X'): ('-1', 'X'),
    ('-1', '0', 'Z'): ('-0', 'XZ'),
    ('-1', '0', 'X'): ('-0', 'XX'),
    ('-1', '1', 'Z'): ('+2', 'Z'),
    ('-1', '1', 'X'): ('-2', ''),
    ('-2', '0', 'Z'): ('-1', 'Z'),
    ('-2', '0', 'X'): ('-1', 'X'),
    ('-2', '1', 'Z'): ('-2', 'Z'),
    ('-2', '1', 'X'): ('-2', 'X'),
    ('+2', '0', 'Z'): ('+1(10)', 'Z'),
    ('+2', '0', 'X'): ('+1(10)', 'X'),
    ('+2', '1', 'Z'): ('+2', 'Z'),
    ('+2', '1', 'X'): ('+2', 'X'),
    ('+1(10)', '0', 'Z'): ('-0', 'Z'),
    ('+1(10)', '0', 'X'): ('+0(100)', ''),
    ('+1(10)', '1', 'Z'): ('+2', 'XZ'),
    ('+1(10)', '1', 'X'): ('+2', 'XX'),
    ('+1(1)', '0', 'Z'): ('-0', 'Z'),
    ('+1(1)', '0', 'X'): ('+0(10)', ''),
    ('+1(1)', '1', 'Z'): ('+2', 'XZ'),
    ('+1(1)', '1', 'X'): ('+2', 'XX'),
    ('+0(000)', '0', 'Z'): ('+0(000)', 'Z'),
    ('+0(000)', '0', 'X'): ('+0(000)', 'X'),
    ('+0(000)', '1', 'Z'): ('+1(1)', 'Z'),
    ('+0(000)', '1', 'X'): ('+1(1)', 'X'),
    ('+0(10)', '0', 'Z'): ('+0(100)', 'Z'),
    ('+0(10)', '0', 'X'): ('+0(100)', 'X'),
    ('+0(10)', '1', 'Z'): ('+1(1)', 'Z'),
    ('+0(10)', '1', 'X'): ('+1(1)', 'X'),
    ('+0(100)', '0', 'Z'): ('+0(000)', 'Z'),
    ('+0(100)', '0', 'X'): ('+0(000)', 'X'),
    ('+0(100)', '1', 'Z'): ('+1(1)', 'Z'),
    ('+0(100)', '1', 'X'): ('+1(1)', 'X'),
    ('+0(100)', '', 'Z'): ('END', ''),
    ('+0(100)', '', 'X'): ('END', ''),
    ('END', '', 'Z'): ('END', ''),
    ('END', '', 'X'): ('END', '')
}


'''
def d(q, a, A): # a is '0' or '1', A is 'Z' or 'X'
    if (q == '-0'):
        if (a == '0'):
            return (q, A)
        else:
            return ('-1', A)
    elif (q == '-1'):
        if (a == '0'):
            return ('-0', 'X'+A)
        else:
            if (A == 'Z'):
                return ('+2', A)
            else:
                return ('-2')
'''

V = set()
P = {}

for q in states:
    for A in stack_alphabet:
        for p in states:
            V.add((q,A,p))

S = ('-0', 'Z', 'END')
print(V.__contains__(S))

# Instantiate P
for v in V:
    P[v] = []

# Fill in P
for q in states:
    for a in ['0', '1', '']:
        for A in stack_alphabet:
            if (delta.__contains__((q, a, A))):
                (q_1, B) = delta[(q,a,A)]
                m = len(B)
                if (m == 0):
                    P[q,A,q_1].append([a])
                elif (m == 1):
                    B_1 = B[0]
                    for q_2 in states:
                        P[q,A,q_2].append([a, (q_1, B_1, q_2)])
                elif (m == 2):
                    B_1 = B[0]
                    B_2 = B[1]
                    for q_2 in states:
                        for q_3 in states:
                            P[q,A,q_3].append([a, (q_1, B_1, q_2), (q_2, B_2, q_3)])
                else:
                    print("SANITY CHECK FAILED")
                    break

# Eliminate dead production rules
flag = True
while (flag):
    print("DELETING...")
    flag = False
    to_remove_from_V = []
    to_remove_from_P = []
    for v in V:
        if (P[v] == []):
            flag = True
            to_remove_from_V.append(v)
    
    for v in to_remove_from_V:
        print('\t', v)
        V.remove(v)
        del P[v]
        for (left, right) in P.items():
            for production in right:
                if (production.__contains__(v)):
                    print('\t\t', left, '\t', production)
                    to_remove_from_P.append((right, production))
    
    for (right, production) in to_remove_from_P:
        right.remove(production)

