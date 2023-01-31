from numba import njit, prange
import numpy as np


"""NvPD in Python with Numpy arrays and Numba JIT compilation"""

@njit(cache=False, parallel=True)
def edit_distance_algorithm(a: np.array, b: np.array, o: np.array, n_type):
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

    # N_proc on CPU
    n_proc = 8
    blk_size = (n+1) // n_proc + 1

    mi = np.zeros((u, n), n_type)
    ed = np.zeros((m + 1, n + 1), n_type)

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
        for blk in prange(n_proc):  # parallel
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

    # Since sequence can be longer than short or int size
    n_type = np.byte
    len_max = max(map(len, (a,b,o)))
    if len_max >= np.iinfo(np.longlong).max:
        raise Exception("The alphabet or one of the sequence is too long")
    elif len_max >= np.iinfo(np.intc).max:
        n_type.longlong
    elif len_max >= np.iinfo(np.short).max:
        n_type = np.intc
    elif len_max >= np.iinfo(np.byte).max:
        n_type = np.short

    o_arr = np.array(range(len(set(a + b))), dtype=n_type)
    a_arr = np.fromiter(map(o.find, a), dtype=n_type)
    b_arr = np.fromiter(map(o.find, b), dtype=n_type)

    return edit_distance_algorithm(a_arr, b_arr, o_arr, n_type)


if __name__ == "__main__":
    print(nvpd("EXECUTION", "INTENTION"))
