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


pda = pda_factory.create_flimsy_PDA(k)
write_iterable_to_file(pda.output_gv(), ('{:02d}'.format(k))+'-flimsy.gv')
cfg = pda.to_CFG()
write_iterable_to_file(cfg.to_Maple(), ('{:02d}'.format(k))+'-flimsy.maple')
