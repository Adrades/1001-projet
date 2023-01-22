from src.edit_distance import nvpd
from sys import argv

import fastaparser as fp
import os

# TODO real parser ?
def prot_parser():
    # use Fasta Parser
    if len(argv) != 3:
        print("You must launch the program with two file names.")
        print(f"Program launched with arguments: {argv}")

    with open(argv[1], "r")as file:
        p1 = fp.Reader(file)
        for seq in p1:
            seq1 = seq
            print(f"Sequence 1: {seq.id}({len(seq.sequence_as_string())})")
            break

    with open(argv[2], "r")as file:
        p2 = fp.Reader(file)
        for seq in p2:
            seq2 = seq
            print(f"Sequence 2: {seq.id}({len(seq.sequence_as_string())})")
            break

    return seq1.sequence_as_string(), seq2.sequence_as_string()


def run():
    p1, p2 = prot_parser()
    omega = set(p1)
    omega.update(set(p2))
    omega = "".join(list(omega))

    print(f"Omega: {omega}")

    r = nvpd(p1, p2, omega)

    print(r[-1, -1])
