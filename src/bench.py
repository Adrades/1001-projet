from src.edit_distance import nvpd

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
    for i in range(len(ids)//2):
        t1 = timeit.timeit(lambda: nvpd(seqs[0], seqs[1]), number=5)
        t2 = timeit.timeit(lambda: edlib.align(seqs[0], seqs[1]), number=5)
        print(t1, t2)
        times.append((t1, t2))

    print(times)
"""
     for i in range(#len(ids)//2):
         t1 = timeit.timeit(lambda: nvpd('IRON', 'ARON', 'AIRON'))
         t2 = timeit.timeit(lambda: edlib.align('IRON', 'ARON'))
         times.append((t1, t2))

"""
if __name__ == "__main__":
    bench()
