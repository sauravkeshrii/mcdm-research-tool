#!/usr/bin/env python3
"""
Quick test script for MCDM Calculator
Run from project root: python test_quick.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mcdm_calculator.core import weighting, ranking, normalization
import numpy as np

# Test data: 3 alternatives, 4 criteria
matrix = np.array([
    [250, 16, 12, 5],  # Alt 1
    [200, 16, 8, 3],   # Alt 2
    [300, 32, 16, 4]   # Alt 3
])

# Criteria types: Cost, Benefit, Benefit, Benefit
c_types = [-1, 1, 1, 1]

print("="*50)
print("MCDM Calculator - Quick Test")
print("="*50)

# Test MEREC Weighting
print("\n1. MEREC Weighting:")
weights_merec = weighting.merec_weighting(matrix, c_types)
print(f"   Weights: {weights_merec}")
print(f"   Sum: {np.sum(weights_merec):.6f}")

# Test Entropy Weighting
print("\n2. Entropy Weighting:")
weights_entropy = weighting.entropy_weighting(matrix)
print(f"   Weights: {weights_entropy}")
print(f"   Sum: {np.sum(weights_entropy):.6f}")

# Test CRITIC Weighting
print("\n3. CRITIC Weighting:")
weights_critic = weighting.critic_weighting(matrix)
print(f"   Weights: {weights_critic}")
print(f"   Sum: {np.sum(weights_critic):.6f}")

# Test TOPSIS Ranking
print("\n4. TOPSIS Ranking:")
scores_topsis = ranking.topsis_ranking(matrix, weights_merec, c_types)
print(f"   Scores: {scores_topsis}")
print(f"   Ranking: {np.argsort(-scores_topsis) + 1}")

# Test VIKOR Ranking
print("\n5. VIKOR Ranking:")
scores_vikor = ranking.vikor_ranking(matrix, weights_merec, c_types)
print(f"   Q Values: {scores_vikor}")
print(f"   Ranking: {np.argsort(scores_vikor) + 1}")

# Test MAIRCA Ranking
print("\n6. MAIRCA Ranking:")
scores_mairca = ranking.mairca_ranking(matrix, weights_merec, c_types)
print(f"   Gap Values: {scores_mairca}")
print(f"   Ranking: {np.argsort(scores_mairca) + 1}")

print("\n" + "="*50)
print("All tests completed successfully!")
print("="*50)
