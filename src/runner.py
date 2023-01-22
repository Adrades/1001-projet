from src.loader import ProtLoader
from src.edit_distance import nvpd
from sys import argv

import os

# TODO real parser ?
def prot_parser():
    if len(argv) != 3:
        print("You must launch the program with two file names.")
        print(f"Program launched with arguments: {argv}")
    p1 = ProtLoader(argv[1])
    p2 = ProtLoader(argv[2])
    print(f"Sequence 1: {p1.name}({len(p1.prot)})")
    print(f"Sequence 2: {p2.name}({len(p2.prot)})")
    return p1.prot, p2.prot


def run():
    p1, p2 = prot_parser()
    omega = set(p1)
    omega.update(set(p2))
    omega = "".join(list(omega))

    print(f"Omega: {omega}")

    r = nvpd(p1, p2, omega)

    print(r[-1, -1])
