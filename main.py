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


def test_flimsy_pda(b, k):
    print("k =", k, ", b =", b)
    pda = pda_factory.create_base_b_k_flimsy_PDA(b, k)
    # write_iterable_to_file(pda.output_gv(), ('{:02d}'.format(k))+'-flimsy-ternary.gv')
    for m in range(1, 11):
        # count = 0
        # for n in range (2**(m-1), 2**m):
        # for n in range (3**(m-1), 3**m):
        for n in range(b ** (m - 1), b ** m):
            pda_flimsiness = pda.accepts(pda_factory.base_b(n, b)[::-1])
            real_flimsiness = pda_factory.s_b(n, b) > pda_factory.s_b(k * n, b)

            if pda_flimsiness != real_flimsiness:
                print(n, pda_factory.base_b(n, b), pda_factory.base_b(k * n, b), real_flimsiness)


def __main__():
    k = 3
    if len(argv) > 1:
        k = int(argv[1])

    b = 2
    if len(argv) > 2:
        b = int(argv[2])

    test_flimsy_pda(b,k)

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

# __main__()

pda = pda_factory.create_base_b_k_flimsy_PDA(4,2)
write_iterable_to_file(pda.output_gv(), '02-flimsy-base-4.gv')
