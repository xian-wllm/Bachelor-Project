import cvxpy as cp
import numpy as np
from usefulFunction import *


def inflation(P_O,num_vertice):
    dimensions = (2,) * num_vertice
    P_I = create_variable_array(dimensions) 
    P_I_linear = P_I.flatten()
    constraints = generate_dynamic_constraints(P_I, P_O, dimensions)
    
    def apply_symmetry_constraints(P_I, symmetry_groups):
        for group in symmetry_groups:
            for i in range(len(group) - 1):
                constraints.append(P_I[group[i]] == P_I[group[i + 1]])

    apply_symmetry_constraints(P_I_linear, generate_last_symmetry_group_decimal(num_vertice))

    return constraints, P_I


def generate_constraints_adding_polygon(P_O, max_inflation):
    
    constraints = []
    P_Is = []  

    for i in range(4, max_inflation + 1):
        constraints_i, P_I = inflation(P_O, i)
        P_Is.append(P_I)
        constraints += constraints_i  

    for i in range(len(P_Is)):
        if i < len(P_Is)-1:
            indices = [range(2)] * (i + 3)  
            for index_tuple in product(*indices):
                
                prev_sum = np.sum(P_Is[i], (i+3))
                curr_sum = np.sum(P_Is[i+1], (i+3, i+4))

                constraints.append(prev_sum[index_tuple] == curr_sum[index_tuple])

    return constraints


def is_feasable(v, num_vertice):
    
    P_O = [(1-v)/8, v*(1/3) + (1-v)/8, v*(1/3) + (1-v)/8, (1-v)/8, v*(1/3) + (1-v)/8, (1-v)/8, (1-v)/8, (1-v)/8]
    #P_O = [(3*v+1)/8, (1-v)/8, (1-v)/8, (1-v)/8, (1-v)/8, (1-v)/8, (1-v)/8, (3*v+1)/8]
    
   
    
    P_O = np.reshape(P_O,(2, 2, 2))

    constraints = generate_constraints_adding_polygon(P_O, num_vertice)

    problem = cp.Problem(cp.Minimize(0), constraints)  
    problem.solve(solver=cp.MOSEK)
    

    return problem.status == cp.OPTIMAL


results = {}
epsilon = 1e-6
for vertices in range(4,13):  
    v_low, v_high = 0, 1
    while v_high - v_low > epsilon:
        v = (v_high + v_low) / 2
        if is_feasable(v, vertices):
            v_low = v
        else:
            v_high = v
    results[vertices] = v

for vertices, value in results.items():
    print(f"Pour {vertices} sommets, la valeur de v est: {value:}")



