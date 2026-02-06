import numpy as np
from .normalization import min_max_normalization, sum_normalization

def entropy_weighting(matrix):
    """
    Calculates weights using the Entropy method.
    """
    matrix = np.array(matrix, dtype=float)
    # 1. Normalize (Sum based for Entropy usually, to make P_ij)
    # However, standard entropy usually effectively uses P_ij = x_ij / sum(x_i)
    p_matrix = sum_normalization(matrix)
    
    # 2. Compute Entropy
    k = 1 / np.log(matrix.shape[0])
    
    # Handle log(0)
    p_matrix = np.where(p_matrix == 0, 1e-9, p_matrix)
    
    entropy = -k * np.sum(p_matrix * np.log(p_matrix), axis=0)
    
    # 3. Compute Weights
    div = 1 - entropy
    weights = div / np.sum(div)
    return weights

def critic_weighting(matrix):
    """
    Calculates weights using the CRITIC method (Criteria Importance Through Intercriteria Correlation).
    """
    matrix = np.array(matrix, dtype=float)
    # 1. Normalize (Min-Max recommended usually, let's assume raw data processed or use simple normalization)
    # Usually CRITIC works on normalized data. We'll normalize internally to be safe/standard.
    # We implicitly treat all as benefit for the correlation structure or just capture variance.
    # Let's use min-max normalizing everything to [0,1]
    norm_matrix = (matrix - np.min(matrix, axis=0)) / (np.max(matrix, axis=0) - np.min(matrix, axis=0) + 1e-9)

    # 2. Standard Deviation
    std_dev = np.std(norm_matrix, axis=0)
    
    # 3. Correlation Matrix
    corr_matrix = np.corrcoef(norm_matrix, rowvar=False)
    
    # 4. Measure of Conflict
    # Sum of (1 - r_ij)
    sum_one_minus_corr = np.sum(1 - corr_matrix, axis=0)
    
    # 5. Information Content
    c_vals = std_dev * sum_one_minus_corr
    
    # 6. Weights
    weights = c_vals / np.sum(c_vals)
    return weights

def merec_weighting(matrix, criteria_types):
    """
    Calculates weights using MEREC (Method based on the Removal Effects of Criteria).
    """
    matrix = np.array(matrix, dtype=float)
    
    # 1. Normalize (Simple linear scaling usually: min/max)
    # Logarithmic transformation is part of MEREC, requires normalized data > 0
    # Formula in papers: n_ij.
    # Benefit: min/x_ij? No, MEREC normalization:
    # If Benefit: x_ij / max, If Cost: min / x_ij ? 
    # Let's check standard MEREC.
    # Usually: Benefit: x_min / x_ij  | Cost: x_ij / x_max ... Wait, MEREC uses ln(S) based on performance.
    # Let's stick to a robust simple normalization if specific MEREC norm isn't specified,
    # but MEREC often implies a specific one.
    # Let's use:
    # Benefit: n_ij = min_k(x_kj) / x_ij
    # Cost: n_ij = x_ij / max_k(x_kj)
    # This ensures values <= 1.
    
    n_matrix = np.zeros_like(matrix)
    min_vals = np.min(matrix, axis=0)
    max_vals = np.max(matrix, axis=0)
    
    for j, c_type in enumerate(criteria_types):
        if c_type == 1: # Benefit
             n_matrix[:, j] = min_vals[j] / np.where(matrix[:, j]==0, 1e-9, matrix[:, j])
        else: # Cost
             n_matrix[:, j] = matrix[:, j] / np.where(max_vals[j]==0, 1, max_vals[j])
             
    # 2. Calculate overall performance of alternatives (S_i)
    # S_i = ln(1 + (1/N * sum(|ln(n_ij)|))) -- Wait, typical formulation:
    # S_i = ln (1 + (1/m * Sum( |ln(n_ij)| )))
    
    # Handling ln(n_ij). 0 < n_ij <= 1. ln(n_ij) <= 0. |ln| is positive.
    # Avoid n_ij = 0
    n_matrix = np.where(n_matrix <= 0, 1e-9, n_matrix)
    
    m = matrix.shape[1]
    S = np.log(1 + (1/m * np.sum(np.abs(np.log(n_matrix)), axis=1)))
    
    # 3. Calculate performance without each criterion j (S_ij')
    # S_ij' = ln (1 + (1/m * Sum_{k!=j}( |ln(n_ik)| )))
    
    E = np.zeros(m) # absolute removal effects
    
    for j in range(m):
        # Exclude column j
        n_matrix_excl = np.delete(n_matrix, j, axis=1)
        S_prime = np.log(1 + (1/m * np.sum(np.abs(np.log(n_matrix_excl)), axis=1)))
        
        # 4. Sum of absolute deviations
        E[j] = np.sum(np.abs(S_prime - S))
        
    # 5. Calculate weights
    weights = E / np.sum(E)
    return weights
