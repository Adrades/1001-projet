from src.edit_distance import nvpd
from time import time

import edlib
import logging
import timeit
import fastaparser as fp


def load():
    """Load SARS COVID SEQUENCE"""
    seqs = []
    ids = []
    with open("data/sars_seqs.fasta", "r") as f:
        for seq in fp.Reader(f):
            seqs.append(seq.sequence_as_string())
            ids.append(seq.id)
    return seqs, ids


def bench():
    """Use SARS covid sequence to bench edlib against numba powered NvPD"""
    seqs, ids = load()
    times = []
    print("Staring Bench")
    for i in range(len(ids) // 2):
        t0 = time()
        nvpd(seqs[0], seqs[1])
        t1 = time()
        edlib.align(seqs[0], seqs[1])
        t2 = time()
        print(t1 - t0, t2 - t1)
        times.append((t1 - t0, t2 - t1))

    print(times)


"""
     for i in range(#len(ids)//2):
         t1 = timeit.timeit(lambda: nvpd('IRON', 'ARON', 'AIRON'))
         t2 = timeit.timeit(lambda: edlib.align('IRON', 'ARON'))
         times.append((t1, t2))

"""
if __name__ == "__main__":
    bench()
