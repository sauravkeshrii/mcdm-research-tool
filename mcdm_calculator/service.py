
import pandas as pd
import numpy as np
import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

from mcdm_calculator.core import normalization, weighting, ranking
from mcdm_calculator.calculator import verbose_topsis, verbose_merec # Reusing existing verbose logic if possible, or refactoring

def calculate_mcdm(df, weights_method, ranking_method, criteria_types, manual_weights=None):
    """
    Core service function to calculate MCDM rankings.
    
    Args:
        df (pd.DataFrame): Input dataframe (Index=Alternatives, Cols=Criteria)
        weights_method (str): 'merec', 'entropy', 'critic', 'equal', 'manual'
        ranking_method (str): 'topsis', 'vikor', 'mairca'
        criteria_types (list): List of 1 (Benefit) or -1 (Cost)
        manual_weights (list, optional): List of weights if weights_method is 'manual'
        
    Returns:
        dict: {
            'results': pd.DataFrame (Final ranking),
            'weights': pd.DataFrame (Weights used),
            'intermediate': dict (Any intermediate steps for display)
        }
    """
    matrix = df.values
    criteria_names = list(df.columns)
    alternatives = list(df.index)
    
    # 1. Calculate Weights
    if weights_method == 'manual':
        if not manual_weights:
            raise ValueError("Manual weights required")
        weights = np.array(manual_weights)
        weights = weights / np.sum(weights)
    elif weights_method == 'equal':
        n = len(criteria_names)
        weights = np.ones(n) / n
    elif weights_method == 'entropy':
        weights = weighting.entropy_weighting(matrix)
    elif weights_method == 'critic':
        weights = weighting.critic_weighting(matrix)
    elif weights_method == 'merec':
        weights = weighting.merec_weighting(matrix, criteria_types)
    else:
        raise ValueError(f"Unknown weighting method: {weights_method}")

    # Prepare weights dataframe for display
    df_weights = pd.DataFrame({
        'Criterion': criteria_names,
        'Weight': weights
    })

    # 2. Calculate Ranking
    # Note: We might want to capture more detailed intermediate steps later
    # For now, we return standard ranking
    
    score_col = 'Score'
    ascending = False

    if ranking_method == 'topsis':
        scores = ranking.topsis_ranking(matrix, weights, criteria_types)
        score_col = 'Closeness Score'
        ascending = False
    elif ranking_method == 'vikor':
        scores = ranking.vikor_ranking(matrix, weights, criteria_types)
        score_col = 'Q Value'
        ascending = True
    elif ranking_method == 'mairca':
        scores = ranking.mairca_ranking(matrix, weights, criteria_types)
        score_col = 'Total Gap'
        ascending = True
    else:
        raise ValueError(f"Unknown ranking method: {ranking_method}")
        
    # 3. Format Results
    results = pd.DataFrame({
        'Alternative': alternatives,
        score_col: scores
    })
    
    results['Rank'] = results[score_col].rank(ascending=ascending).astype(int)
    results = results.sort_values('Rank')
    
    return {
        'results': results,
        'weights': df_weights,
        'intermediate': {} # Placeholder for deeper verbose data
    }
