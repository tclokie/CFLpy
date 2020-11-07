from PDA import PDA
import math

EMPTY_STRING = ''


def int_to_bin(x):
    return x.__format__('b')


def s_2(x):
    return int_to_bin(x).count('1')


def base_b(n,b):
    s = EMPTY_STRING
    while n > 0:
        s += str(n % b)
        n //= b
    return s[::-1]

def s_b(n,b):
    count = 0
    while n > 0:
        count += n % b
        n //= b
    return count

# def is_k_flimsy(x, k):
#     return s_2(x) > s_2(k*x)

# def find_first_k_flimsy_numbers (k, limit): # Finds the k-flimsy integers in [1..limit]
#     output = []
#     for i in range (1, limit):
#         if (is_k_flimsy(i,k)):
#             output.append(i)
#     return output


def create_palindrome_PDA():
    states = {'S', 'END'}
    alphabet = {'', 'a', 'b'}
    stack_alphabet = {'Z', 'a', 'b'}
    start_state = 'S'
    start_stack = 'Z'
    transitions = {
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
    return PDA(states, alphabet, stack_alphabet, start_state, start_stack, transitions)


def create_even_palindrome_PDA():
    states = {'S', 'END'}
    alphabet = {'', 'a', 'b'}
    stack_alphabet = {'Z', 'a', 'b'}
    start_state = 'S'
    start_stack = 'Z'
    transitions = {
        ('S', 'a', 'Z'): [('S', 'aZ')],
        ('S', 'a', 'a'): [('S', 'aa')],
        ('S', 'a', 'b'): [('S', 'ab')],
        ('S', 'b', 'Z'): [('S', 'bZ')],
        ('S', 'b', 'a'): [('S', 'ba')],
        ('S', 'b', 'b'): [('S', 'bb')],
        ('S', '', 'Z'): [('END', 'Z')],
        ('S', '', 'a'): [('END', 'a')],
        ('S', '', 'b'): [('END', 'b')],
        ('END', '', 'Z'): [('END', '')],
        ('END', 'a', 'a'): [('END', '')],
        ('END', 'b', 'b'): [('END', '')]
    }
    return PDA(states, alphabet, stack_alphabet, start_state, start_stack, transitions)


def create_even_palindrome_PDA_alternate():
    states = {'q_0', 'q_1', 'q_2'}
    alphabet = {'a', 'b', ''}
    stack_alphabet = {'Z', 'a', 'b'}
    start_state = 'q_0'
    start_stack = 'Z'
    transitions = {
        ('q_0', 'a', 'Z'): [('q_0', 'aZ')],
        ('q_0', 'a', 'a'): [('q_0', 'aa')],
        ('q_0', 'a', 'b'): [('q_0', 'ab')],
        ('q_0', 'b', 'Z'): [('q_0', 'bZ')],
        ('q_0', 'b', 'a'): [('q_0', 'ba')],
        ('q_0', 'b', 'b'): [('q_0', 'bb')],
        ('q_0', '', 'Z'): [('q_1', 'Z')],
        ('q_0', '', 'a'): [('q_1', 'a')],
        ('q_0', '', 'b'): [('q_1', 'b')],
        ('q_1', 'a', 'a'): [('q_1', '')],
        ('q_1', 'b', 'b'): [('q_1', '')],
        ('q_1', '', 'Z'): [('q_2', '')]
    }
    return PDA(states, alphabet, stack_alphabet, start_state, start_stack, transitions)


def create_an_bn_PDA():
    states = {'S', 'END'}
    alphabet = {'', 'a', 'b'}
    stack_alphabet = {'Z', 'a'}
    start_state = 'S'
    start_stack = 'Z'
    transitions = {
        ('S', '', 'Z'): [('END', '')],
        ('S', 'a', 'Z'): [('S', 'aZ')],
        ('S', 'a', 'a'): [('S', 'aa')],
        ('S', 'b', 'a'): [('END', '')],
        ('END', '', 'Z'): [('END', '')],
        ('END', 'b', 'a'): [('END', '')]
    }
    return PDA(states, alphabet, stack_alphabet, start_state, start_stack, transitions)


def create_equal_as_bs_PDA():
    states = {'S', 'END'}
    alphabet = {'', 'a', 'b'}
    stack_alphabet = {'Z', 'a', 'b'}
    start_state = 'S'
    start_stack = 'Z'
    transitions = {
        ('S', '', 'Z'): [('END', '')],
        ('S', 'a', 'Z'): [('S', 'aZ')],
        ('S', 'a', 'a'): [('S', 'aa')],
        ('S', 'a', 'b'): [('S', '')],
        ('S', 'b', 'Z'): [('S', 'bZ')],
        ('S', 'b', 'a'): [('S', '')],
        ('S', 'b', 'b'): [('S', 'bb')]
    }
    return PDA(states, alphabet, stack_alphabet, start_state, start_stack, transitions)


def create_dyck_PDA():  # TODO: Test this
    states = {'S', 'END'}
    alphabet = {'', '(', ')'}
    stack_alphabet = {'Z', '('}
    start_state = 'S'
    start_stack = 'Z'
    transitions = {
        ('S', '(', 'Z'): [('S', '(Z')],
        ('S', '(', '('): [('S', '((')],
        ('S', ')', '('): [('S', '')],
        ('S', '', 'Z'): [('END', '')]
    }
    return PDA(states, alphabet, stack_alphabet, start_state, start_stack, transitions)

# For the language a^m b^n c^m
def create_am_bn_cm_PDA():
    states = {'q_0', 'q_1', 'q_2'}
    alphabet = {'', 'a', 'b', 'c'}
    stack_alphabet = {'Z', 'a'}
    start_state = 'q_0'
    start_stack = 'Z'
    transitions = {
        ('q_0', 'a', 'Z'): [('q_0', 'aZ')],
        ('q_0', 'a', 'a'): [('q_0', 'aa')],
        ('q_0', '', 'Z'): [('q_0', '')],
        ('q_0', 'b', 'Z'): [('q_1', 'Z')],
        ('q_0', 'b', 'a'): [('q_1', 'a')],
        ('q_0', 'c', 'a'): [('q_2', '')],
        ('q_1', 'b', 'Z'): [('q_1', 'Z')],
        ('q_1', 'b', 'a'): [('q_1', 'a')],
        ('q_1', '', 'Z'): [('q_1', '')],
        ('q_1', 'c', 'a'): [('q_2', '')],
        ('q_2', 'c', 'a'): [('q_2', '')],
        ('q_2', '', 'Z'): [('q_2', '')],
    }
    return PDA(states, alphabet, stack_alphabet, start_state, start_stack, transitions)


# Create a PDA to accept all 3-flimsy binary numbers
def create_3flimsy_PDA():
    states = {'-0', '-1', '-2', '+2', '+1', '+0', 'END'}
    alphabet = {'0', '1', ''}
    stack_alphabet = {'Z', 'X'}
    start_state = '-0'
    start_stack = 'Z'
    transitions = {
        ('-0', '0', 'Z'): [('-0', 'Z')],
        ('-0', '0', 'X'): [('-0', 'X')],
        ('-0', '1', 'Z'): [('-1', 'Z')],
        ('-0', '1', 'X'): [('-1', 'X')],
        ('-1', '0', 'Z'): [('-0', 'XZ')],
        ('-1', '0', 'X'): [('-0', 'XX')],
        ('-1', '1', 'Z'): [('+2', 'Z')],
        ('-1', '1', 'X'): [('-2', '')],
        ('-2', '0', 'Z'): [('-1', 'Z')],
        ('-2', '0', 'X'): [('-1', 'X')],
        ('-2', '1', 'Z'): [('-2', 'Z')],
        ('-2', '1', 'X'): [('-2', 'X')],
        ('+2', '0', 'Z'): [('+1', 'Z')],
        ('+2', '0', 'X'): [('+1', 'X')],
        ('+2', '1', 'Z'): [('+2', 'Z')],
        ('+2', '1', 'X'): [('+2', 'X'), ('END', '')],
        ('+1', '0', 'Z'): [('-0', 'Z')],
        ('+1', '0', 'X'): [('+0', '')],
        ('+1', '1', 'Z'): [('+2', 'XZ'), ('END', '')],
        ('+1', '1', 'X'): [('+2', 'XX'), ('END', '')],
        ('+0', '0', 'Z'): [('+0', 'Z')],
        ('+0', '0', 'X'): [('+0', 'X')],
        ('+0', '1', 'Z'): [('+1', 'Z')],
        ('+0', '1', 'X'): [('+1', 'X'), ('END', '')],
        ('END', '', 'Z'): [('END', '')],
        ('END', '', 'X'): [('END', '')]
    }
    return PDA(states, alphabet, stack_alphabet, start_state, start_stack, transitions)


def create_3flimsy_PDA_alternate():
    states = {'-0', '-1', '-2', '+2', '+1', '+0', 'END_0', 'END_1'}
    alphabet = {'0', '1', ''}
    stack_alphabet = {'Z', 'X'}
    start_state = '-0'
    start_stack = 'Z'
    transitions = {
        ('-0', '0', 'Z'): [('-0', 'Z')],
        ('-0', '0', 'X'): [('-0', 'X')],
        ('-0', '1', 'Z'): [('-1', 'Z')],
        ('-0', '1', 'X'): [('-1', 'X')],
        ('-1', '0', 'Z'): [('-0', 'XZ')],
        ('-1', '0', 'X'): [('-0', 'XX')],
        ('-1', '1', 'Z'): [('+2', 'Z')],
        ('-1', '1', 'X'): [('-2', '')],
        ('-2', '0', 'Z'): [('-1', 'Z')],
        ('-2', '0', 'X'): [('-1', 'X')],
        ('-2', '1', 'Z'): [('-2', 'Z')],
        ('-2', '1', 'X'): [('-2', 'X')],
        ('+2', '0', 'Z'): [('+1', 'Z')],
        ('+2', '0', 'X'): [('+1', 'X')],
        ('+2', '1', 'Z'): [('+2', 'Z')],
        ('+2', '1', 'X'): [('+2', 'X'), ('END_1', 'X')],
        ('+1', '0', 'Z'): [('-0', 'Z')],
        ('+1', '0', 'X'): [('+0', '')],
        ('+1', '1', 'Z'): [('+2', 'XZ'), ('END_0', 'Z')],
        ('+1', '1', 'X'): [('+2', 'XX'), ('END_0', 'X')],
        ('+0', '0', 'Z'): [('+0', 'Z')],
        ('+0', '0', 'X'): [('+0', 'X')],
        ('+0', '1', 'Z'): [('+1', 'Z')],
        ('+0', '1', 'X'): [('+1', 'X'), ('END_1', 'X')],
        ('END_0', '', 'Z'): [('END_0', '')],
        ('END_0', '', 'X'): [('END_0', '')],
        ('END_1', '', 'X'): [('END_0', '')]
    }
    return PDA(states, alphabet, stack_alphabet, start_state, start_stack, transitions)


def create_3equal_PDA():
    states = {'-0', '-1', '-2', '+2', '+1', '+0', 'END_0'}
    alphabet = {'0', '1', ''}
    stack_alphabet = {'Z', 'X'}
    start_state = '-0'
    start_stack = 'Z'
    transitions = {
        ('-0', '0', 'Z'): [('-0', 'Z')],
        ('-0', '0', 'X'): [('-0', 'X')],
        ('-0', '1', 'Z'): [('-1', 'Z')],
        ('-0', '1', 'X'): [('-1', 'X')],
        ('-1', '0', 'Z'): [('-0', 'XZ')],
        ('-1', '0', 'X'): [('-0', 'XX')],
        ('-1', '1', 'Z'): [('+2', 'Z'), ('END_0', '')],
        ('-1', '1', 'X'): [('-2', '')],
        ('-2', '0', 'Z'): [('-1', 'Z')],
        ('-2', '0', 'X'): [('-1', 'X')],
        ('-2', '1', 'Z'): [('-2', 'Z')],
        ('-2', '1', 'X'): [('-2', 'X')],
        ('+2', '0', 'Z'): [('+1', 'Z')],
        ('+2', '0', 'X'): [('+1', 'X')],
        ('+2', '1', 'Z'): [('+2', 'Z'), ('END_0', '')],
        ('+2', '1', 'X'): [('+2', 'X')],
        ('+1', '0', 'Z'): [('-0', 'Z')],
        ('+1', '0', 'X'): [('+0', '')],
        ('+1', '1', 'Z'): [('+2', 'XZ')],
        ('+1', '1', 'X'): [('+2', 'XX')],
        ('+0', '0', 'Z'): [('+0', 'Z')],
        ('+0', '0', 'X'): [('+0', 'X')],
        ('+0', '1', 'Z'): [('+1', 'Z'), ('END_0', '')],
        ('+0', '1', 'X'): [('+1', 'X')]
    }
    return PDA(states, alphabet, stack_alphabet, start_state, start_stack, transitions)


def create_5equal_PDA():
    states = {'-0', '-1', '-2', '-3', '-4', '+4', '+3', '+2', '+1', '+0', 'END_0', 'END_1'}
    alphabet = {'0', '1', ''}
    stack_alphabet = {'Z', 'X'}
    start_state = '-0'
    start_stack = 'Z'
    transitions = {
        ('+0', '0', 'X'): [('+0', 'X')],
        ('+0', '0', 'Z'): [('+0', 'Z')],
        ('+0', '1', 'X'): [('+2', 'X')],
        ('+0', '1', 'Z'): [('+2', 'Z'), ('END_0', 'Z')],
        ('+1', '0', 'X'): [('+0', '')],
        ('+1', '0', 'Z'): [('-0', 'Z')],
        ('+1', '1', 'X'): [('+3', 'XX')],
        ('+1', '1', 'Z'): [('+3', 'XZ'), ('END_0', 'Z')],
        ('+2', '0', 'X'): [('+1', 'X')],
        ('+2', '0', 'Z'): [('+1', 'Z')],
        ('+2', '1', 'X'): [('+3', 'X'), ('END_1', 'X')],
        ('+2', '1', 'Z'): [('+3', 'Z')],
        ('+3', '0', 'X'): [('+1', '')],
        ('+3', '0', 'Z'): [('-1', 'Z')],
        ('+3', '1', 'X'): [('+4', 'XX')],
        ('+3', '1', 'Z'): [('+4', 'XZ')],
        ('+4', '0', 'X'): [('+2', 'X')],
        ('+4', '0', 'Z'): [('+2', 'Z')],
        ('+4', '1', 'X'): [('+4', 'X')],
        ('+4', '1', 'Z'): [('+4', 'Z'), ('END_0', 'Z')],
        ('-0', '0', 'X'): [('-0', 'X')],
        ('-0', '0', 'Z'): [('-0', 'Z')],
        ('-0', '1', 'X'): [('-2', 'X')],
        ('-0', '1', 'Z'): [('-2', 'Z')],
        ('-1', '0', 'X'): [('-0', 'XX')],
        ('-1', '0', 'Z'): [('-0', 'XZ')],
        ('-1', '1', 'X'): [('-3', '')],
        ('-1', '1', 'Z'): [('+3', 'Z')],
        ('-2', '0', 'X'): [('-1', 'X')],
        ('-2', '0', 'Z'): [('-1', 'Z')],
        ('-2', '1', 'X'): [('-3', 'X')],
        ('-2', '1', 'Z'): [('-3', 'Z')],
        ('-3', '0', 'X'): [('-1', 'XX')],
        ('-3', '0', 'Z'): [('-1', 'XZ')],
        ('-3', '1', 'X'): [('-4', '')],
        ('-3', '1', 'Z'): [('+4', 'Z'), ('END_0', 'Z')],
        ('-4', '0', 'X'): [('-2', 'X')],
        ('-4', '0', 'Z'): [('-2', 'Z')],
        ('-4', '1', 'X'): [('-4', 'X')],
        ('-4', '1', 'Z'): [('-4', 'Z')],
        ('END_0', '', 'Z'): [('END_0', '')],
        ('END_1', '', 'X'): [('END_0', '')]
    }
    return PDA(states, alphabet, stack_alphabet, start_state, start_stack, transitions)


# Create a PDA to accept all k-flimsy binary numbers
def create_flimsy_PDA(k):
    assert (type(k) == int) and (k > 1) and (k % 2 == 1)
    states = {'END_0'}
    alphabet = {'0', '1', EMPTY_STRING}
    stack_alphabet = {'Z', 'X'}
    start_state = '-0'
    start_stack = 'Z'
    transitions = {('END_0', EMPTY_STRING, 'Z'): [('END_0', EMPTY_STRING)],
                   ('END_0', EMPTY_STRING, 'X'): [('END_0', EMPTY_STRING)]}

    for carry in range(k):
        s = str(carry)
        states.add('-' + s)
        states.add('+' + s)
        for si in alphabet:
            if si != EMPTY_STRING:
                i = int(si)
                for z in stack_alphabet:
                    added = i * k + carry
                    new_kn_digit = added % 2
                    new_carry = str(added // 2)
                    if new_kn_digit % 2 == i:
                        transitions[('-' + s, si, z)] = [('-' + new_carry, z)]
                        transitions[('+' + s, si, z)] = [('+' + new_carry, z)]
                    elif new_kn_digit % 2 == 1:
                        assert (i == 0)  # n goes up by 0, kn goes up by 1
                        transitions[('-' + s, si, z)] = [('-' + new_carry, 'X' + z)]
                        if z == 'X':
                            transitions[('+' + s, si, z)] = [('+' + new_carry, EMPTY_STRING)]
                        else:
                            transitions[('+' + s, si, z)] = [('-' + new_carry, z)]
                    else:
                        assert (new_kn_digit % 2 == 0)
                        assert (i == 1)  # n goes up by 1, kn goes up by 0
                        transitions[('+' + s, si, z)] = [('+' + new_carry, 'X' + z)]
                        if z == 'X':
                            transitions[('-' + s, si, z)] = [('-' + new_carry, EMPTY_STRING)]
                        else:
                            transitions[('-' + s, si, z)] = [('+' + new_carry, z)]

    # Add new end states
    # Transitions from END_{i+1} to END_{i} that read nothing but pop an X
    for i in range(int(math.log2(k))):
        new_state = 'END_' + str(i + 1)
        states.add(new_state)
        one_less = 'END_' + str(i)
        transitions[(new_state, EMPTY_STRING, 'X')] = [(one_less, EMPTY_STRING)]

    # 1-transitions that pop nothing from final states to END_x for some x?
    for carry in range(k):
        current_state = '+' + str(carry)
        required_pops = s_2(k + carry) - 1
        transitions[(current_state, '1', 'X')].append(('END_' + str(required_pops), 'X'))
        if required_pops == 0:
            transitions[(current_state, '1', 'Z')].append(('END_' + str(required_pops), 'Z'))

    return PDA(states, alphabet, stack_alphabet, start_state, start_stack, transitions)


# Create a PDA to accept all n where b(n) = b(kn)
def create_k_equal_PDA(k):
    assert (type(k) == int) and (k > 1) and (k % 2 == 1)
    states = {'END_0'}
    alphabet = {'0', '1', EMPTY_STRING}
    stack_alphabet = {'Z', 'X'}
    start_state = '-0'
    start_stack = 'Z'
    transitions = {('END_0', EMPTY_STRING, 'Z'): [('END_0', EMPTY_STRING)]}

    for carry in range(k):
        s = str(carry)
        states.add('-' + s)
        states.add('+' + s)
        for si in alphabet:
            if si != EMPTY_STRING:
                i = int(si)
                for z in stack_alphabet:
                    added = i * k + carry
                    new_kn_digit = added % 2
                    new_carry = str(added // 2)
                    if new_kn_digit % 2 == i:
                        transitions[('-' + s, si, z)] = [('-' + new_carry, z)]
                        transitions[('+' + s, si, z)] = [('+' + new_carry, z)]
                    elif new_kn_digit % 2 == 1:
                        assert (i == 0)  # n goes up by 0, kn goes up by 1
                        transitions[('-' + s, si, z)] = [('-' + new_carry, 'X' + z)]
                        if z == 'X':
                            transitions[('+' + s, si, z)] = [('+' + new_carry, EMPTY_STRING)]
                        else:
                            transitions[('+' + s, si, z)] = [('-' + new_carry, z)]
                    else:
                        assert (new_kn_digit % 2 == 0)
                        assert (i == 1)  # n goes up by 1, kn goes up by 0
                        transitions[('+' + s, si, z)] = [('+' + new_carry, 'X' + z)]
                        if z == 'X':
                            transitions[('-' + s, si, z)] = [('-' + new_carry, EMPTY_STRING)]
                        else:
                            transitions[('-' + s, si, z)] = [('+' + new_carry, z)]

    # Add new end states
    # Transitions from END_{i+1} to END_{i} that read nothing but pop an X
    for i in range(int(math.log2(k))):
        new_state = 'END_' + str(i + 1)
        states.add(new_state)
        one_less = 'END_' + str(i)
        transitions[(new_state, EMPTY_STRING, 'X')] = [(one_less, EMPTY_STRING)]

    # 1-transitions that pop Z (stack bottom) from stack iff reading 100000... would leave PDA at -0 with empty stack
    b = math.floor(math.log2(k)) + 1
    pda_states = {(start_state,
                   start_stack)}  # working backwards from the state we want to get to, simulating reading last 1 plus leading zeros
    for letter in ('0' * b + '1'):
        temp = set()
        for (state, stack) in pda_states:
            # for all (q, S) such that ((state, stack_top) in transitions[(q, letter, S)])
            #     temp.add((q, S))
            assert (len(stack) > 0)

            for (q, let, S) in transitions:
                if let == letter:
                    destinations = transitions[(q, letter, S)]
                    if (state, stack[-1]) in destinations:  # no push or pop
                        new_stack = stack[:-1] + S
                        temp.add((q, new_stack))
                    if (state, EMPTY_STRING) in destinations:  # pop
                        new_stack = stack + S
                        temp.add((q, new_stack))
                    if (len(stack) > 1) and ((state, stack[-2] + 'X') in destinations):  # push
                        new_stack = stack[:-2] + S
                        temp.add((q, new_stack))
        pda_states = temp

    for (state, stack) in pda_states:
        assert (len(stack) > 0)
        stack_top = stack[-1]
        required_pops = len(stack) - 1
        # Add transition (to transitions) from $state to END by popping $stack_height
        transitions[(state, '1', stack_top)].append(('END_' + str(required_pops), stack_top))

    return PDA(states, alphabet, stack_alphabet, start_state, start_stack, transitions)


# Create a PDA to accept all 3-flimsy binary numbers
def create_2_flimsy_ternary_PDA():
    states = {'-0', '-1', '+1', '+0', 'END_0', 'END_1'}
    alphabet = {'0', '1', '2', ''}
    stack_alphabet = {'Z', 'X'}
    start_state = '-0'
    start_stack = 'Z'
    transitions = {
        ('-0', '0', 'Z'): [('-0', 'Z')],
        ('-0', '0', 'X'): [('-0', 'X')],
        ('-0', '1', 'Z'): [('-0', 'XZ')],
        ('-0', '1', 'X'): [('-0', 'XX')],
        ('-0', '2', 'Z'): [('+1', 'Z')],
        ('-0', '2', 'X'): [('-1', '')],
        ('-1', '0', 'Z'): [('-0', 'XZ')],
        ('-1', '0', 'X'): [('-0', 'XX')],
        ('-1', '1', 'Z'): [('+1', 'Z')],
        ('-1', '1', 'X'): [('-1', '')],
        ('-1', '2', 'Z'): [('-1', 'Z')],
        ('-1', '2', 'X'): [('-1', 'X')],
        ('+0', '0', 'Z'): [('+0', 'Z')],
        ('+0', '0', 'X'): [('+0', 'X')],
        ('+0', '1', 'Z'): [('-0', 'Z')],
        ('+0', '1', 'X'): [('+0', ''), ('END_1', 'X')],
        ('+0', '2', 'Z'): [('+1', 'XZ'), ('END_0', 'Z')],
        ('+0', '2', 'X'): [('+1', 'XX'), ('END_0', 'X')],
        ('+1', '0', 'Z'): [('-0', 'Z')],
        ('+1', '0', 'X'): [('+0', '')],
        ('+1', '1', 'Z'): [('+1', 'XZ'), ('END_0', 'Z')],
        ('+1', '1', 'X'): [('+1', 'XX'), ('END_0', 'X')],
        ('+1', '2', 'Z'): [('+1', 'Z')],
        ('+1', '2', 'X'): [('+1', 'X'), ('END_1', 'X')],
        ('END_1', '', 'X'): [('END_0', '')],
        ('END_0', '', 'Z'): [('END_0', '')],
        ('END_0', '', 'X'): [('END_0', '')]
    }
    return PDA(states, alphabet, stack_alphabet, start_state, start_stack, transitions)


def _char_to_int(c):  # Get integer from generalized ASCII number
    return ord(c) - ord('0')


def _int_to_char(i):  # Get ASCII character for given number
    return chr(ord('0')+i)


def _create_flimsy_transitions(states: set, transitions: dict, stack_change: int, old_carry: str, new_carry: str, read_char: str):
    if stack_change == 0:
        transitions[('-' + old_carry, read_char, 'Z')] = [('-' + new_carry, 'Z')]
        transitions[('-' + old_carry, read_char, 'X')] = [('-' + new_carry, 'X')]
        transitions[('+' + old_carry, read_char, 'Z')] = [('+' + new_carry, 'Z')]
        transitions[('+' + old_carry, read_char, 'X')] = [('+' + new_carry, 'X')]

    elif stack_change == 1:
        transitions[('+' + old_carry, read_char, 'Z')] = [('+' + new_carry, 'XZ')]
        transitions[('+' + old_carry, read_char, 'X')] = [('+' + new_carry, 'XX')]
        transitions[('-' + old_carry, read_char, 'Z')] = [('+' + new_carry, 'Z')]
        transitions[('-' + old_carry, read_char, 'X')] = [('-' + new_carry, EMPTY_STRING)]

    elif stack_change == -1:
        transitions[('-' + old_carry, read_char, 'Z')] = [('-' + new_carry, 'XZ')]
        transitions[('-' + old_carry, read_char, 'X')] = [('-' + new_carry, 'XX')]
        transitions[('+' + old_carry, read_char, 'Z')] = [('-' + new_carry, 'Z')]
        transitions[('+' + old_carry, read_char, 'X')] = [('+' + new_carry, EMPTY_STRING)]

    elif stack_change > 1:
        current_state_plus = '+'+old_carry
        current_state_minus = '-'+old_carry
        while stack_change > 1:
            stack_change -= 1
            intermediate_state_plus = 'push_'+str(stack_change)+'_to_+'+new_carry
            intermediate_state_minus = 'pop_'+str(stack_change)+'_to_-'+new_carry
            transitions[(current_state_plus, read_char, 'Z')] = [(intermediate_state_plus, 'XZ')]
            transitions[(current_state_plus, read_char, 'X')] = [(intermediate_state_plus, 'XX')]
            transitions[(current_state_minus, read_char, 'Z')] = [(intermediate_state_plus, 'Z')]
            transitions[(current_state_minus, read_char, 'X')] = [(intermediate_state_minus, EMPTY_STRING)]

            if intermediate_state_plus in states and intermediate_state_minus in states:
                return
            states.add(intermediate_state_plus)
            states.add(intermediate_state_minus)

            current_state_plus = intermediate_state_plus
            current_state_minus = intermediate_state_minus
            read_char = EMPTY_STRING

        final_state_plus = '+'+new_carry
        final_state_minus = '-'+new_carry
        transitions[(current_state_plus, read_char, 'Z')] = [(final_state_plus, 'XZ')]
        transitions[(current_state_plus, read_char, 'X')] = [(final_state_plus, 'XX')]
        transitions[(current_state_minus, read_char, 'Z')] = [(final_state_plus, 'Z')]
        transitions[(current_state_minus, read_char, 'X')] = [(final_state_minus, EMPTY_STRING)]

    elif stack_change < -1:
        current_state_plus = '+' + old_carry
        current_state_minus = '-' + old_carry
        while stack_change < -1:
            stack_change += 1
            intermediate_state_plus = 'pop_' + str(stack_change) + '_to_+' + new_carry
            intermediate_state_minus = 'push_' + str(stack_change) + '_to_-' + new_carry
            transitions[(current_state_minus, read_char, 'Z')] = [(intermediate_state_minus, 'XZ')]
            transitions[(current_state_minus, read_char, 'X')] = [(intermediate_state_minus, 'XX')]
            transitions[(current_state_plus, read_char, 'Z')] = [(intermediate_state_minus, 'Z')]
            transitions[(current_state_plus, read_char, 'X')] = [(intermediate_state_plus, EMPTY_STRING)]

            if intermediate_state_plus in states and intermediate_state_minus in states:
                return
            states.add(intermediate_state_plus)
            states.add(intermediate_state_minus)

            current_state_plus = intermediate_state_plus
            current_state_minus = intermediate_state_minus
            read_char = EMPTY_STRING

        final_state_plus = '+'+new_carry
        final_state_minus = '-'+new_carry
        transitions[(current_state_minus, read_char, 'Z')] = [(final_state_minus, 'XZ')]
        transitions[(current_state_minus, read_char, 'X')] = [(final_state_minus, 'XX')]
        transitions[(current_state_plus, read_char, 'Z')] = [(final_state_minus, 'Z')]
        transitions[(current_state_plus, read_char, 'X')] = [(final_state_plus, EMPTY_STRING)]


# Create a PDA to accept all k-flimsy binary numbers
def create_base_b_k_flimsy_PDA(b, k): 
    assert (type(k) == int) and (type(b) == int) and (k >= 1) and (b > 1)
    while k % b == 0:
        k //= b

    states = {'END_0'}
    alphabet = {EMPTY_STRING}
    for i in range(b):
        alphabet.add(_int_to_char(i))
    stack_alphabet = {'Z', 'X'}
    start_state = '-0'
    start_stack = 'Z'
    transitions = {('END_0', EMPTY_STRING, 'Z'): [('END_0', EMPTY_STRING)],
                   ('END_0', EMPTY_STRING, 'X'): [('END_0', EMPTY_STRING)]}

    for carry in range(k):
        s = _int_to_char(carry)
        states.add('-' + s)
        states.add('+' + s)
        for si in alphabet:
            if si != EMPTY_STRING:
                i = _char_to_int(si)
                added = i * k + carry
                new_kn_digit = added % b
                new_carry = _int_to_char(added // b)
                stack_change = i - new_kn_digit  # if positive, push on + state and pop on - state; else vice versa
                _create_flimsy_transitions(states, transitions, stack_change, s, new_carry, si)

    # Add new end states
    # Transitions from END_{i+1} to END_{i} that read nothing but pop an X
    for i in range(int(math.log2(k))):
        new_state = 'END_' + str(i + 1)
        states.add(new_state)
        one_less = 'END_' + str(i)
        transitions[(new_state, EMPTY_STRING, 'X')] = [(one_less, EMPTY_STRING)]

    # nonzero-transitions that pop nothing from final states to END_x for some x?
    for carry in range(k):
        current_state = '+' + _int_to_char(carry)
        required_pops = s_2(k + carry) - 1
        transitions[(current_state, '1', 'X')].append(('END_' + str(required_pops), 'X'))
        if required_pops == 0:
            transitions[(current_state, '1', 'Z')].append(('END_' + str(required_pops), 'Z'))

    return PDA(states, alphabet, stack_alphabet, start_state, start_stack, transitions)
