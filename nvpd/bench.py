#!/usr/bin/env python

from nvpd.nvpd import nvpd
from time import time
import timeit

import edlib
import editdistance
import Levenshtein


def bench():
    with open("data/mutated_90_perc_oneline.fasta", "r") as f:
        queryFull = f.readline()
    print("Read query: ", len(queryFull), " characters.")

    with open("data/Enterobacteria_phage_1_oneline.fa", "r") as f:
        targetFull = f.readline()
    print("Read target: ", len(targetFull), " characters.")

    for seqLen in [10, 30, 100, 1000, 10000, 30000]:
        global query
        global target
        query = queryFull[:seqLen]
        target = targetFull[:seqLen]
        numRuns = 10 # max(1000000000 // (seqLen**2), 1)

        print("Sequence length: ", seqLen)

        edlibTime = (
            timeit.timeit(
                stmt="edlib.align(query, target)", number=numRuns, globals=globals()
            )
            / numRuns
        )
        print("Edlib: ", edlibTime)

        editdistanceTime = (
            timeit.timeit(
                stmt="editdistance.eval(query, target)",
                number=numRuns,
                globals=globals(),
            )
            / numRuns
        )
        print("editdistance: ", editdistanceTime)

        levenshteinTime = (
            timeit.timeit(
                stmt="Levenshtein.distance(query, target)",
                number=numRuns,
                globals=globals(),
            )
            / numRuns
        )
        print("levenshtein: ", levenshteinTime)

        nvpd(query, target)
        tt = 0
        for i in range(numRuns):
            t0 = time()
            nvpd(query, target)
            tt += time() - t0
        nvPDTime = tt / numRuns
        print("nvpd: ", nvPDTime)

        print(
            "edlib is %f times faster than editdistance."
            % (editdistanceTime / edlibTime)
        )
        print(
            "edlib is %f times faster than Levenshtein." % (levenshteinTime / edlibTime)
        )
        print("edlib is %f times faster than NvPD." % (nvPDTime / edlibTime))
