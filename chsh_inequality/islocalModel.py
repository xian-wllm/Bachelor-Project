import cvxpy as cp
import numpy as np

# lambda behaviors
lambda_behaviors = [
    (0, 0, 0, 0), (0, 0, 0, 1), (0, 0, 1, 0), (0, 0, 1, 1),
    (0, 1, 0, 0), (0, 1, 0, 1), (0, 1, 1, 0), (0, 1, 1, 1),
    (1, 0, 0, 0), (1, 0, 0, 1), (1, 0, 1, 0), (1, 0, 1, 1),
    (1, 1, 0, 0), (1, 1, 0, 1), (1, 1, 1, 0), (1, 1, 1, 1),
]

# the deterministic behavior function
def d_lambda(lambda_behavior, x, y, a, b):
    # Extract the behavior for the given inputs
    ax = lambda_behavior[x]
    by = lambda_behavior[2 + y]
    return 1 if (ax == a and by == b) else 0

# Probability matrix P1
# E00 + E01 + E10 - E11 = 2 it should work 
#Modify this matrix to test a specific distribution
P1 = np.array([
    [1/4*(1+1*(1/2 + 1e-4)), 1/4*(1-1*(1/2 + 1e-4)), 1/4*(1-1*(1/2 + 1e-4)), 1/4*(1+1*(1/2 + 1e-4))], #E00 = 1
    [1/4*(1+1*(1/2 + 1e-4)), 1/4*(1-1*(1/2 + 1e-4)), 1/4*(1-1*(1/2 + 1e-4)), 1/4*(1+1*(1/2 + 1e-4))], #E00 = 1
    [1/4*(1+1*(1/2 + 1e-4)), 1/4*(1-1*(1/2 + 1e-4)), 1/4*(1-1*(1/2 + 1e-4)), 1/4*(1+1*(1/2 + 1e-4))], #E00 = 1
    [1/4*(1-1*(1/2 + 1e-4)), 1/4*(1+1*(1/2 + 1e-4)), 1/4*(1+1*(1/2 + 1e-4)), 1/4*(1-1*(1/2 + 1e-4))], #E00 = 1
])

# # E00 + E01 + E10 - E11 = 4 it should not work (it didn't :) )
# P2 =  np.array([
#     [0.5, 0., 0., 0.5], #E00 = 1
#     [0.5, 0., 0., 0.5], #E01 = 1
#     [0.5, 0., 0., 0.5], #E10 = 1
#     [0., 0.5, 0.5, 0.]  #E11 = -1
# ])


# Number of inputs/outputs and lambda behaviors
num_behaviors = len(lambda_behaviors)
num_inputs = 2  # Since x, y can be 0 or 1

# q variables (one for each lambda)
q = cp.Variable(num_behaviors, nonneg=True)

# Constraints
constraints = [cp.sum(q) == 1]  # Ensure q sums to 1
#
# the constraints for each entry and output in the probability matrix
for i in range(num_inputs):
    for j in range(num_inputs):
        for a in range(num_inputs):
            for b in range(num_inputs):
                # Define the linear combination for this particular P1 value
                constraints.append(
                    sum(q[k] * d_lambda(lambda_behaviors[k], i, j, a, b) for k in range(num_behaviors))\
                        == P1[j*2+i, b*2+a]
                )
               

problem = cp.Problem(cp.Minimize(0), constraints)  
problem.solve(solver = cp.MOSEK)

q_values = q.value
feasible = problem.status == cp.OPTIMAL
q_values, feasible
print(problem.status)
print(q_values)
print(feasible)
print(problem.solution)