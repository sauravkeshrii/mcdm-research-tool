import numpy as np

def vector_normalization(matrix):
    """
    Normalizes the decision matrix using vector normalization.
    x_ij = x_ij / sqrt(sum(x_ij^2))
    """
    matrix = np.array(matrix, dtype=float)
    norm = np.linalg.norm(matrix, axis=0)
    norm = np.where(norm == 0, 1, norm) # Avoid division by zero
    return matrix / norm

def min_max_normalization(matrix, criteria_types):
    """
    Normalizes the matrix using Min-Max method.
    criteria_types: list of 1 (benefit) or -1 (cost)
    """
    matrix = np.array(matrix, dtype=float)
    normalized = np.zeros_like(matrix)
    
    min_vals = np.min(matrix, axis=0)
    max_vals = np.max(matrix, axis=0)
    ranges = max_vals - min_vals
    ranges = np.where(ranges == 0, 1, ranges) # Avoid division by zero

    for j, c_type in enumerate(criteria_types):
        if c_type == 1: # Benefit
            normalized[:, j] = (matrix[:, j] - min_vals[j]) / ranges[j]
        else: # Cost
            normalized[:, j] = (max_vals[j] - matrix[:, j]) / ranges[j]
            
    return normalized

def linear_normalization(matrix, criteria_types):
    """
    Linear normalization (Max or Sum based).
    Benefit: x_ij / x_max
    Cost: x_min / x_ij
    """
    matrix = np.array(matrix, dtype=float)
    normalized = np.zeros_like(matrix)
    
    max_vals = np.max(matrix, axis=0)
    min_vals = np.min(matrix, axis=0)
    
    for j, c_type in enumerate(criteria_types):
        if c_type == 1: # Benefit
            div = max_vals[j] if max_vals[j] != 0 else 1
            normalized[:, j] = matrix[:, j] / div
        else: # Cost
            # Handle zeros in data for cost criteria if necessary, usually replace with small epsilon or handle
            denom = matrix[:, j]
            denom = np.where(denom == 0, 1e-9, denom)
            normalized[:, j] = min_vals[j] / denom
            
    return normalized

def sum_normalization(matrix):
    """
    Normalizes so that each column sums to 1.
    x_ij = x_ij / sum(x_ij)
    """
    matrix = np.array(matrix, dtype=float)
    col_sums = np.sum(matrix, axis=0)
    col_sums = np.where(col_sums == 0, 1, col_sums)
    return matrix / col_sums
