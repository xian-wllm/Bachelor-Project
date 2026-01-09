import cvxpy as cp
import numpy as np
# P[A_i=a, B_j=b] where i,j in {0,1} and a,b in {+1,-1}
#
P = cp.Variable((4, 4)) # 4 measurement settings (A1B1, A1B2, A2B1, A2B2) for the line, 
                        # 4 outcomes (+1+1, +1-1, -1+1, -1-1) for the column
                        
# objective function: CHSH expression
CHSH = cp.sum(P[:3,[0, 3]] - P[:3, [1, 2]]) - cp.sum(P[3, [0, 3]] - P[3, [1, 2]])


constraints = []

# no-signaling constraints
for a in range(2):
    for b in range(2): 
        constraints += [cp.sum(P[a*2+b, :2]) == cp.sum(P[a*2+b, 2:]),  # A's outcomes independent of B
                        cp.sum(P[a+b*2, ::2]) == cp.sum(P[a+b*2, 1::2])]  # B's outcomes independent of A

# probability constraints
for i in range(4):
    constraints += [P[i] >= 0,  
                    cp.sum(P[i]) == 1]  
    
problem = cp.Problem(cp.Maximize(CHSH), constraints)

problem.solve(verbose= False, solver=cp.MOSEK)

print("Maximum CHSH value under no-signaling constraints:", problem.value)

print("P values:\n", P.value)
