import cvxpy as cp
import numpy as np
from usefulFunction import *


def is_feasable(v, num_vertice):
    #P_O = [(3*v+1)/8, (1-v)/8, (1-v)/8, (1-v)/8, (1-v)/8, (1-v)/8, (1-v)/8, (3*v+1)/8]
    P_O = [(1-v)/8, v*(1/3) + (1-v)/8, v*(1/3) + (1-v)/8, (1-v)/8, v*(1/3) + (1-v)/8, (1-v)/8, (1-v)/8, (1-v)/8]

    P_O = np.reshape(P_O, (2, 2, 2))   
    dimensions = (2,) * num_vertice
    P_I = create_variable_array(dimensions)
    P_I_linear = P_I.flatten()
    constraints = generate_dynamic_constraints(P_I, P_O, dimensions)

    def apply_symmetry_constraints(P_I, symmetry_groups):
        for group in symmetry_groups:
            for i in range(len(group) - 1):
                constraints.append(P_I[group[i]] == P_I[group[i + 1]])

    apply_symmetry_constraints(P_I_linear, generate_last_symmetry_group_decimal(num_vertice))
    
    problem = cp.Problem(cp.Minimize(0), constraints)
    problem.solve(solver=cp.MOSEK, canon_backend=cp.SCIPY_CANON_BACKEND)

    return problem.status == cp.OPTIMAL


results = {}
epsilon = 1e-6
for vertices in range(4, 7):  
    v_low, v_high = 0, 1
    while v_high - v_low > epsilon:
        v = (v_high + v_low) / 2
        if is_feasable(v, vertices):
            v_low = v
            print(f"Faisable;", v_low)
        else:
            v_high = v
            print(f"Infaisable;", v_high)


    results[vertices] = v
    print(v)


# for vertices, value in results.items():
#     print(f"Pour {vertices} sommets, la valeur de v est: {value:}")



