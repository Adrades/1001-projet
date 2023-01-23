from numba import jit, prange
import numpy as np


@jit(nopython=True, cache=True, parallel=True)
def edit_distance_algorithm(a: np.array, b: np.array, o: np.array):
    """Implement Algorithm 1 from paper"""
    u = int(o.shape[0])
    m = int(a.shape[0])
    n = int(b.shape[0])

    mi = np.zeros((u, n), np.short)
    ed = np.zeros((m + 1, n + 1), np.short)

    for i in prange(u):  # parallel
        for j in range(n):
            # Compute mi[i, j] according to Equation 2
            if j == 0 and b[j] != o[i]:
                mi[i, j] = -1
            elif b[j] == o[i]:
                mi[i, j] = j
            else:
                mi[i, j] = mi[i, j - 1]

    for i in range(m + 1):
        for j in prange(n + 1):  # parallel
            # Compute ed[i, j] according to Equation 3
            if i == 0:
                ed[i, j] = j
            elif j == 0:
                ed[i, j] = i
            elif j - 1 == mi[a[i - 1], j - 1]:
                ed[i, j] = ed[i - 1, j - 1]
            elif mi[a[i - 1], j - 1] == -1:
                ed[i, j] = min(ed[i - 1, j - 1], ed[i - 1, j]) + 1
            elif j - 1 > mi[a[i - 1], j - 1]:
                ed[i, j] = min(
                    ed[i - 1, j - 1] + 1,
                    ed[i - 1, j] + 1,
                    ed[i - 1, mi[a[i - 1], j - 1]] + (j - mi[a[i - 1], j - 1] - 1),
                )
    return ed[m, n]


def nvpd(a: str, b: str, o: str):
    o_arr = np.array([i for i in range(len(o))])
    a_arr = np.array([o.find(s) for s in a])
    b_arr = np.array([o.find(s) for s in b])

    return edit_distance_algorithm(a_arr, b_arr, o_arr)


if __name__ == "__main__":
    print(nvpd("EXECUTION", "INTENTION", "EXCUTION"))
