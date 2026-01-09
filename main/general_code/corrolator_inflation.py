import cvxpy as cp
import numpy as np
from usefulFunction import *
import time
import matplotlib.pyplot as plt
import matplotlib.cm as cm

def is_feasable(E1, E2, num_vertice, E3=0):
    P_O = [1/8 * (3*E1 + 3*E2 + E3 + 1),   # 000
           1/8 * (E1 - E2 - E3 + 1),       # 001       
           1/8 * (E1 - E2 - E3 + 1),       # 010
           1/8 * (-E1 - E2 + E3 + 1),      # 011
           1/8 * (E1 - E2 - E3 + 1),       # 100
           1/8 * (-E1 - E2 + E3 + 1),      # 101
           1/8 * (-E1 - E2 + E3 +1),       # 110
           1/8 * (-3*E1 +3*E2 - E3 + 1)]   # 111
    
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
    problem.solve(solver=cp.MOSEK)

    return problem.status == cp.OPTIMAL

def bisection_search(low, high, func, epsilon):
    """ Perform bisection search to find the best value within tolerance. """
    while high - low > epsilon:
        mid = (high + low) / 2
        if func(mid):
            low = mid
        else:
            high = mid
    return (high + low) / 2

def calculate_optimal_E1_per_vertex(E2_range, vertices_range, E1_low, E1_high, epsilon):
    """ Calculate the optimal E1 for each E2 and each vertex in the range. """
    value_for_each = {}
    for vertice in vertices_range:
        best_E1s = {}
        for E2 in E2_range:
            ## bisection search for the best E1 for each E2 for the current polygon with n vertice
            best_E1 = bisection_search(E1_low, E1_high, lambda E1: is_feasable(E1, E2, vertice), epsilon)
            best_E1s[E2] = best_E1
        value_for_each[vertice] = best_E1s
        print(f"Results for {vertice} vertices: {best_E1s}")
    return value_for_each

def plot_results(value_for_each):
    """ Plot the results of the E1 calculations. """
    plt.figure(figsize=(12, 8))
    color_palette = cm.tab10.colors
    first_key = next(iter(value_for_each)) if value_for_each else None
    if first_key is None:
        raise ValueError("No data to plot.")

    E2_values = list(value_for_each[first_key].keys())

    for index, (vertices, results) in enumerate(value_for_each.items()):
        E1_values = list(results.values())
        plt.plot(E1_values, E2_values, label=f"{vertices} vertices", color=color_palette[index % 10])


    E1 = np.arange(0.18, 0.5, 0.01)
    E2 = np.array([-0.3333, -0.3333, -0.3333, -0.3333, -0.3206,
              -0.3081, -0.2958, -0.2838, -0.2721, -0.2606,
              -0.2493, -0.2383, -0.2274, -0.2168, -0.2063,
              -0.1960, -0.1859, -0.1759, -0.1661, -0.1564,
              -0.1469, -0.1375, -0.1283, -0.1191, -0.1101,
              -0.1013, -0.0925, -0.0838, -0.0753, -0.0600,
              -0.0400, -0.0200])

    plt.plot(E1, E2, label = "new point added", color = "black")
    plt.ylabel('E2 Values')
    plt.xlabel('E1 Values')
    plt.title('Optimal E1 for Different Vertices and E2 Values')
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    E2_range = np.arange(-1/3, 0, 0.01)  
    E1_low, E1_high = 0.1, 0.5
    epsilon = 1e-6  
    vertices_range = range(4, 7)  

    start_time = time.perf_counter()
    value_for_each = calculate_optimal_E1_per_vertex(E2_range, vertices_range, E1_low, E1_high, epsilon)
    end_time = time.perf_counter()
    
    print(f"Execution time: {end_time - start_time} seconds")
    
    plot_results(value_for_each)


if __name__ == "__main__":
    main()
