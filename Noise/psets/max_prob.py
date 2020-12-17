import random
import numpy as np

np.random.seed(1)
N = 10000
p = np.random.randn(10)
p = np.abs(p)
p = p / np.sum(p)
n = p * N


def calc_prob(p, n, N):
    a = N * np.log(N)
    for i in range(len(n)):
        a += n[i] * np.log(p[i] / n[i])
    return np.exp(a)


print(calc_prob(p, n, N))

a = 5
n[5] = n[5] + a
n[6] = n[6] - a

print(calc_prob(p, n, N))


def term(i, j, a, p, N):
    return a * np.log((p[j] * N - a) / p[j] * p[i] / (p[i] * N + a))


print(term(5, 6, a, p, N))

