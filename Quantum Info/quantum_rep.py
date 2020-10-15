#%%
from scipy.special import comb
import matplotlib.pyplot as plt


def worth_it(p, n):
    # no_error_prob = (1 - p) ** n
    # one_error_probs = n * p * (1 - p) ** (n - 1)
    more_than_one_error_probs = 0
    for j in range(2, n + 1):  # j is number of errors
        more_than_one_error_probs += comb(n, j) * p ** j * (1 - p) ** (n - j)
    return more_than_one_error_probs < p


def find_upper_p(n):
    step_size = 1e-4
    p = 0.5
    while not worth_it(p, n):
        p -= step_size
    return p


#%%
print(worth_it(0.4, 3))

#%% Find upper p for which it is worth using an n rep code
# print(valid(0.2, 3))

data = {"n": [], "p_bound": []}
for n in range(30):
    data["n"].append(n)
    data["p_bound"].append(find_upper_p(n))
    print(str(n) + ": " + str(data["p_bound"][-1]))
# %% Plot

plt.figure()
plt.scatter(data["n"], data["p_bound"])
plt.xlabel("n")
plt.ylabel("Probability Bound for Worthwhile QEC")
plt.savefig("prob_bound.png")
# %%
