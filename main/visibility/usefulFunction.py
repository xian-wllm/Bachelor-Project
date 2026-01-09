import numpy as np
import cvxpy as cp
from itertools import product
from concurrent.futures import ProcessPoolExecutor

def create_variable_array(dimensions):
    # Vérifie que dimensions est une liste ou un tuple de tailles de dimension
    if not isinstance(dimensions, (list, tuple)) or not all(isinstance(d, int) for d in dimensions):
        raise ValueError("Les dimensions doivent être une liste ou un tuple d'entiers.")
    
    # Initialiser la structure de données pour contenir les variables
    array = np.empty(dimensions, dtype=object)
    
    # Remplir le tableau avec des variables cvxpy
    for index in np.ndindex(array.shape):
        array[index] = cp.Variable(nonneg=True)
        
    return array


def generate_cyclic_permutations(binary_string):
    permutations = []
    for i in range(len(binary_string)):
        rotated_binary = binary_string[i:] + binary_string[:i]
        permutations.append(rotated_binary)
    return permutations


def binary_to_decimal(binary_string):
    return int(binary_string, 2)


def generate_last_symmetry_group_decimal(n):
    def generate_combinations(prefix, length):
        if length == 0:
            return [prefix]
        combinations = []
        for bit in ['0', '1']:
            combinations.extend(generate_combinations(prefix + bit, length - 1))
        return combinations

    last_group = []
    for length in range(1, n + 1):
        combinations = generate_combinations('', length)
        grouped_combinations = {}
        for combination in combinations:
            cyclic_permutations = generate_cyclic_permutations(combination)
            key = tuple(sorted(cyclic_permutations))
            if key not in grouped_combinations:
                grouped_combinations[key] = []
            grouped_combinations[key].append(combination)
        last_group = list(grouped_combinations.values())
    
    # convertir les nombres binaires en décimal et filtrer les groupes avec plus d'un élément
    last_group_decimal = []
    for group in last_group:
        if len(group) > 1:
            decimal_group = [binary_to_decimal(num) for num in group]
            last_group_decimal.append(decimal_group)
    
    return last_group_decimal


def generate_polygon_constraints(P_I, P_O, dimensions):
    
    constraints = []
    # initial constraint
    constraints.append(np.sum(P_I, axis=tuple(range(len(dimensions)))) == 1)
    vertice = len(dimensions)
    # dynamically generate index ranges based on the number of sides
    indices = [range(2)] * (vertice - 2)
    
    # generate all possible combinations of indices
    for index_tuple in product(*indices):
        index_list = list(index_tuple)


        
        #adding constraints based on the polygon's side number
        constraints.append(np.sum(P_I, (2, vertice-1))[tuple(index_list)] == 
                           np.sum(P_O, (2))[tuple(index_list[:2])] * 
                           np.sum(P_I, (0, 1, 2, vertice-1))[tuple(index_list[2:])])
                           
        
        constraints.append(np.sum(P_I, (1, vertice-1))[tuple(index_list)] == 
                           np.sum(P_O, (1, 2))[index_list[0]] * 
                           np.sum(P_I, (0, 1, vertice -1))[tuple(index_list[1:])])

        ### other types of constraints
        #constraints.append(np.sum(P_I, (tuple(range(2, vertice))))[tuple(index_list[:2])] ==
        #                   np.sum(P_O, (2))[tuple(index_list[:2])])

    return constraints


def generate_dynamic_constraints(P_I, P_O, dimensions):
    """
    Generate dynamic constraints for a given form with arbitrary dimensions.
    
    :param P_I: N-dimensional array representing the input probability space.
    :param P_O: N-dimensional array representing the output probability space.
    :param dimensions: Tuple or list indicating the dimensions of P_I.
    :return: A list of constraints generated dynamically based on dimensions.
    """
    constraints = []
    # Normalization constraint

    num_vertice = len(dimensions)

    if num_vertice < 4:
        raise ValueError("Le nombre de dimensions doit être au moins de 4 pour former une géométrie valide.")


    constraints.append(np.sum(P_I, axis=tuple(range(num_vertice))) == 1)
    indices = [range(2)] * (num_vertice - 2)

    #the unique specific case
    if num_vertice == 4:
        
        for i ,j in product(*indices):
            constraints.append(np.sum(P_I, (1, 3))[i][j] == np.sum(P_O, (1, 2))[i] * np.sum(P_O, (1, 2))[j])
            constraints.append(np.sum(P_I, (2, 3))[i][j] == np.sum(P_O, (2))[i][j])

    #general case starting from pentagon
    else:

        #constraints =  generate_polygon_constraints_parallel(P_I, P_O, dimensions)
        constraints = generate_polygon_constraints(P_I, P_O, dimensions)

    return constraints



def add_constraints(index_tuple, P_I, P_O, dimensions):
    vertice = len(dimensions)
    index_list = list(index_tuple)
    constraints = []
    
    # ajout des contraintes basées sur le nombre de côtés du polygone
    constraints.append((np.sum(P_I, (2, vertice-1))[tuple(index_list)] == 
                        np.sum(P_O, (2))[tuple(index_list[:2])] * 
                        np.sum(P_I, (0, 1, 2, vertice-1))[tuple(index_list[2:])]))
    
    constraints.append((np.sum(P_I, (1, vertice-1))[tuple(index_list)] == 
                        np.sum(P_O, (1, 2))[index_list[0]] * 
                        np.sum(P_I, (0, 1, vertice -1))[tuple(index_list[1:])]))
    
    return constraints

def generate_polygon_constraints_parallel(P_I, P_O, dimensions):
    constraints = []
    vertice = len(dimensions)
    indices = [range(2)] * (vertice - 2)
    
    # préparation pour exécuter en parallèle
    all_index_tuples = list(product(*indices))
    
    # utilisation de ProcessPoolExecutor pour paralléliser
    with ProcessPoolExecutor(max_workers=15) as executor:
        futures = [executor.submit(add_constraints, index_tuple, P_I, P_O, dimensions) for index_tuple in all_index_tuples]
        
        for future in futures:
            constraints.extend(future.result())
    
    # contrainte initiale
    constraints.append(np.sum(P_I, axis=tuple(range(len(dimensions)))) == 1)
    
    return constraints
