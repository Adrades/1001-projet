#!/usr/bin/env python

from src.edit_distance import nvpd as nvpd1
from src.nvpd import nvpd as nvpd2
from time import time
import timeit

import edlib
import editdistance
import Levenshtein


def bench():
    with open('data/mutated_90_perc_oneline.fasta', 'r') as f:
        queryFull = f.readline()
    print('Read query: ', len(queryFull) ,' characters.')

    with open('data/Enterobacteria_phage_1_oneline.fa', 'r') as f:
        targetFull = f.readline()
    print('Read target: ', len(targetFull) ,' characters.')

    for seqLen in [30, 100, 1000, 10000, 50000]:
        global query
        global target
        query = queryFull[:seqLen]
        target = targetFull[:seqLen]
        numRuns = max(1000000000 // (seqLen**2), 1)

        print('Sequence length: ', seqLen)

        edlibTime = timeit.timeit(stmt="edlib.align(query, target)",
                                  number=numRuns, globals=globals()) / numRuns
        print('Edlib: ', edlibTime)

        editdistanceTime = timeit.timeit(stmt="editdistance.eval(query, target)",
                                         number=numRuns, globals=globals()) / numRuns
        print('editdistance: ', editdistanceTime)

        levenshteinTime = timeit.timeit(stmt="Levenshtein.distance(query, target)",
                                         number=numRuns, globals=globals()) / numRuns
        print('levenshtein: ', levenshteinTime)

        tt = 0
        for i in range(numRuns):
            t0 = time()
            nvpd1(query, target)
            tt += time() - t0
        nvPDTime = tt / numRuns
        print('nvpd1: ', nvPDTime)

        tt = 0
        for i in range(numRuns):
            t0 = time()
            nvpd2(query, target)
            tt += time() - t0
        nvPDTime = tt / numRuns
        print('nvpd2: ', nvPDTime)


        print('edlib is %f times faster than editdistance.' % (editdistanceTime / edlibTime))
        print('edlib is %f times faster than Levenshtein.' % (levenshteinTime / edlibTime))
