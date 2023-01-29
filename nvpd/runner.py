from nvpd.nvpd import nvpd
from nvpd.parser import pyNvPDParser

import fastaparser as fp
import os

# TODO real parser ?
def prot_parser():
    args = pyNvPDParser().parse_args()

    fastas = args.fasta
    texts = args.text

    seqs = []

    for fasta in fastas:
        with open(fasta, "r") as file:
            for seq in fp.Reader(file):
                print(f"Sequence: {seq.id}({len(seq.sequence_as_string())})")
                seqs.append(seq.sequence_as_string())

    for text in texts:
        seqs.append(text)

    return seqs[0], seqs[1]


def run():
    p1, p2 = prot_parser()
    r = nvpd(p1, p2)

    print(r)
