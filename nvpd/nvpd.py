from numba import njit, prange
import numpy as np


@njit(cache=True, parallel=True)
def edit_distance_algorithm(a: np.array, b: np.array, o: np.array):
    """Implement Algorithm 1 from paper

    Args:
        a (np.array): The first string viewed as an short int typed array.
            Each value is a position in the alphabet.
        b (np.array): The first string viewed as an short int typed array.
            Each value is a position in the alphabet.
        o (np.array): The alphabet, as a short int typed array.

    """
    u = int(o.shape[0])
    m = int(a.shape[0])
    n = int(b.shape[0])

    # N_proc on CPU or Block size on GPU
    blk_size = 8

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
        for blk in prange((n + 1) // blk_size + 1):  # parallel
            for j in range(blk_size * blk, blk_size * blk + blk_size):
                if j >= n + 1:
                    break
                # Compute ed[i, j] according to Equation 3
                if i == 0:
                    ed[i, j] = j
                elif j == 0:
                    ed[i, j] = i
                elif j == mi[a[i - 1], j - 1] + 1:
                    ed[i, j] = ed[i - 1, j - 1]
                elif mi[a[i - 1], j - 1] == -1:
                    ed[i, j] = min(ed[i - 1, j - 1], ed[i - 1, j]) + 1
                elif j > mi[a[i - 1], j - 1] + 1:
                    ed[i, j] = min(
                        ed[i - 1, j - 1] + 1,
                        ed[i - 1, j] + 1,
                        ed[i - 1, mi[a[i - 1], j - 1]] + (j - mi[a[i - 1], j - 1] - 1),
                    )
    return ed[m, n]


def nvpd(a: str, b: str):
    """Function that convert each string in numpy array
    And then launch the edit distance numba function.
    """
    o = "".join(set(a + b))
    o_arr = np.array(range(len(set(a + b))), dtype=np.short)
    a_arr = np.fromiter(map(o.find, a), dtype=np.short)
    b_arr = np.fromiter(map(o.find, b), dtype=np.short)

    return edit_distance_algorithm(a_arr, b_arr, o_arr)


if __name__ == "__main__":
    print(nvpd("EXECUTION", "INTENTION"))
