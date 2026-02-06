# Example 1: Smartphone Selection

## Problem Description
A consumer wants to select the best smartphone from 5 alternatives based on 4 criteria.

## Decision Matrix

| Alternative | Price ($) | Storage (GB) | Camera (MP) | Looks (1-10) |
|-------------|-----------|--------------|-------------|--------------|
| Phone A     | 250       | 16           | 12          | 5            |
| Phone B     | 200       | 16           | 8           | 3            |
| Phone C     | 300       | 32           | 16          | 4            |
| Phone D     | 275       | 32           | 8           | 4            |
| Phone E     | 225       | 16           | 16          | 2            |

## Criteria Information

- **Price**: Cost (lower is better)
- **Storage**: Benefit (higher is better)
- **Camera**: Benefit (higher is better)
- **Looks**: Benefit (higher is better)

**Criteria Types:** `[-1, 1, 1, 1]`

## Expected Results

### MEREC Weights
```
Price:   0.2097
Storage: 0.2055
Camera:  0.3362
Looks:   0.2486
```

### TOPSIS Ranking
```
Alternative  Score      Rank
Phone C      0.7225     1
Phone A      0.4749     2
Phone B      0.2235     3
Phone D      ~0.47      4
Phone E      ~0.22      5
```

**Interpretation:** Phone C is the best choice (highest storage and camera despite higher price).

## How to Run

```bash
cd /media/NewVolume/mcdm.ai/mcdm-research-tool

# Using MEREC + TOPSIS
.venv/bin/python mcdm_calculator/calculator.py \
  mcdm_calculator/verification/examples/example1_phones.csv \
  --weights merec \
  --ranking topsis \
  --types "-1,1,1,1" \
  --verbose

# Using Entropy + VIKOR
.venv/bin/python mcdm_calculator/calculator.py \
  mcdm_calculator/verification/examples/example1_phones.csv \
  --weights entropy \
  --ranking vikor \
  --types "-1,1,1,1"
```

## Verification

Run the test to verify your implementation matches expected results:
```bash
.venv/bin/python test_quick.py
```
