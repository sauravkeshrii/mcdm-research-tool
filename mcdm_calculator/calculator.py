import argparse
import pandas as pd
import numpy as np
import sys
import os
import json

# Add current directory to path to allow imports if running from root
sys.path.append(os.getcwd())

from mcdm_calculator.core import normalization, weighting, ranking

def load_data(filepath):
    """
    Load data from CSV.
    Expected format: 
    - Index column as 0
    - Columns are criteria names
    """
    try:
        df = pd.read_csv(filepath, index_col=0)
        return df
    except Exception as e:
        print(f"Error loading file: {e}")
        sys.exit(1)

def parse_criteria_types(types_str, num_criteria):
    """
    Parse criteria types from string argument.
    Format: "1,1,-1,1" or "cost,benefit,..."
    Returns list of 1/-1
    """
    if not types_str:
        return [1] * num_criteria # Default to all benefit
    
    parts = types_str.split(',')
    if len(parts) != num_criteria:
        print(f"Error: Number of criteria types ({len(parts)}) doesn't match columns ({num_criteria}).")
        sys.exit(1)
        
    types = []
    for p in parts:
        p = p.strip().lower()
        if p in ['1', 'benefit', 'max', '+']:
            types.append(1)
        elif p in ['-1', 'cost', 'min', '-']:
            types.append(-1)
        else:
            print(f"Unknown criteria type: {p}. Use 1/benefit or -1/cost.")
            sys.exit(1)
    return types

def load_expected_results(filepath):
    """Load expected results from JSON file for comparison."""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading expected results: {e}")
        return None

def compare_results(actual, expected, tolerance=0.01):
    """Compare actual results with expected results."""
    print("\n" + "="*60)
    print("COMPARISON WITH EXPECTED RESULTS")
    print("="*60)
    
    all_match = True
    
    # Compare weights
    if 'weights' in expected:
        print("\nWeights Comparison:")
        exp_weights = np.array(expected['weights'])
        diff = np.abs(actual['weights'] - exp_weights)
        max_diff = np.max(diff)
        
        for i, (act, exp, d) in enumerate(zip(actual['weights'], exp_weights, diff)):
            status = "✓" if d < tolerance else "✗"
            print(f"  Criterion {i+1}: {act:.4f} vs {exp:.4f} (diff: {d:.4f}) {status}")
        
        if max_diff < tolerance:
            print(f"  ✓ Weights match within tolerance ({tolerance})")
        else:
            print(f"  ✗ Weights differ by up to {max_diff:.4f}")
            all_match = False
    
    # Compare scores
    if 'scores' in expected:
        print("\nScores Comparison:")
        exp_scores = np.array(expected['scores'])
        diff = np.abs(actual['scores'] - exp_scores)
        max_diff = np.max(diff)
        
        for i, (act, exp, d) in enumerate(zip(actual['scores'], exp_scores, diff)):
            status = "✓" if d < tolerance else "✗"
            print(f"  Alternative {i+1}: {act:.4f} vs {exp:.4f} (diff: {d:.4f}) {status}")
        
        if max_diff < tolerance:
            print(f"  ✓ Scores match within tolerance ({tolerance})")
        else:
            print(f"  ✗ Scores differ by up to {max_diff:.4f}")
            all_match = False
    
    # Compare ranking
    if 'ranking' in expected:
        print("\nRanking Comparison:")
        exp_ranking = expected['ranking']
        act_ranking = actual['ranking']
        
        matches = sum(1 for a, e in zip(act_ranking, exp_ranking) if a == e)
        print(f"  Expected: {exp_ranking}")
        print(f"  Actual:   {act_ranking}")
        
        if act_ranking == exp_ranking:
            print("  ✓ Rankings match exactly")
        else:
            print(f"  ✗ Rankings differ ({matches}/{len(exp_ranking)} positions match)")
            all_match = False
    
    print("\n" + "="*60)
    if all_match:
        print("✓ ALL CHECKS PASSED - Implementation verified!")
    else:
        print("✗ SOME CHECKS FAILED - Review differences above")
    print("="*60 + "\n")
    
    return all_match

def verbose_topsis(matrix, weights, c_types, criteria_names, alternatives):
    """Run TOPSIS with detailed step-by-step output."""
    print("\n" + "="*60)
    print("TOPSIS - DETAILED STEPS")
    print("="*60)
    
    # Step 1: Vector Normalization
    print("\nStep 1: Vector Normalization")
    print("-" * 40)
    norm_matrix = normalization.vector_normalization(matrix)
    df_norm = pd.DataFrame(norm_matrix, index=alternatives, columns=criteria_names)
    print(df_norm.to_string())
    
    # Step 2: Weighted Normalized Matrix
    print("\nStep 2: Weighted Normalized Matrix")
    print("-" * 40)
    weighted_matrix = norm_matrix * weights
    df_weighted = pd.DataFrame(weighted_matrix, index=alternatives, columns=criteria_names)
    print(df_weighted.to_string())
    
    # Step 3: Ideal Solutions
    print("\nStep 3: Ideal and Anti-Ideal Solutions")
    print("-" * 40)
    ideal = np.zeros(len(weights))
    anti_ideal = np.zeros(len(weights))
    
    for j, c_type in enumerate(c_types):
        if c_type == 1:  # Benefit
            ideal[j] = np.max(weighted_matrix[:, j])
            anti_ideal[j] = np.min(weighted_matrix[:, j])
        else:  # Cost
            ideal[j] = np.min(weighted_matrix[:, j])
            anti_ideal[j] = np.max(weighted_matrix[:, j])
    
    df_ideal = pd.DataFrame({
        'Criterion': criteria_names,
        'Type': ['Benefit' if t == 1 else 'Cost' for t in c_types],
        'Ideal (A*)': ideal,
        'Anti-Ideal (A-)': anti_ideal
    })
    print(df_ideal.to_string(index=False))
    
    # Step 4: Separation Measures
    print("\nStep 4: Separation Measures (Euclidean Distance)")
    print("-" * 40)
    dist_ideal = np.sqrt(np.sum((weighted_matrix - ideal)**2, axis=1))
    dist_anti_ideal = np.sqrt(np.sum((weighted_matrix - anti_ideal)**2, axis=1))
    
    df_dist = pd.DataFrame({
        'Alternative': alternatives,
        'S+ (to Ideal)': dist_ideal,
        'S- (to Anti-Ideal)': dist_anti_ideal
    })
    print(df_dist.to_string(index=False))
    
    # Step 5: Closeness Coefficient
    print("\nStep 5: Closeness Coefficient")
    print("-" * 40)
    scores = dist_anti_ideal / (dist_ideal + dist_anti_ideal + 1e-9)
    
    df_scores = pd.DataFrame({
        'Alternative': alternatives,
        'Closeness (C)': scores,
        'Rank': pd.Series(scores).rank(ascending=False).astype(int)
    })
    df_scores = df_scores.sort_values('Rank')
    print(df_scores.to_string(index=False))
    
    print("="*60 + "\n")
    return scores

def verbose_merec(matrix, c_types, criteria_names):
    """Run MEREC with detailed step-by-step output."""
    print("\n" + "="*60)
    print("MEREC - DETAILED STEPS")
    print("="*60)
    
    # Step 1: Normalization
    print("\nStep 1: Normalization (min/x for benefit, x/max for cost)")
    print("-" * 40)
    n_matrix = np.zeros_like(matrix, dtype=float)
    min_vals = np.min(matrix, axis=0)
    max_vals = np.max(matrix, axis=0)
    
    for j, c_type in enumerate(c_types):
        if c_type == 1:  # Benefit
            n_matrix[:, j] = min_vals[j] / np.where(matrix[:, j] == 0, 1e-9, matrix[:, j])
        else:  # Cost
            n_matrix[:, j] = matrix[:, j] / np.where(max_vals[j] == 0, 1, max_vals[j])
    
    df_norm = pd.DataFrame(n_matrix, columns=criteria_names)
    print(df_norm.to_string())
    
    # Step 2: Overall Performance
    print("\nStep 2: Overall Performance (S_i)")
    print("-" * 40)
    n_matrix = np.where(n_matrix <= 0, 1e-9, n_matrix)
    m = matrix.shape[1]
    S = np.log(1 + (1/m * np.sum(np.abs(np.log(n_matrix)), axis=1)))
    print(f"S values: {S}")
    
    # Step 3: Removal Effects
    print("\nStep 3: Removal Effects (E_j)")
    print("-" * 40)
    E = np.zeros(m)
    
    for j in range(m):
        n_matrix_excl = np.delete(n_matrix, j, axis=1)
        S_prime = np.log(1 + (1/m * np.sum(np.abs(np.log(n_matrix_excl)), axis=1)))
        E[j] = np.sum(np.abs(S_prime - S))
        print(f"  E_{criteria_names[j]}: {E[j]:.6f}")
    
    # Step 4: Final Weights
    print("\nStep 4: Final Weights")
    print("-" * 40)
    weights = E / np.sum(E)
    
    df_weights = pd.DataFrame({
        'Criterion': criteria_names,
        'Removal Effect (E)': E,
        'Weight': weights
    })
    print(df_weights.to_string(index=False))
    print(f"\nSum of weights: {np.sum(weights):.6f}")
    
    print("="*60 + "\n")
    return weights

def main():
    parser = argparse.ArgumentParser(
        description="MCDM Calculator CLI - Multi-Criteria Decision Making Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage with MEREC + TOPSIS
  python calculator.py data.csv --weights merec --ranking topsis --types "-1,1,1,1"
  
  # Verbose mode with detailed steps
  python calculator.py data.csv --weights merec --ranking topsis --types "-1,1,1,1" --verbose
  
  # Compare with expected results
  python calculator.py data.csv --compare expected.json --verbose
        """
    )
    
    parser.add_argument('data', type=str, help='Path to input CSV file')
    parser.add_argument('--weights', type=str, default='merec', 
                       choices=['merec', 'entropy', 'critic', 'equal', 'manual'], 
                       help='Weighting method (default: merec)')
    parser.add_argument('--ranking', type=str, default='topsis', 
                       choices=['topsis', 'vikor', 'mairca'], 
                       help='Ranking method (default: topsis)')
    parser.add_argument('--types', type=str, 
                       help='Criteria types. Comma separated, e.g., "-1,1,1,1" or "cost,benefit,benefit,benefit". Default: all benefit')
    parser.add_argument('--manual-weights', type=str, 
                       help='Manual weights (comma separated) if --weights=manual')
    parser.add_argument('--verbose', '-v', action='store_true', 
                       help='Show detailed step-by-step calculations')
    parser.add_argument('--compare', type=str, metavar='FILE',
                       help='Compare results with expected values from JSON file')
    parser.add_argument('--tolerance', type=float, default=0.01,
                       help='Tolerance for comparison (default: 0.01)')
    
    args = parser.parse_args()
    
    # 1. Load Data
    df = load_data(args.data)
    matrix = df.values
    criteria_names = list(df.columns)
    alternatives = list(df.index)
    m, n = matrix.shape
    
    print("\n" + "="*60)
    print("MCDM CALCULATOR")
    print("="*60)
    print(f"\nDataset: {args.data}")
    print(f"Alternatives: {m}")
    print(f"Criteria: {n}")
    print("\nDecision Matrix:")
    print(df.to_string())
    
    # 2. Parse Types
    c_types = parse_criteria_types(args.types, n)
    print(f"\nCriteria Types: {['Benefit' if t == 1 else 'Cost' for t in c_types]}")
    
    # 3. Calculate Weights
    if args.weights == 'manual':
        if not args.manual_weights:
            print("Error: --manual-weights required when --weights=manual")
            sys.exit(1)
        try:
            w = [float(x) for x in args.manual_weights.split(',')]
            if len(w) != n:
                raise ValueError(f"Expected {n} weights, got {len(w)}")
            weights = np.array(w)
            weights = weights / np.sum(weights)  # Normalize
        except Exception as e:
            print(f"Error parsing manual weights: {e}")
            sys.exit(1)
    elif args.weights == 'equal':
        weights = np.ones(n) / n
    elif args.weights == 'entropy':
        if args.verbose:
            print("\n[Entropy method - verbose mode not yet implemented for this method]")
        weights = weighting.entropy_weighting(matrix)
    elif args.weights == 'critic':
        if args.verbose:
            print("\n[CRITIC method - verbose mode not yet implemented for this method]")
        weights = weighting.critic_weighting(matrix)
    elif args.weights == 'merec':
        if args.verbose:
            weights = verbose_merec(matrix, c_types, criteria_names)
        else:
            weights = weighting.merec_weighting(matrix, c_types)
    
    if not args.verbose or args.weights not in ['merec']:
        print(f"\n{'='*60}")
        print(f"WEIGHTS ({args.weights.upper()})")
        print('='*60)
        for name, w in zip(criteria_names, weights):
            print(f"  {name:20s}: {w:.6f}")
        print(f"\nSum of weights: {np.sum(weights):.6f}")
    
    # 4. Ranking
    if args.ranking == 'topsis':
        if args.verbose:
            scores = verbose_topsis(matrix, weights, c_types, criteria_names, alternatives)
        else:
            scores = ranking.topsis_ranking(matrix, weights, c_types)
        score_col = 'Score (Closeness)'
        ascending = False  # Higher is better
    elif args.ranking == 'vikor':
        if args.verbose:
            print("\n[VIKOR verbose mode not yet implemented]")
        scores = ranking.vikor_ranking(matrix, weights, c_types)
        score_col = 'Q Value'
        ascending = True  # Lower is better
    elif args.ranking == 'mairca':
        if args.verbose:
            print("\n[MAIRCA verbose mode not yet implemented]")
        scores = ranking.mairca_ranking(matrix, weights, c_types)
        score_col = 'Total Gap'
        ascending = True  # Lower is better
    
    # 5. Output
    results = pd.DataFrame({
        'Alternative': alternatives,
        score_col: scores
    })
    
    results['Rank'] = results[score_col].rank(ascending=ascending).astype(int)
    results = results.sort_values('Rank')
    
    if not args.verbose:
        print(f"\n{'='*60}")
        print(f"RANKING RESULTS ({args.ranking.upper()})")
        print('='*60)
        print(results.to_string(index=False))
    
    # Save
    out_file = f"result_{args.ranking}_{args.weights}.csv"
    results.to_csv(out_file, index=False)
    print(f"\n✓ Results saved to: {out_file}")
    
    # 6. Comparison (if requested)
    if args.compare:
        expected = load_expected_results(args.compare)
        if expected:
            actual = {
                'weights': weights,
                'scores': scores,
                'ranking': results['Rank'].tolist()
            }
            compare_results(actual, expected, args.tolerance)
    
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
