from nvpd.nvpd import nvpd

import fastaparser as fp


if __name__ == "__main__":
    with open("data/Enterobacteria_phage_1.fasta", "r") as file:
        for seq in fp.Reader(file):
            seq1 = seq.sequence_as_string()[:30000]
    r = nvpd(seq1, seq1)

