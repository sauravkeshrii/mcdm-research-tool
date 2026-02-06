import unittest
import numpy as np
import sys
import os

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from mcdm_calculator.core import weighting, ranking

class TestMCDMVerification(unittest.TestCase):
    
    def setUp(self):
        # Sample Decision Matrix (5 Alts, 4 Criteria)
        # Random but consistent
        self.matrix = np.array([
            [250, 16, 12, 5],
            [200, 16, 8, 3],
            [300, 32, 16, 4],
            [275, 32, 8, 4],
            [225, 16, 16, 2]
        ])
        # Criteria Types: Cost, Benefit, Benefit, Benefit
        # C1 (Price) -> Cost
        # C2 (Storage) -> Benefit
        # C3 (Camera) -> Benefit
        # C4 (Looks) -> Benefit
        self.c_types = [-1, 1, 1, 1]
        
    def test_merec_weights(self):
        weights = weighting.merec_weighting(self.matrix, self.c_types)
        self.assertAlmostEqual(np.sum(weights), 1.0, places=5)
        self.assertEqual(len(weights), 4)
        print(f"\nMEREC Weights: {weights}")
        
    def test_entropy_weights(self):
        weights = weighting.entropy_weighting(self.matrix)
        self.assertAlmostEqual(np.sum(weights), 1.0, places=5)
        print(f"\nEntropy Weights: {weights}")
        
    def test_topsis_ranking(self):
        weights = np.array([0.25, 0.25, 0.25, 0.25])
        scores = ranking.topsis_ranking(self.matrix, weights, self.c_types)
        self.assertEqual(len(scores), 5)
        self.assertTrue(np.all(scores >= 0) and np.all(scores <= 1))
        
        # Test consistency: Alt 2 (row 1) [200, 16, 8, 3] vs Alt 0 [250, 16, 12, 5]
        # Alt 2 is cheaper (Good), but worse on C3, C4. 
        # Just checking it runs without error.
        print(f"\nTOPSIS Scores: {scores}")
        
    def test_vikor_ranking(self):
        weights = np.array([0.25, 0.25, 0.25, 0.25])
        q_vals = ranking.vikor_ranking(self.matrix, weights, self.c_types)
        print(f"\nVIKOR Q values: {q_vals}")
        self.assertEqual(len(q_vals), 5)
        
    def test_mairca_ranking(self):
        weights = np.array([0.25, 0.25, 0.25, 0.25])
        gap_vals = ranking.mairca_ranking(self.matrix, weights, self.c_types)
        print(f"\nMAIRCA Gaps: {gap_vals}")
        self.assertEqual(len(gap_vals), 5)

if __name__ == '__main__':
    unittest.main()
