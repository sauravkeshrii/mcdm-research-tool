import numpy as np
from .normalization import vector_normalization, min_max_normalization, linear_normalization

def topsis_ranking(matrix, weights, criteria_types):
    """
    Returns TOPSIS scores (Closeness Coefficient). Higher is better.
    """
    # 1. Vector Normalization
    norm_matrix = vector_normalization(matrix)
    
    # 2. Weighted Normalized Decision Matrix
    weighted_matrix = norm_matrix * weights
    
    # 3. Ideal (A*) and Anti-Ideal (A-) Solutions
    # If Benefit: Max A*, Min A-
    # If Cost: Min A*, Max A-
    
    # However, since we might have costs, let's be explicit
    # max_cols = np.max(weighted_matrix, axis=0) # This is purely mathematical max
    # min_cols = np.min(weighted_matrix, axis=0)
    
    ideal = np.zeros(len(weights))
    anti_ideal = np.zeros(len(weights))
    
    for j, c_type in enumerate(criteria_types):
        if c_type == 1: # Benefit
            ideal[j] = np.max(weighted_matrix[:, j])
            anti_ideal[j] = np.min(weighted_matrix[:, j])
        else: # Cost
            ideal[j] = np.min(weighted_matrix[:, j])
            anti_ideal[j] = np.max(weighted_matrix[:, j])
            
    # 4. Separation Measures (Euclidean Distance)
    dist_ideal = np.sqrt(np.sum((weighted_matrix - ideal)**2, axis=1))
    dist_anti_ideal = np.sqrt(np.sum((weighted_matrix - anti_ideal)**2, axis=1))
    
    # 5. Closeness Coefficient
    # C_i = S- / (S+ + S-)
    score = dist_anti_ideal / (dist_ideal + dist_anti_ideal + 1e-9)
    
    return score

def vikor_ranking(matrix, weights, criteria_types, v=0.5):
    """
    Run VIKOR method. Returns Q values (lower is better).
    v: weight for strategy of maximum group utility (usually 0.5)
    """
    matrix = np.array(matrix, dtype=float)
    
    # 1. Best (f*) and Worst (f-) values for each criterion
    f_star = np.zeros(matrix.shape[1])
    f_minus = np.zeros(matrix.shape[1])
    
    for j, c_type in enumerate(criteria_types):
        if c_type == 1: # Benefit
            f_star[j] = np.max(matrix[:, j])
            f_minus[j] = np.min(matrix[:, j])
        else: # Cost
            f_star[j] = np.min(matrix[:, j])
            f_minus[j] = np.max(matrix[:, j])
            
    # 2. S and R values
    # S_i = Sum( w_j * (f*_j - x_ij) / (f*_j - f-_j) )
    # R_i = Max( w_j * (f*_j - x_ij) / (f*_j - f-_j) )
    
    denom = f_star - f_minus
    denom = np.where(denom == 0, 1e-9, denom)
    
    term = weights * (f_star - matrix) / denom
    # Note: For cost criteria, f* is min. (min - x) is negative?
    # Standard formula: |f*_j - x_ij| / |f*_j - f-_j| usually?
    # Or:
    # Benefit: (f* - x) / (f* - f-) -> (Max - x)/(Max - Min) : 0 at Max, 1 at Min. Correct (regret).
    # Cost:   (x - f*) / (f- - f*) ? -> (x - Min)/(Max - Min) : 0 at Min, 1 at Max. Correct.
    
    normalized_regret = np.zeros_like(matrix)
    for j, c_type in enumerate(criteria_types):
        if c_type == 1:
            normalized_regret[:, j] = (f_star[j] - matrix[:, j]) / denom[j]
        else:
            # f_star is min, f_minus is max. denom is min-max (neg).
            # We want (x - min) / (max - min)
            # (f_star - matrix) is (min - x). 
            # (f_star - f_minus) is (min - max).
            # (min - x) / (min - max) = (x - min) / (max - min). Correct.
            normalized_regret[:, j] = (f_star[j] - matrix[:, j]) / denom[j]
            
    weighted_regret = weights * normalized_regret
    
    S = np.sum(weighted_regret, axis=1)
    R = np.max(weighted_regret, axis=1)
    
    # 3. Q values
    # Q_i = v * (S_i - S*) / (S- - S*) + (1-v) * (R_i - R*) / (R- - R*)
    S_star = np.min(S)
    S_minus = np.max(S)
    R_star = np.min(R)
    R_minus = np.max(R)
    
    # Avoid div by zero
    delta_S = S_minus - S_star
    delta_S = delta_S if delta_S != 0 else 1
    
    delta_R = R_minus - R_star
    delta_R = delta_R if delta_R != 0 else 1
    
    Q = v * (S - S_star) / delta_S + (1 - v) * (R - R_star) / delta_R
    
    return Q # Sort Ascending

def mairca_ranking(matrix, weights, criteria_types):
    """
    MAIRCA (Multi-Attributive Border Approximation area Comparison).
    Returns total gap values (lower/higher? Checking standard).
    Actually final values are sum of gap. Higher gap = worse?
    Standard: Calculate Total Gap Matrix (Gap). Sum Gaps. Ascending order usually preferred (Gap = 0 is best).
    Actually, let's verify MAIRCA flow.
    1. Tp = 1/n (Theoretical Priority)
    2. Real Priorities (Tr = Tp * Weights?) -> No, Tp_j = P_A * w_j?
       Usually: Tp = 1/m (m=alternatives) or something.
       Let's use standard:
       Tp = 1/m (m = number of alternatives).
       Real T_pj = Tp * w_j ? No.
       Let's stick to simple version:
       Gap_ij = T_p_ij - Real_rating_ij
    
    Re-reading standard MAIRCA:
    1. Form theoretical rating matrix (Tp). Tp_ij = P_Ai * w_j. P_Ai = 1/m.
       So Tp_ij = (1/m) * w_j.
    2. Real rating matrix (Tr).
       Multiply normalized matrix elements by Tp? Or direct Mapping?
       Tr_ij = Tp_ij * (normalized_x_ij).
       Normalization: Linear (Max/Min). 
       Benefit: x/Max. Cost: Min/x.
    3. Total Gap Matrix (G).
       G_ij = Tp_ij - Tr_ij.
    4. Final Function values (S_i).
       S_i = Sum(G_ij).
    Rank by S_i Ascending (Smaller gap is better).
    """
    matrix = np.array(matrix, dtype=float)
    m, n = matrix.shape # m alts, n criteria
    
    # 1. Theoretical Priorities
    # each alternative is equally probable initially P(Ai) = 1/m
    prob = 1.0 / m
    Tp = np.tile(prob * weights, (m, 1))
    
    # 2. Real Ratings
    # Linear normalization
    norm_matrix = linear_normalization(matrix, criteria_types) # assumes x/max, min/x
    Tr = Tp * norm_matrix
    
    # 3. Gap Matrix
    G = Tp - Tr
    
    # 4. Sum
    S = np.sum(G, axis=1)
    
    return S # Sort Ascending (Lower is better)