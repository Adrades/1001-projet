from sys import argv

# import numpy as np
# import numba

def edit_distance_algorithm(a: list, b: list, o: list):
    """Implement Algorithm 1 from paper"""
    u = len(o)
    m = len(a)
    n = len(b)

    mi = [[0]*n for _ in range(u)]
    ed = [[0]*(n+1) for _ in range(m+1)]

    for i in range(u):  # parallel
        for j in range(n):
            # Compute mi[i][j] according to Equation 2
            if j == 0 and b[j] != o[i]:
                mi[i][j] = None
            elif b[j] == o[i]:
                mi[i][j] = j
            else:
                mi[i][j] = mi[i][j-1]

    for i in range(m+1):
        for j in range(n+1): # parallel
            # Compute ed[i][j] according to Equation 3
            #  print(f"Debug u {u} n {n}, a[i] {a[i-1]} j {j}")
            if i == 0:
              ed[i][j] = j
            elif j == 0:
              ed[i][j] = i
            # lmi = mi[a[i]][j-1]
            elif j-1 == mi[a[i-1]][j-1]:
              ed[i][j] = ed[i-1][j-1]
            elif mi[a[i-1]][j-1] == None:
              ed[i][j] = min(ed[i-1][j-1], ed[i-1][j]) + 1
            elif j-1 > mi[a[i-1]][j-1]:
              ed[i][j] = min(ed[i-1][j-1] + 1, ed[i-1][j] + 1, ed[i-1][mi[a[i-1]][j-1]-1] + (j -mi[a[i-1]][j-1]))
            else:
                raise Exception("Case not handled by eq3, use pdb")

    return ed

def nvpd(a: str, b: str, o: str):
    o_arr = [i for i in range(len(o))]
    a_arr = [o.find(s) for s in a]
    b_arr = [o.find(s) for s in b]

    return edit_distance_algorithm(a_arr, b_arr, o_arr)

if __name__ == "__main__":
    # print(nvpd(args[1], args[2], args[3]))

    print(nvpd("IRON", "AERO", "AEINOR"))