# Python Levenshtein Distance Calculator using NvPD

Python implementation of the following paper: 

Sadiq, M.U., Yousaf, M.M., Aslam, L. et al. NvPD: novel parallel edit distance algorithm, correctness, and performance evaluation. Cluster Comput 23, 879–894 (2020). https://doi.org/10.1007/s10586-019-02962-w

## How to use
Firstly clone the project.

Install all dependencies from pyproject.toml or use poetry to do it for you:
```
poetry install -n
```

Launch the app with the temporary command:
```
poetry run test data/Q6JAN0.fasta data/Q555C6.fasta 
```

Replace by any other fasta file.
