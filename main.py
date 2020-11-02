import pda_factory
from sys import argv


def print_iterable(lst):
    for a in lst:
        print(a)


def write_iterable_to_file(lst, filename):
    f = open(filename, 'w')
    for line in lst:
        f.write(line + '\n')
    f.close()

def __main__():
    k = 3
    if len(argv) > 1:
        k = int(argv[1])

    print("k =", k)
    pda = pda_factory.create_flimsy_PDA(k)
    # pda = pda_factory.create_2_flimsy_ternary_PDA()
    # write_iterable_to_file(pda.output_gv(), ('{:02d}'.format(k))+'-flimsy-ternary.gv')
    for m in range (1,19):
        # count = 0
        for n in range (2**(m-1), 2**m):
        # for n in range (3**(m-1), 3**m):
            # P = pda.accepts(pda_factory.base_b(n,3)[::-1])
            # Q = pda_factory.s_b(n,3) > pda_factory.s_b(2*n,3)
            P = pda.accepts(pda_factory.int_to_bin(n)[::-1])
            Q = pda_factory.s_2(n) > pda_factory.s_2(k*n)
            if P != Q:
                # print(n, pda_factory.base_b(n,3), pda_factory.base_b(2*n,3), Q)
                print(n, pda_factory.int_to_bin(n), pda_factory.int_to_bin(k*n), Q)
        #     if Q:
        #         count += 1
        # print (m, count)

    # cfg = pda.to_CFG()
    # write_iterable_to_file(cfg.to_Maple(), ('{:02d}'.format(k))+'-flimsy-ternary.maple')

def next_lex_string(word, alphabet):
    # assert type(word) == str
    # assert type(alphabet) == list
    # assert len(alphabet) > 0
    # for x in word:
    #     assert x in alphabet
    # for i in range (len(alphabet)):
    #     assert type(alphabet[i]) == str
    #     assert len(alphabet[i]) == 1
    #     assert not alphabet[i] in alphabet[i+1:]

    index = len(word) - 1
    while index >= 0:
        if word[index] == alphabet[-1]:
            index -= 1
        else:
            current_char = word[index]
            next_char_index = alphabet.index(current_char) + 1
            next_char = alphabet[next_char_index]
            return word[:index] + next_char + alphabet[0]*(len(word) - index - 1)
    return alphabet[0] * (len(word) + 1)
