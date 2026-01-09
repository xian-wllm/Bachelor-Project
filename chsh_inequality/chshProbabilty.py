import cvxpy as cp
import numpy as np

# Définir les variables d'optimisation pour les corrélations E(A_i, B_j)
E_A0_B0 = cp.Variable()
E_A0_B1 = cp.Variable()
E_A1_B0 = cp.Variable()
E_A1_B1 = cp.Variable()

# Expression CHSH
S = E_A0_B0 + E_A0_B1 + E_A1_B0 - E_A1_B1

# Objectif : Maximiser S
objective = cp.Maximize(S)

# Contraintes de non-signalement
# Les valeurs absolues des corrélations ne peuvent pas dépasser abs(1)
constraints = [
    cp.abs(E_A0_B0) <= 1,
    cp.abs(E_A0_B1) <= 1,
    cp.abs(E_A1_B0) <= 1,
    cp.abs(E_A1_B1) <= 1,
]

problem = cp.Problem(objective, constraints)

problem.solve(solver = "MOSEK")

print("Valeur maximale de S sous contraintes de non-signalement:", problem.value)
print("E(A0, B0):", E_A0_B0.value)
print("E(A0, B1):", E_A0_B1.value)
print("E(A1, B0):", E_A1_B0.value)
print("E(A1, B1):", E_A1_B1.value)
