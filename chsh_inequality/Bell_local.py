import cvxpy as cp
import numpy as np

lambda_behaviors = [
    (0, 0, 0, 0), (0, 0, 0, 1), (0, 0, 1, 0), (0, 0, 1, 1),
    (0, 1, 0, 0), (0, 1, 0, 1), (0, 1, 1, 0), (0, 1, 1, 1),
    (1, 0, 0, 0), (1, 0, 0, 1), (1, 0, 1, 0), (1, 0, 1, 1),
    (1, 1, 0, 0), (1, 1, 0, 1), (1, 1, 1, 0), (1, 1, 1, 1),
]

q = cp.Variable(len(lambda_behaviors), nonneg=True)

# compute chsh with probilitey associated to deterministic behaviour
def compute_CHSH(q, lambda_behaviors):
    CHSH = 0
    for i, behavior in enumerate(lambda_behaviors):
        a0, a1, b0, b1 = (2*output - 1 for output in behavior) # Conversion de 0 en -1, et 1 en +1
        CHSH_contribution = a0*b0 + a0*b1 + a1*b0 - a1*b1
        # print(i)
        # print(f"a0 ", a0 ,"b0 ", b0, "a1 ", a1, "b1", b1)
        
        # print(CHSH_contribution)
        # print()
        CHSH += q[i] * CHSH_contribution

    return CHSH

objective = cp.Maximize(compute_CHSH(q, lambda_behaviors))

constraints = [cp.sum(q) == 1]

problem = cp.Problem(objective, constraints)
problem.solve(solver = cp.MOSEK)

print("Valeur maximale de CHSH sous réalisme local :", problem.value)
print("Probabilités des stratégies déterministes qui maximisent CHSH :")
print(q.value)
