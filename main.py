from PDA import PDA
from CFG import CFG
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

